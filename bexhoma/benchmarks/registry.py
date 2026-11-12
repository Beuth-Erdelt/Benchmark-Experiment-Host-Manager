"""
Registry of the benchmarks bexhoma knows.

Generic code never names a benchmark. Where it has to pick something that
belongs to one (the experiment class that ``bexhoma summary`` rebuilds, the
collector of a benchmark run, the argument builder of a catalog workload, the
entry script), it asks this registry, and each benchmark answers with its
:class:`BenchmarkDescriptor`.

Lookups:

* :func:`descriptor_of` by the benchmark's canonical name,
* :func:`descriptor_for_type` by a name a result folder uses for it,
* :func:`descriptors` for all of them.

The descriptors are loaded on the first lookup, not on import, so this module
can be imported from anywhere in the package without an import cycle.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any, Callable, Optional

__all__ = ["BenchmarkDescriptor", "register", "descriptors", "descriptor_of", "descriptor_for_type"]

#: The module that registers the descriptors.
_DESCRIPTOR_MODULES = ("bexhoma.benchmarks.registered",)


@dataclass(frozen=True)
class BenchmarkDescriptor:
    """
    What generic code needs to know about one benchmark.

    :param name: Canonical name. It is the name of the benchmark's asset folder
        ``experiments/<name>/`` and of a workload in the catalog.
    :param types: Names a result folder uses for the benchmark: the workload
        ``type`` in ``queries.config`` and the ``type`` of its entries in
        ``benchmark_sequence``. Unique across all benchmarks.
    :param experiment: Experiment class that ``bexhoma summary`` rebuilds for a
        result folder of one of ``types``. ``None``: the generic base class.
    :param collector: Collector class for a benchmark run of one of ``types``.
        ``None``: the benchmark has no collector.
    :param entry_script: File name of the entry script in the repository root.
    :param argv_builder: ``(catalog, experiment) -> argv`` for a catalog workload
        of this ``name``. ``None``: the benchmark cannot be run from the catalog.
    """
    name: str
    types: tuple = ()
    experiment: Optional[type] = None
    collector: Optional[type] = None
    entry_script: str = ''
    argv_builder: Optional[Callable[[dict, dict], list]] = None


_BY_NAME: dict[str, BenchmarkDescriptor] = {}
_BY_TYPE: dict[str, BenchmarkDescriptor] = {}
_state = {'loaded': False, 'loading': False}


def register(descriptor: BenchmarkDescriptor) -> BenchmarkDescriptor:
    """
    Add a benchmark's descriptor.

    :param descriptor: The descriptor.
    :return: The descriptor, so a module can keep it as its ``DESCRIPTOR``.
    :raises ValueError: When the name or one of the types is already taken.
    """
    if descriptor.name in _BY_NAME:
        raise ValueError(f"benchmark {descriptor.name!r} is registered twice")
    for type_name in descriptor.types:
        if type_name in _BY_TYPE:
            raise ValueError(f"type {type_name!r} of benchmark {descriptor.name!r} "
                             f"already belongs to {_BY_TYPE[type_name].name!r}")
    _BY_NAME[descriptor.name] = descriptor
    for type_name in descriptor.types:
        _BY_TYPE[type_name] = descriptor
    return descriptor


def _load() -> None:
    """Import the modules that register the descriptors, once. A failing import is raised, not skipped."""
    if _state['loaded'] or _state['loading']:
        return
    _state['loading'] = True
    try:
        for module in _DESCRIPTOR_MODULES:
            importlib.import_module(module)
        _state['loaded'] = True
    finally:
        _state['loading'] = False


def descriptors() -> tuple:
    """
    All registered descriptors, in registration order.

    :rtype: tuple[BenchmarkDescriptor, ...]
    """
    _load()
    return tuple(_BY_NAME.values())


def descriptor_of(name: Any) -> Optional[BenchmarkDescriptor]:
    """
    The descriptor of the benchmark with this canonical name.

    :param name: Canonical name, e.g. the ``workload.name`` of an experiment spec.
    :return: The descriptor, or ``None`` when no such benchmark is registered.
    """
    _load()
    return _BY_NAME.get(name) if isinstance(name, str) else None


def descriptor_for_type(type_name: Any) -> Optional[BenchmarkDescriptor]:
    """
    The descriptor of the benchmark a result folder refers to by this name.

    :param type_name: Workload ``type`` of ``queries.config`` or ``type`` of a
        ``benchmark_sequence`` entry.
    :return: The descriptor, or ``None`` when no benchmark uses that name.
    """
    _load()
    return _BY_TYPE.get(type_name) if isinstance(type_name, str) else None
