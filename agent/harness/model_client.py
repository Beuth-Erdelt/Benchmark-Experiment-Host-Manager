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
from dataclasses import dataclass, field
from typing import Any

from openai import OpenAI

__all__ = ["ToolCall", "Reply", "ChatModel"]

#: vLLM does not check credentials, but the OpenAI client insists on a key.
_PLACEHOLDER_API_KEY = "EMPTY"


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
    """
    text: str
    reasoning: str
    tool_calls: list[ToolCall]
    message: dict[str, Any]
    usage: dict[str, int]


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
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout)

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
        """
        request: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if tools:
            request["tools"] = tools
        response = self._client.chat.completions.create(**request)
        message = response.choices[0].message
        replayed = message.model_dump(exclude_none=True)
        # A reasoning model returns its thinking in a separate field. Qwen's own
        # guidance is not to feed previous thinking back in, and some servers
        # reject the field on input, so it is logged but not replayed.
        # vLLM 0.27 renamed ``reasoning_content`` to ``reasoning``. Remove both
        # spellings so hidden thinking is never replayed into the next request.
        reasoning = replayed.pop("reasoning", None)
        legacy_reasoning = replayed.pop("reasoning_content", None)
        reasoning = reasoning or legacy_reasoning
        return Reply(
            text=message.content or "",
            reasoning=reasoning or "",
            tool_calls=[_parse_tool_call(call) for call in (message.tool_calls or [])],
            message=replayed,
            usage=response.usage.model_dump() if response.usage else {},
        )


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
