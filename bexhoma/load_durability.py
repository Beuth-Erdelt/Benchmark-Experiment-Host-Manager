"""
Import durability during the load (``-xld/--load-durability``).

The option sets the durability during the load only. The init script lists of
the cluster config (``volumes.<benchmark>.initscripts``) contain two
placeholders where the durability scripts run, like the index or constraint
scripts: ``durability.sql`` (first in every pre-load list) and
``restoredurability.sql`` (in every post-load list, right before the check
script). At loading start bexhoma replaces them with the scripts of the chosen
level that the DBMS folder has; a list without a placeholder gets none. The
restore scripts return the server to its configured state (template and
``--set``), so the benchmark is not affected.

- ``durable``: the load runs crash-safe, e.g. PostgreSQL
  ``synchronous_commit``/``fsync``/``full_page_writes`` on, MySQL/MariaDB
  flush at every commit (MariaDB also doublewrite on).
- ``relaxed`` (default): e.g. PostgreSQL ``synchronous_commit=off``,
  MySQL ``innodb_flush_log_at_trx_commit``, key checks off.
- ``unsafe``: the relaxed scripts plus e.g. MySQL redo log off, PostgreSQL
  ``fsync=off``; a crash during the load can corrupt data.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import os

__all__ = ["LEVELS", "DEFAULT_LEVEL", "PLACEHOLDERS", "expand_durability_placeholders"]

#: Levels of ``-xld/--load-durability``.
LEVELS = ('durable', 'relaxed', 'unsafe')

#: CLI default: the relaxations the load always had, so results stay comparable.
DEFAULT_LEVEL = 'relaxed'

#: Placeholder in the init script lists -> level -> scripts, in execution order.
#: Shell scripts run in the SUT container (e.g. MariaDB as root, PostgreSQL sync).
PLACEHOLDERS = {
    'durability.sql': {
        'durable': ['durability-durable.sql', 'durability-durable.sh'],
        'relaxed': ['durability-relaxed.sql', 'durability-relaxed.sh'],
        'unsafe': ['durability-relaxed.sql', 'durability-relaxed.sh',
                   'durability-unsafe.sql', 'durability-unsafe.sh'],
    },
    'restoredurability.sql': {
        'durable': ['restoredurability-durable.sql', 'restoredurability-durable.sh'],
        'relaxed': ['restoredurability-relaxed.sql', 'restoredurability-relaxed.sh'],
        'unsafe': ['restoredurability-unsafe.sql', 'restoredurability-unsafe.sh',
                   'restoredurability-relaxed.sql', 'restoredurability-relaxed.sh'],
    },
}


def expand_durability_placeholders(scripts: list, level: str, folder: str) -> list:
    """Replace the placeholders of a script list by the level's scripts the folder has.

    :param scripts: Init script list from the cluster config (not changed).
    :param level: One of :data:`LEVELS`.
    :param folder: The configuration's DBMS script folder (e.g. ``experiments/tpch/MySQL``).
    :return: The list with every placeholder replaced (possibly by nothing).
    :rtype: list
    """
    expanded = []
    for script in scripts:
        if script in PLACEHOLDERS:
            expanded.extend(s for s in PLACEHOLDERS[script][level]
                            if os.path.isfile(os.path.join(folder, s)))
        else:
            expanded.append(script)
    return expanded
