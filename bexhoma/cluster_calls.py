"""Bookkeeping and token caching for calls to the Kubernetes cluster.

:class:`CallStats` counts and times kubectl subprocesses and Kubernetes API
requests, so a step can report what it cost (e.g. ``submitted benchmarker job
in 44.1s (23 kubectl calls 38.2s, 40 API requests 3.1s)``).

:class:`ThrottledTokenRefresh` wraps the Python client's token refresh hook.
For a kubeconfig whose user gets its token from an exec plugin, the client
runs the plugin before every request while it considers the token expired,
which it does from 5 minutes before ``expirationTimestamp`` on. Tokens that
live about 5 minutes (OIDC) are therefore "expired" as soon as they are
issued, and every request pays for a plugin process (about 0.5 s from the
Windows host instead of 0.08 s).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import base64
import json
import threading
import time
from typing import Any, Callable, Optional

__all__ = [
    'CALL_STATS', 'CallStats', 'ThrottledTokenRefresh', 'token_expiry', 'stored_pods',
    'TOKEN_REFRESH_SECONDS', 'TOKEN_EXPIRY_MARGIN_SECONDS',
]

#: The token refresh hook is passed on at most this often; a token is then at
#: most this old. OIDC tokens of the cluster live about 5 minutes.
TOKEN_REFRESH_SECONDS = 60

#: A token whose expiry (``exp`` claim of a JWT) is closer than this is
#: refreshed at once, whatever its age.
TOKEN_EXPIRY_MARGIN_SECONDS = 30


class CallStats:
    """Thread-safe counters of kubectl subprocesses and API requests.

    The counters are global; a step reads :meth:`snapshot` at its start and
    :meth:`since` at its end. Calls made by other threads meanwhile (e.g. a
    metric fetch batch) are counted too.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.kubectl_calls = 0
        self.kubectl_seconds = 0.0
        self.api_calls = 0
        self.api_seconds = 0.0

    def record_kubectl(self, seconds: float) -> None:
        """Count one kubectl subprocess that took ``seconds``."""
        with self._lock:
            self.kubectl_calls += 1
            self.kubectl_seconds += seconds

    def record_api(self, seconds: float) -> None:
        """Count one Kubernetes API request (or exec stream) that took ``seconds``."""
        with self._lock:
            self.api_calls += 1
            self.api_seconds += seconds

    def snapshot(self) -> tuple:
        """Current counters, to pass to :meth:`since` later.

        :return: ``(kubectl_calls, kubectl_seconds, api_calls, api_seconds)``.
        """
        with self._lock:
            return (self.kubectl_calls, self.kubectl_seconds, self.api_calls, self.api_seconds)

    def since(self, snapshot: tuple) -> str:
        """Describe the calls made since ``snapshot``.

        :param snapshot: Value of :meth:`snapshot` taken earlier.
        :return: E.g. ``23 kubectl calls 38.2s, 40 API requests 3.1s``.
        """
        kubectl_calls, kubectl_seconds, api_calls, api_seconds = self.snapshot()
        return "{} kubectl calls {:.1f}s, {} API requests {:.1f}s".format(
            kubectl_calls - snapshot[0], kubectl_seconds - snapshot[1],
            api_calls - snapshot[2], api_seconds - snapshot[3])


#: Counters of this process.
CALL_STATS = CallStats()


def stored_pods(cluster: Any) -> set:
    """Names of finished pods whose logs and description are stored, per cluster object.

    A finished pod does not change any more (a failed pod is replaced by a pod
    with a new name), so once all its files exist it need not be inspected
    again. Callers add a pod only after checking that every file exists.

    :param cluster: The cluster object the pods belong to.
    :return: The (mutable) set kept on that object.
    """
    return cluster.__dict__.setdefault('_stored_pods', set())


def token_expiry(authorization: Optional[str]) -> Optional[float]:
    """Return the expiry of a bearer token if it is a JWT, else ``None``.

    Reads the ``exp`` claim without verifying the signature: it only decides
    when to ask the plugin again, the API server still checks the token.

    :param authorization: Value of the ``authorization`` api key, e.g. ``Bearer eyJ...``.
    :return: Expiry as a Unix timestamp, or ``None`` if unknown.
    """
    if not authorization:
        return None
    token = authorization.split(' ', 1)[-1]
    parts = token.split('.')
    if len(parts) != 3:
        return None
    try:
        payload = parts[1] + '=' * (-len(parts[1]) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload.encode('ascii')))
        expiry = claims.get('exp')
        return float(expiry) if expiry is not None else None
    except (ValueError, TypeError, UnicodeError, AttributeError):
        return None


class ThrottledTokenRefresh:
    """Pass the client's token refresh hook on only when the token may be stale.

    The wrapped hook (the client's own) runs the exec plugin when it considers
    the token expired. It is passed on when the last pass-on is older than
    :data:`TOKEN_REFRESH_SECONDS`, or when the token's own expiry (if it is a
    JWT) is closer than :data:`TOKEN_EXPIRY_MARGIN_SECONDS`. A token rejected
    anyway (401) is renewed by the callers' ``ApiException`` handling, which
    rebuilds the clients via ``cluster_access()``.

    :param hook: The client's ``refresh_api_key_hook``.
    :param clock: Time source (seconds), for tests.
    """

    def __init__(self, hook: Callable[[Any], None], clock: Callable[[], float] = time.time) -> None:
        self._hook = hook
        self._clock = clock
        self._lock = threading.Lock()
        self._refreshed_at: Optional[float] = None

    def _is_stale(self, configuration: Any, now: float) -> bool:
        if self._refreshed_at is None or now - self._refreshed_at >= TOKEN_REFRESH_SECONDS:
            return True
        expiry = token_expiry(getattr(configuration, 'api_key', {}).get('authorization'))
        return expiry is not None and expiry - now < TOKEN_EXPIRY_MARGIN_SECONDS

    def __call__(self, configuration: Any) -> None:
        with self._lock:
            now = self._clock()
            if not self._is_stale(configuration, now):
                return
            self._hook(configuration)
            self._refreshed_at = now
            # the client's hook registers itself again when it reloads the
            # token (kube_config._set_config()); keep the throttle in front
            current = getattr(configuration, 'refresh_api_key_hook', None)
            if current is not None and current is not self:
                self._hook = current
                configuration.refresh_api_key_hook = self
