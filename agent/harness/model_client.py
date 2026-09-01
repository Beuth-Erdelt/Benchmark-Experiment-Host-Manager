"""Model adapter for the self-hosted inference server.

The server is vLLM, which exposes an OpenAI-compatible chat-completions API, so
this speaks that protocol through the ``openai`` client library -- pointed at
our own server, so no request reaches OpenAI. Nothing above this module knows
which server is behind it: the harness only needs "send messages and tool
schemas, get back text and tool calls".

This module handles exactly one exchange and never runs a tool. The
tool-calling loop lives in :mod:`agent.harness.agent`.

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from typing import Any

from openai import (
    APIConnectionError, InternalServerError, OpenAI, OpenAIError, RateLimitError,
)

__all__ = [
    "ModelNotServed", "ModelUnreachable", "ContextWindowExhausted", "ToolCall",
    "Reply", "ChatModel",
]

#: vLLM does not check credentials, but the OpenAI client insists on a key.
_PLACEHOLDER_API_KEY = "EMPTY"

#: Held back from the context window, because the served chat template adds
#: tokens no client-side estimate can see.
_CONTEXT_MARGIN_TOKENS = 512
#: Below this much room, a turn cannot produce a usable answer, so the phase
#: stops with a reported reason instead of letting the server refuse the request.
_MINIMUM_GENERATION_TOKENS = 1024
#: Attempts made when a metered endpoint refuses a turn for rate limiting.
#: Hosted providers meter per minute, so a phase that would otherwise die
#: mid-investigation waits the meter out instead.
_RETRY_ATTEMPTS = 6
#: First wait after a refused turn; doubled per attempt up to the cap below.
_RETRY_BACKOFF_SECONDS = 5.0
_RETRY_BACKOFF_CAP_SECONDS = 60.0

#: Field names servers publish their context length under, in the order tried.
_CONTEXT_WINDOW_FIELDS = ("max_model_len", "max_context_length")

#: Characters per token for the messages appended since the last exchange.
#: Deliberately low: overestimating the appended text shrinks the generation
#: budget slightly, while underestimating it would overflow the window.
_CHARACTERS_PER_TOKEN = 3


class ContextWindowExhausted(RuntimeError):
    """Raised when the conversation leaves no room to generate an answer.

    The server would refuse such a request outright, which is a setup problem
    (a per-turn ceiling too large for this window, or a phase that read too
    much), not a crash: callers report it the way they report the endpoint
    being unreachable.
    """


class ModelUnreachable(RuntimeError):
    """Raised when the configured endpoint could not be reached at all.

    Also raised when a metered endpoint kept refusing the turn for rate
    limiting until the retries below were spent, which leaves the phase just as
    unable to continue.

    Deliberately not the client library's own exception: this module is the only
    one that knows which server is behind the endpoint, and callers report a
    misconfigured endpoint the way they report any other setup mistake.
    """


class ModelNotServed(RuntimeError):
    """Raised when a multi-model endpoint does not serve the configured model."""


@dataclass
class ToolCall:
    """One tool invocation the model asked for.

    :ivar id: Identifier the tool result must be returned under.
    :ivar name: Tool name.
    :ivar arguments: Decoded arguments, empty when the model emitted invalid JSON.
    :ivar decode_error: Why the arguments could not be decoded, or ``None``.
    """
    id: str
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    decode_error: str | None = None


@dataclass
class Reply:
    """One assistant turn.

    :ivar text: The visible message, empty when the model only called tools.
    :ivar reasoning: Thinking the server separated out, logged but not replayed.
    :ivar tool_calls: Tool invocations requested this turn.
    :ivar message: The assistant message as the server returned it, appended
        to the conversation so the next request replays this turn.
    :ivar usage: Token counts reported by the server.
    :ivar finish_reason: Why the server stopped generating -- ``stop`` for a
        completed turn, ``length`` when the turn was cut off at the token
        ceiling, ``tool_calls`` when it ended on a tool call. Empty when the
        server did not report one.
    :ivar generation_budget: Tokens this turn was allowed to generate, after
        the served context window narrowed the configured ceiling.
    """
    text: str
    reasoning: str
    tool_calls: list[ToolCall]
    message: dict[str, Any]
    usage: dict[str, int]
    finish_reason: str = ""
    generation_budget: int = 0


class ChatModel:
    """A chat model reached over an OpenAI-compatible endpoint.

    :ivar model: Model identifier the server serves it under.
    :ivar temperature: Sampling temperature; zero for the archival runs, so a
        trajectory replays the same way.
    :ivar max_tokens: Ceiling on tokens generated per turn.
    """

    def __init__(
        self,
        model: str,
        base_url: str,
        api_key: str = _PLACEHOLDER_API_KEY,
        temperature: float = 0.0,
        max_tokens: int = 16384,
        timeout: float = 600.0,
    ) -> None:
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout)
        self._context_window: int | None = None
        self._context_window_asked = False
        self._counted_messages = 0
        self._counted_prompt_tokens = 0
        #: Seam so a test can exercise the backoff without waiting for it.
        self._sleep = time.sleep

    def resolve_served_model(self) -> str:
        """Resolve a configured alias against the endpoint's model list.

        A dedicated endpoint often serves one model under an implementation-
        chosen identifier. That identifier is unambiguous and safe to adopt.
        A multi-model endpoint requires an exact configured match instead.

        :return: Model identifier that subsequent requests will use.
        :rtype: str
        :raises ModelNotServed: When no exact match exists and the endpoint does
            not advertise exactly one alternative.
        """
        try:
            identifiers = [
                entry.id for entry in self._client.models.list().data
                if isinstance(getattr(entry, "id", None), str) and entry.id
            ]
        except OpenAIError:
            # Some compatible servers do not implement model discovery. Let the
            # first completion retain the configured name and report any error.
            return self.model
        if self.model in identifiers:
            return self.model
        if len(identifiers) != 1:
            available = ", ".join(identifiers) or "none"
            raise ModelNotServed(
                f"configured model {self.model!r} is not served; available models: "
                f"{available}"
            )
        self.model = identifiers[0]
        self._context_window = None
        self._context_window_asked = False
        return self.model

    def _window(self) -> int | None:
        """Return the served context length, asking the server once.

        :return: Tokens the server accepts per request, or ``None`` when it does
            not publish the figure.
        :rtype: int | None
        """
        if not self._context_window_asked:
            self._context_window_asked = True
            try:
                for entry in self._client.models.list().data:
                    if entry.id == self.model:
                        self._context_window = _published_window(entry)
                        break
            except OpenAIError:
                # A server that will not list its models still answers requests;
                # without a window the per-turn ceiling stands unchanged.
                self._context_window = None
        return self._context_window

    def _prompt_tokens(self, messages: list[dict[str, Any]]) -> int:
        """Estimate the tokens this conversation will occupy.

        Anchored on the exact count the server reported for the previous
        request, so only the turns appended since then are estimated.

        :param messages: Full conversation about to be sent.
        :return: Estimated prompt tokens.
        :rtype: int
        """
        appended = messages
        counted = 0
        if self._counted_messages and len(messages) >= self._counted_messages:
            appended = messages[self._counted_messages:]
            counted = self._counted_prompt_tokens
        characters = sum(len(json.dumps(message, default=str)) for message in appended)
        return counted + characters // _CHARACTERS_PER_TOKEN

    def _generation_budget(self, messages: list[dict[str, Any]]) -> int:
        """Cap this turn's output so the request fits the server's window.

        :param messages: Full conversation about to be sent.
        :return: Tokens this turn may generate.
        :rtype: int
        :raises ContextWindowExhausted: When too little room is left to answer.
        """
        window = self._window()
        if window is None:
            return self.max_tokens
        room = window - self._prompt_tokens(messages) - _CONTEXT_MARGIN_TOKENS
        if room < _MINIMUM_GENERATION_TOKENS:
            raise ContextWindowExhausted(
                f"the conversation leaves {max(room, 0)} of {window} tokens for an "
                f"answer, below the {_MINIMUM_GENERATION_TOKENS} needed"
            )
        return min(self.max_tokens, room)

    def _create_with_backoff(self, request: dict[str, Any]) -> Any:
        """Send one request, waiting out a refusal the endpoint will recover from.

        Two refusals are temporary and worth waiting for rather than losing an
        investigation to: a metered API's per-minute quota, which clears on its
        own, and a hosted endpoint that is momentarily out of capacity. A
        self-hosted server queues instead of refusing, so this only engages
        against a hosted API.

        :param request: Keyword arguments for the chat-completions call.
        :return: The server's completion.
        :raises ModelUnreachable: When every attempt was refused.
        """
        wait = _RETRY_BACKOFF_SECONDS
        for attempt in range(1, _RETRY_ATTEMPTS + 1):
            try:
                return self._client.chat.completions.create(**request)
            except (RateLimitError, InternalServerError) as error:
                refusal = (
                    "rate limiting" if isinstance(error, RateLimitError)
                    else "a server-side failure"
                )
                if attempt == _RETRY_ATTEMPTS:
                    raise ModelUnreachable(
                        f"{self.base_url} refused {_RETRY_ATTEMPTS} attempts for "
                        f"{refusal}: {error}"
                    ) from error
                delay = _retry_after(error) or wait
                print(
                    f"the endpoint refused this turn for {refusal}; "
                    f"retrying attempt {attempt + 1} of {_RETRY_ATTEMPTS} in {delay:g}s",
                    file=sys.stderr, flush=True,
                )
                self._sleep(delay)
                wait = min(wait * 2, _RETRY_BACKOFF_CAP_SECONDS)

    def reply(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> Reply:
        """Send one request and return the assistant's turn.

        :param messages: Full conversation so far, in OpenAI message shape.
        :param tools: Tool schemas the model may call; ``None`` withdraws them,
            which forces a text-only turn.
        :return: The parsed assistant turn.
        :rtype: Reply
        :raises ModelUnreachable: When the endpoint did not answer at all.
        :raises ContextWindowExhausted: When the conversation leaves no room to
            answer, so the server would refuse the request.
        """
        budget = self._generation_budget(messages)
        request: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": budget,
        }
        if tools:
            request["tools"] = tools
        try:
            response = self._create_with_backoff(request)
        except APIConnectionError as error:
            raise ModelUnreachable(
                f"no answer from {self.base_url}: {error}"
            ) from error
        choice = response.choices[0]
        message = choice.message
        replayed = message.model_dump(exclude_none=True)
        # Only a string finish reason is meaningful; anything else (a server that
        # omits the field, a test double) is reported as unknown.
        finish_reason = getattr(choice, "finish_reason", None)
        if not isinstance(finish_reason, str):
            finish_reason = ""
        # A reasoning model returns its thinking in a separate field. Qwen's own
        # guidance is not to feed previous thinking back in, and some servers
        # reject the field on input, so it is logged but not replayed.
        # vLLM 0.27 renamed ``reasoning_content`` to ``reasoning``. Remove both
        # spellings so hidden thinking is never replayed into the next request.
        reasoning = replayed.pop("reasoning", None)
        legacy_reasoning = replayed.pop("reasoning_content", None)
        reasoning = reasoning or legacy_reasoning
        usage = response.usage.model_dump() if response.usage else {}
        if isinstance(usage.get("prompt_tokens"), int):
            # Anchor the next turn's estimate on what the server actually counted.
            self._counted_messages = len(messages)
            self._counted_prompt_tokens = usage["prompt_tokens"]
        return Reply(
            text=message.content or "",
            reasoning=reasoning or "",
            tool_calls=[_parse_tool_call(call) for call in (message.tool_calls or [])],
            message=replayed,
            usage=usage,
            finish_reason=finish_reason,
            generation_budget=budget,
        )


def _retry_after(error: OpenAIError) -> float | None:
    """Return the wait the refusing server asked for, when it named one.

    :param error: The refusal raised by the client library.
    :return: Seconds to wait, or ``None`` when no usable header was sent.
    :rtype: float | None
    """
    response = getattr(error, "response", None)
    header = getattr(response, "headers", {}).get("retry-after") if response else None
    try:
        return float(header) if header is not None else None
    except (TypeError, ValueError):
        return None


def _published_window(entry: Any) -> int | None:
    """Return the context length a listed model publishes, if it publishes one.

    The field is not part of the OpenAI protocol, so each server names it
    differently: vLLM reports ``max_model_len``, Mistral ``max_context_length``.
    A server that reports neither leaves the window unknown.

    :param entry: One model as the server listed it.
    :return: Tokens the server accepts per request, or ``None``.
    :rtype: int | None
    """
    for name in _CONTEXT_WINDOW_FIELDS:
        length = getattr(entry, name, None)
        if isinstance(length, int) and not isinstance(length, bool):
            return length
    return None


def _parse_tool_call(call: Any) -> ToolCall:
    """Decode one tool call, keeping a JSON failure as data rather than raising.

    A model that emits malformed arguments should be told so and get another
    turn, exactly as it would for any other rejected call.

    :param call: A tool call object from the client library.
    :return: The decoded call.
    :rtype: ToolCall
    """
    try:
        arguments = json.loads(call.function.arguments or "{}")
    except json.JSONDecodeError as error:
        return ToolCall(id=call.id, name=call.function.name, decode_error=str(error))
    if not isinstance(arguments, dict):
        return ToolCall(
            id=call.id,
            name=call.function.name,
            decode_error="tool arguments must be a JSON object",
        )
    return ToolCall(id=call.id, name=call.function.name, arguments=arguments)
