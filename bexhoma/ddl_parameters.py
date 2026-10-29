"""
DDL parameters: placeholders in the scripts of an experiment folder.

A DBMS folder (``experiments/<benchmark>/<dbms>``) may declare parameters in
``ddl-parameters.config``, a Python dict literal::

    {
        'num_worker_shards': {
            'default': 32,
            'type': 'int',
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
need characters a token may not have. ``type: 'int'`` (optional) normalises
values (``032`` is ``32``). ``requires`` (optional, ``{'other_key': [values]}``)
restricts other keys while this key is not at its default. Scripts of the folder name a parameter as
``{key}``; any other text in braces (JSON, ClickHouse macros) is kept.

Values are tokens that are valid Kubernetes label values, because the values
a volume was loaded with are stored as its labels (``ddl_<key>``, see
:func:`volume_labels`); a reused volume brings them along
(:func:`compare_with_volume`). Keys are valid label names with the prefix.

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
import itertools
import os
import re

__all__ = ["FILENAME", "LABEL_PREFIX", "load_declarations", "parse_assignments", "combinations",
           "normalize", "validate", "check_requirements", "resolve", "fill_values", "fill", "is_label_value",
           "volume_labels", "compare_with_volume"]

#: Name of the declaration file in a DBMS script folder.
FILENAME = 'ddl-parameters.config'

#: Prefix of the volume labels that hold the DDL values.
LABEL_PREFIX = 'ddl_'

#: A value: a valid Kubernetes label value (it is stored as one), never empty.
_TOKEN = re.compile(r'^[A-Za-z0-9]([A-Za-z0-9_.-]{0,61}[A-Za-z0-9])?$')

#: A declared key: a placeholder name that is a valid label name after LABEL_PREFIX.
_KEY = re.compile(r'^[A-Za-z]([A-Za-z0-9_]{0,57}[A-Za-z0-9])?$')

#: A placeholder in a script.
_PLACEHOLDER = re.compile(r'\{([A-Za-z_][A-Za-z0-9_]*)\}')


def is_label_value(value) -> bool:
    """Whether a value can be stored as a Kubernetes label value (and given as a token).

    :param value: The value.
    :return: True for 1-63 characters ``[A-Za-z0-9_.-]``, first and last alphanumeric.
    :rtype: bool
    """
    return bool(_TOKEN.match(str(value)))


def load_declarations(experiments_folder: str, docker_path: str) -> dict:
    """Read and check the declarations of a configuration's script folder.

    A folder variant (``Citus/distributed``) without its own file uses the
    file of the parent folder (``Citus``). Defaults and allowed values are
    returned as strings, the form they have as labels.

    :param experiments_folder: The benchmark's folder (e.g. ``experiments/tpch``).
    :param docker_path: The configuration's ``path_experiment_docker``.
    :return: Declarations per key, empty when there is no file.
    :rtype: dict
    :raises ValueError: On a key, default or allowed value that would not be a
        valid label, a value that is not a string or an int, or an unknown type.
    """
    path = docker_path.strip('/')
    while path:
        filename = os.path.join(experiments_folder, path, FILENAME)
        if os.path.isfile(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                declarations = ast.literal_eval(f.read())
            checked = {key: _checked(filename, key, declaration) for key, declaration in declarations.items()}
            for key, declaration in checked.items():
                for other, allowed in (declaration.get('requires') or {}).items():
                    if other not in checked or not isinstance(allowed, list):
                        raise ValueError(f"{filename}: '{key}' requires '{other}', which must be a declared key "
                                         f"with a list of values")
            return checked
        path = os.path.dirname(path)
    return {}


def _checked(filename: str, key: str, declaration) -> dict:
    """One declaration with its values as canonical strings, or an error naming the file and key."""
    if not isinstance(declaration, dict) or 'default' not in declaration:
        raise ValueError(f"{filename}: '{key}' needs a dict with a 'default'")
    if not _KEY.match(key):
        raise ValueError(f"{filename}: key '{key}' must match {_KEY.pattern} (a label name after '{LABEL_PREFIX}')")
    if declaration.get('type', 'token') not in ('token', 'int'):
        raise ValueError(f"{filename}: '{key}' has type {declaration['type']!r}, expected 'token' or 'int'")
    checked = dict(declaration)
    for name, values in (('default', [declaration['default']]), ('values', declaration.get('values') or [])):
        for value in values:
            # bool is an int in Python: refuse it explicitly
            if isinstance(value, bool) or not isinstance(value, (str, int)):
                raise ValueError(f"{filename}: '{key}' {name} {value!r} must be a string or an int")
            if not is_label_value(normalize(checked, value)):
                raise ValueError(f"{filename}: '{key}' {name} {value!r} is not a valid label value; "
                                 f"use a token and map it in 'sql'")
    checked['default'] = normalize(checked, declaration['default'])
    if 'values' in declaration:
        checked['values'] = [normalize(checked, value) for value in declaration['values']]
    return checked


def parse_assignments(entries: list) -> dict:
    """Parse ``-xddl`` entries ``KEY=V1[,V2...]`` into one value list per key.

    :param entries: The ``-xddl`` values (the flag may be repeated).
    :return: Values per key, in the given order.
    :rtype: dict[str, list[str]]
    :raises ValueError: On an entry that is not ``KEY=VALUE``, or a value that
        is not a valid label value (1-63 characters ``[A-Za-z0-9_.-]``, first
        and last alphanumeric).
    """
    assignments = {}
    for entry in entries or []:
        key, separator, text = entry.partition('=')
        key = key.strip()
        values = [value.strip() for value in text.split(',')]
        if not separator or not key or not all(values):
            raise ValueError(f"-xddl {entry!r} must be KEY=VALUE or KEY=V1,V2")
        bad = [value for value in values if not is_label_value(value)]
        if bad:
            raise ValueError(f"-xddl {entry!r}: value(s) {bad} must be 1-63 characters of letters, digits "
                             f"and _.- starting and ending with a letter or digit")
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


def normalize(declaration: dict, value) -> str:
    """The canonical string of a value: ``int`` types without sign or leading zeros.

    :param declaration: The key's declaration.
    :param value: A value as given or declared.
    :return: The value as it is compared, filled and stored.
    :rtype: str
    :raises ValueError: For an ``int`` type and a value that is no integer.
    """
    if declaration.get('type') == 'int':
        try:
            return str(int(str(value)))
        except ValueError:
            raise ValueError(f"{value!r} is not an integer") from None
    return str(value)


def validate(declarations: dict, given: dict, where: str) -> dict:
    """Check given values against the declarations of one folder and normalise them.

    :param declarations: From :func:`load_declarations`.
    :param given: Values (or value lists) per key, only keys the folder declares.
    :param where: Name for the error message (configuration or folder).
    :return: The given values, normalised, in the same shape.
    :rtype: dict
    :raises ValueError: On a value that is not one of the declared ``values``
        (exact spelling) or not an integer for an ``int`` type.
    """
    checked = {}
    for key, values in given.items():
        declaration = declarations[key]
        normalized = []
        for value in values if isinstance(values, list) else [values]:
            try:
                value = normalize(declaration, value)
            except ValueError as error:
                raise ValueError(f"{where}: {key}={value}: {error}") from None
            if 'values' in declaration and value not in declaration['values']:
                raise ValueError(f"{where}: {key}={value} is not one of {declaration['values']}")
            normalized.append(value)
        checked[key] = normalized if isinstance(values, list) else normalized[0]
    return checked


def check_requirements(declarations: dict, values: dict, where: str) -> None:
    """Check that keys away from their default have what they require of other keys.

    A declaration may hold ``'requires': {'other_key': ['allowed', ...]}``:
    when the key's value is not its default, ``other_key`` must have one of
    the allowed values (e.g. TiDB ``split_regions`` needs a clustered key,
    YugabyteDB ``num_tablets`` needs hash sharding).

    :param declarations: From :func:`load_declarations`.
    :param values: Effective values of one configuration (or one sweep combination).
    :param where: Name for the error message.
    :raises ValueError: When a requirement is not met.
    """
    for key, declaration in declarations.items():
        if str(values.get(key, declaration['default'])) == str(declaration['default']):
            continue
        for other, allowed in (declaration.get('requires') or {}).items():
            other_value = str(values.get(other, declarations.get(other, {}).get('default')))
            if other_value not in [str(value) for value in allowed]:
                raise ValueError(f"{where}: {key}={values[key]} requires {other} in {list(allowed)}, "
                                 f"not {other}={other_value}")


def resolve(declarations: dict, given: dict) -> dict:
    """The effective values of a folder: the defaults, overwritten by the given ones.

    :param declarations: From :func:`load_declarations`.
    :param given: Single values per key; keys the folder does not declare are ignored.
    :return: One value (canonical string) per declared key.
    :rtype: dict[str, str]
    """
    return {key: normalize(declaration, given.get(key, declaration['default']))
            for key, declaration in declarations.items()}


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


def volume_labels(values: dict, prefix: str = LABEL_PREFIX) -> dict:
    """Labels that store values on a volume, one per key.

    :param values: Values per key (canonical strings).
    :param prefix: Label name prefix (``ddl_`` for DDL values).
    :return: Label name to value; values that are no valid label value are left out.
    :rtype: dict[str, str]
    """
    return {prefix + key: str(value) for key, value in values.items() if is_label_value(value)}


def compare_with_volume(requested: dict, given: set, labels: dict, defaults: dict,
                        prefix: str = LABEL_PREFIX) -> tuple:
    """Compare the requested values with those a reused volume was loaded with.

    The volume's values win: they describe the data. A key the volume has no
    label for (loaded before the key or the labels existed) keeps its
    default, marked as assumed.

    :param requested: Effective values the configuration would load with.
    :param given: Keys whose value was given explicitly (not a default).
    :param labels: All labels of the volume.
    :param defaults: Value assumed for a key the volume has no label for.
    :param prefix: Label name prefix of these values.
    :return: ``(effective, report)``: the values of the run, and a dict with
        ``from_volume`` (key: value), ``differences`` (key: [requested, volume],
        given keys only), ``matching`` (given keys equal to the volume's),
        ``assumed`` (keys without label) and ``unknown`` (labels of keys not requested).
    :rtype: tuple[dict, dict]
    """
    effective = {}
    report = {'from_volume': {}, 'differences': {}, 'matching': [], 'assumed': [], 'unknown': []}
    for key, value in requested.items():
        label = prefix + key
        if label not in labels:
            effective[key] = str(defaults.get(key, value))
            report['assumed'].append(key)
            continue
        volume_value = str(labels[label])
        effective[key] = volume_value
        report['from_volume'][key] = volume_value
        if key in given:
            if volume_value == str(value):
                report['matching'].append(key)
            else:
                report['differences'][key] = [str(value), volume_value]
    report['unknown'] = sorted(label[len(prefix):] for label in labels
                               if label.startswith(prefix) and label[len(prefix):] not in requested)
    return effective, report
