"""
DDL parameters: placeholders in the scripts of an experiment folder.

A DBMS folder (``experiments/<benchmark>/<dbms>``) may declare parameters in
``ddl-parameters.config``, a Python dict literal::

    {
        'num_worker_shards': {
            'default': 32,
            'description': 'citus.shard_count of the distributed tables',
        },
        'pk_sharding': {
            'default': 'hash',
            'values': ['hash', 'asc'],
            'sql': {'hash': 'HASH', 'asc': 'ASC'},
            'description': 'sharding of the primary key',
        },
    }

``default`` is the value that reproduces the script as it was before the
parameter existed. ``values`` (optional) lists the allowed tokens, ``sql``
(optional) maps a token to the text written into the script, for values that
need characters a token may not have. Scripts of the folder name a parameter
as ``{key}``; any other text in braces (JSON, ClickHouse macros) is kept.

Values come from ``-xddl KEY=VALUE`` (a comma list sweeps the key, see
:meth:`bexhoma.experiments.base.ExperimentBase.expand_resource_cells`) and
from ``-nwr``/``-nws`` (``num_worker_replicas``/``num_worker_shards``). A
folder without the file gets no filling; its scripts are uploaded unchanged.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import hashlib
import itertools
import os
import re

__all__ = ["FILENAME", "load_declarations", "parse_assignments", "combinations",
           "validate", "resolve", "fill_values", "fill", "non_default", "storage_suffix"]

#: Name of the declaration file in a DBMS script folder.
FILENAME = 'ddl-parameters.config'

#: A value as given on the command line: written into SQL, so no quotes or spaces.
_TOKEN = re.compile(r'^[A-Za-z0-9_.+-]+$')

#: A placeholder in a script.
_PLACEHOLDER = re.compile(r'\{([A-Za-z_][A-Za-z0-9_]*)\}')


def load_declarations(experiments_folder: str, docker_path: str) -> dict:
    """Read the declarations of a configuration's script folder.

    A folder variant (``Citus/distributed``) without its own file uses the
    file of the parent folder (``Citus``).

    :param experiments_folder: The benchmark's folder (e.g. ``experiments/tpch``).
    :param docker_path: The configuration's ``path_experiment_docker``.
    :return: Declarations per key, empty when there is no file.
    :rtype: dict
    :raises ValueError: When the file is not a dict of dicts with a ``default``.
    """
    path = docker_path.strip('/')
    while path:
        filename = os.path.join(experiments_folder, path, FILENAME)
        if os.path.isfile(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                declarations = ast.literal_eval(f.read())
            for key, declaration in declarations.items():
                if not isinstance(declaration, dict) or 'default' not in declaration:
                    raise ValueError(f"{filename}: '{key}' needs a dict with a 'default'")
            return declarations
        path = os.path.dirname(path)
    return {}


def parse_assignments(entries: list) -> dict:
    """Parse ``-xddl`` entries ``KEY=V1[,V2...]`` into one value list per key.

    :param entries: The ``-xddl`` values (the flag may be repeated).
    :return: Values per key, in the given order.
    :rtype: dict[str, list[str]]
    :raises ValueError: On an entry that is not ``KEY=VALUE``, an empty value or
        a value with other characters than letters, digits and ``_.+-``.
    """
    assignments = {}
    for entry in entries or []:
        key, separator, text = entry.partition('=')
        key = key.strip()
        values = [value.strip() for value in text.split(',')]
        if not separator or not key or not all(values):
            raise ValueError(f"-xddl {entry!r} must be KEY=VALUE or KEY=V1,V2")
        bad = [value for value in values if not _TOKEN.match(value)]
        if bad:
            raise ValueError(f"-xddl {entry!r}: value(s) {bad} may only have letters, digits and _.+-")
        assignments[key] = values
    return assignments


def combinations(swept: dict) -> list:
    """All combinations of the swept keys, the first key changing slowest.

    :param swept: Values per key.
    :return: One dict per combination; ``[{}]`` when nothing is swept.
    :rtype: list[dict]
    """
    keys = list(swept)
    return [dict(zip(keys, values)) for values in itertools.product(*(swept[key] for key in keys))]


def validate(declarations: dict, given: dict, where: str) -> None:
    """Check given values against the declarations of one folder.

    :param declarations: From :func:`load_declarations`.
    :param given: Values (or value lists) per key, only keys the folder declares.
    :param where: Name for the error message (configuration or folder).
    :raises ValueError: On a value that is not one of the declared ``values``.
    """
    for key, values in given.items():
        allowed = declarations[key].get('values')
        if allowed is None:
            continue
        allowed = [str(value) for value in allowed]
        for value in values if isinstance(values, list) else [values]:
            if str(value) not in allowed:
                raise ValueError(f"{where}: {key}={value} is not one of {allowed}")


def resolve(declarations: dict, given: dict) -> dict:
    """The effective values of a folder: the defaults, overwritten by the given ones.

    :param declarations: From :func:`load_declarations`.
    :param given: Single values per key; keys the folder does not declare are ignored.
    :return: One value per declared key.
    :rtype: dict
    """
    return {key: given.get(key, declaration['default']) for key, declaration in declarations.items()}


def fill_values(declarations: dict, values: dict) -> dict:
    """The text written for each placeholder (``sql`` mapping applied).

    :param declarations: From :func:`load_declarations`.
    :param values: Effective values, from :func:`resolve`.
    :return: Text per key.
    :rtype: dict[str, str]
    """
    return {key: str(declarations.get(key, {}).get('sql', {}).get(str(value), value))
            for key, value in values.items()}


def fill(text: str, values: dict) -> str:
    """Replace ``{key}`` for every key in ``values``; other braces stay.

    :param text: Script text.
    :param values: Text per key.
    :return: The filled script.
    :rtype: str
    """
    return _PLACEHOLDER.sub(
        lambda match: str(values[match.group(1)]) if match.group(1) in values else match.group(0), text)


def non_default(declarations: dict, values: dict) -> dict:
    """The effective values that differ from the declared defaults.

    :param declarations: From :func:`load_declarations`.
    :param values: Effective values, from :func:`resolve`.
    :return: The differing values, in declaration order.
    :rtype: dict
    """
    return {key: value for key, value in values.items()
            if str(value) != str(declarations[key]['default'])}


def storage_suffix(declarations: dict, values: dict) -> str:
    """Part of the volume name that tells data loaded with other DDL values apart.

    A volume is found again by name alone (``-rst``), so data loaded with
    other DDL values must not be found under the same name. Defaults add
    nothing, so volumes of runs without ``-xddl`` keep their names.

    :param declarations: From :func:`load_declarations`.
    :param values: Effective values, from :func:`resolve`.
    :return: ``''`` or ``'ddl'`` followed by 6 hex digits.
    :rtype: str
    """
    changed = non_default(declarations, values)
    if not changed:
        return ''
    text = ';'.join(f'{key}={changed[key]}' for key in sorted(changed))
    return 'ddl' + hashlib.sha1(text.encode('utf-8')).hexdigest()[:6]
