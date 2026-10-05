"""Cross-platform "is another agent-started run still active" guard.

An OS advisory lock (``fcntl.flock`` on POSIX) does not survive into a
detached child process the same way on Windows: ``subprocess.Popen`` there has
no equivalent of ``pass_fds``, so a locked descriptor cannot be handed to the
child. Instead this module records the holding process's PID in the lock
file and treats "locked" as "that PID is still alive", which works
identically once the parent has exited and the child is the sole owner of the
run. A short-lived OS lock -- ``fcntl`` on POSIX, ``msvcrt`` on Windows --
gates the read-check-write around that PID, so two processes racing to claim
the file at the same instant cannot both succeed. :func:`gate` exposes that
lock to a caller whose decision to claim needs more than the PID, such as a
look at which experiments are still unfinished.

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import os
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

if os.name == "nt":
    import msvcrt
else:
    import fcntl

__all__ = ["pid_alive", "gate", "Gate", "try_claim", "record", "release"]

#: Permissions for a freshly created lock file: owner read/write only.
_LOCK_FILE_MODE = 0o600
#: Bytes locked/unlocked by the short same-process gate; the file holds
#: nothing but the holder's PID as ASCII text, so one byte is enough to
#: satisfy msvcrt's non-empty-region requirement on Windows.
_LOCK_REGION_BYTES = 1
#: Generous upper bound on a PID rendered as ASCII decimal text.
_MAX_PID_TEXT_BYTES = 64
#: How long :func:`gate` waits for another process to leave it. A holder may
#: scan the status files inside it, which is quick but not instantaneous.
_GATE_TIMEOUT_SECONDS = 60.0
#: Pause between attempts to enter a gate someone else holds.
_GATE_RETRY_SECONDS = 0.05


def pid_alive(pid: int) -> bool:
    """Report whether a process ID is currently running.

    :param pid: Process ID to probe.
    :return: ``True`` if the process exists (including when its liveness
        cannot be determined because it belongs to another user), ``False``
        otherwise.
    :rtype: bool
    """
    if os.name == "nt":
        import ctypes
        process_query_limited_information = 0x1000
        handle = ctypes.windll.kernel32.OpenProcess(
            process_query_limited_information, False, pid
        )
        if not handle:
            return False
        ctypes.windll.kernel32.CloseHandle(handle)
        return True
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _lock(fd: int) -> bool:
    """Try once to take the short exclusive lock on an open file descriptor."""
    if os.fstat(fd).st_size == 0:
        # msvcrt.locking needs a non-empty region to lock; pad with whitespace
        # so a fresh, unclaimed file never reads back as a "0" holder pid.
        os.write(fd, b" ")
    os.lseek(fd, 0, os.SEEK_SET)
    try:
        if os.name == "nt":
            msvcrt.locking(fd, msvcrt.LK_NBLCK, _LOCK_REGION_BYTES)
        else:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return False
    return True


def _unlock(fd: int) -> None:
    """Release the short exclusive lock taken by :func:`_lock`."""
    os.lseek(fd, 0, os.SEEK_SET)
    if os.name == "nt":
        msvcrt.locking(fd, msvcrt.LK_UNLCK, _LOCK_REGION_BYTES)
    else:
        fcntl.flock(fd, fcntl.LOCK_UN)


class Gate:
    """The run lock's holder PID, readable and writable while the gate is held."""

    def __init__(self, fd: int) -> None:
        self._fd = fd

    def holder(self) -> int | None:
        """Return the recorded holder's PID, or ``None`` when nobody holds it."""
        os.lseek(self._fd, 0, os.SEEK_SET)
        raw = os.read(self._fd, _MAX_PID_TEXT_BYTES).strip()
        return int(raw) if raw.isdigit() else None

    def held(self) -> bool:
        """Report whether a live process is recorded as the holder."""
        holder = self.holder()
        return holder is not None and pid_alive(holder)

    def set_holder(self, pid: int | None) -> None:
        """Record ``pid`` as the holder, or clear the lock with ``None``."""
        os.lseek(self._fd, 0, os.SEEK_SET)
        os.ftruncate(self._fd, 0)
        if pid is not None:
            os.write(self._fd, str(pid).encode("ascii"))


@contextmanager
def gate(lock_path: Path) -> Iterator[Gate]:
    """Hold the run lock's OS gate, waiting while another process holds it.

    Everything decided inside is atomic with respect to every other caller of
    this module, so a claim can rest on more than the recorded PID.

    :param lock_path: Lock file recording the current holder's PID.
    :raises TimeoutError: When the gate stays held for
        :data:`_GATE_TIMEOUT_SECONDS`.
    """
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, _LOCK_FILE_MODE)
    try:
        deadline = time.monotonic() + _GATE_TIMEOUT_SECONDS
        while not _lock(fd):
            if time.monotonic() >= deadline:
                raise TimeoutError(f"run lock {lock_path} stayed busy")
            time.sleep(_GATE_RETRY_SECONDS)
        try:
            yield Gate(fd)
        finally:
            _unlock(fd)
    finally:
        os.close(fd)


def try_claim(lock_path: Path, pid: int) -> bool:
    """Claim the run lock for ``pid`` unless a live process already holds it.

    :param lock_path: Lock file recording the current holder's PID.
    :param pid: PID to record as the new holder when the claim succeeds.
    :return: ``True`` if claimed, ``False`` if a live process already holds it.
    :rtype: bool
    """
    with gate(lock_path) as lock:
        if lock.held():
            return False
        lock.set_holder(pid)
        return True


def release(lock_path: Path) -> None:
    """Clear the run lock so a later claim does not wait on this holder.

    :param lock_path: Lock file to clear.
    """
    with gate(lock_path) as lock:
        lock.set_holder(None)


def record(lock_path: Path, pid: int) -> None:
    """Hand the run lock to ``pid``, e.g. once a detached child's real PID is known.

    :param lock_path: Lock file to update.
    :param pid: PID that should now be treated as the holder.
    """
    with gate(lock_path) as lock:
        lock.set_holder(pid)
