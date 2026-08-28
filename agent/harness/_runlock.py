"""Cross-platform "is another agent-started run still active" guard.

An OS advisory lock (``fcntl.flock`` on POSIX) does not survive into a
detached child process the same way on Windows: ``subprocess.Popen`` there has
no equivalent of ``pass_fds``, so a locked descriptor cannot be handed to the
child. Instead this module records the holding process's PID in the lock
file and treats "locked" as "that PID is still alive", which works
identically once the parent has exited and the child is the sole owner of the
run. A short-lived, same-process OS lock -- ``fcntl`` on POSIX, ``msvcrt`` on
Windows -- brackets only the read-check-write around that PID, so two
processes racing to claim the file at the same instant cannot both succeed.

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import os
from pathlib import Path

if os.name == "nt":
    import msvcrt
else:
    import fcntl

__all__ = ["pid_alive", "try_claim", "record", "release"]

#: Permissions for a freshly created lock file: owner read/write only.
_LOCK_FILE_MODE = 0o600
#: Bytes locked/unlocked by the short same-process gate; the file holds
#: nothing but the holder's PID as ASCII text, so one byte is enough to
#: satisfy msvcrt's non-empty-region requirement on Windows.
_LOCK_REGION_BYTES = 1
#: Generous upper bound on a PID rendered as ASCII decimal text.
_MAX_PID_TEXT_BYTES = 64


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
    """Take a short, same-process exclusive lock on an open file descriptor."""
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
    """Release the short, same-process exclusive lock taken by :func:`_lock`."""
    os.lseek(fd, 0, os.SEEK_SET)
    if os.name == "nt":
        msvcrt.locking(fd, msvcrt.LK_UNLCK, _LOCK_REGION_BYTES)
    else:
        fcntl.flock(fd, fcntl.LOCK_UN)


def try_claim(lock_path: Path, pid: int) -> bool:
    """Claim the run lock for ``pid`` unless a live process already holds it.

    :param lock_path: Lock file recording the current holder's PID.
    :param pid: PID to record as the new holder when the claim succeeds.
    :return: ``True`` if claimed, ``False`` if a live process already holds it.
    :rtype: bool
    """
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, _LOCK_FILE_MODE)
    try:
        if not _lock(fd):
            return False
        try:
            os.lseek(fd, 0, os.SEEK_SET)
            raw = os.read(fd, _MAX_PID_TEXT_BYTES).strip()
            holder = int(raw) if raw.isdigit() else None
            if holder is not None and pid_alive(holder):
                return False
            os.lseek(fd, 0, os.SEEK_SET)
            os.ftruncate(fd, 0)
            os.write(fd, str(pid).encode("ascii"))
            return True
        finally:
            _unlock(fd)
    finally:
        os.close(fd)


def release(lock_path: Path) -> None:
    """Clear the run lock so a later claim does not wait on this holder.

    :param lock_path: Lock file to clear.
    """
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, _LOCK_FILE_MODE)
    try:
        if _lock(fd):
            try:
                os.lseek(fd, 0, os.SEEK_SET)
                os.ftruncate(fd, 0)
            finally:
                _unlock(fd)
    finally:
        os.close(fd)


def record(lock_path: Path, pid: int) -> None:
    """Hand the run lock to ``pid``, e.g. once a detached child's real PID is known.

    :param lock_path: Lock file to update.
    :param pid: PID that should now be treated as the holder.
    """
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, _LOCK_FILE_MODE)
    try:
        if _lock(fd):
            try:
                os.lseek(fd, 0, os.SEEK_SET)
                os.ftruncate(fd, 0)
                os.write(fd, str(pid).encode("ascii"))
            finally:
                _unlock(fd)
    finally:
        os.close(fd)
