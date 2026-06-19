"""DBMS configuration subpackage for bexhoma.

Provides :class:`SutConfiguration` (the primary configuration class) together
with helper classes that implement specialised subsystems via composition.

The module-level name ``default`` is kept as an alias so that any code that
still imports ``from bexhoma.configurations import default`` continues to work
without changes.

The module-level YAML helpers and the ``load_data_asynch`` thread function are
re-exported from :mod:`~.manifest` and :mod:`~.loading` respectively.
"""
from .base import SutConfiguration
from .benchmarking import BenchmarkRunner
from .host import HostProbe
from .lifecycle import LifecycleManager
from .loading import LoadingCoordinator, load_data_asynch
from .manifest import ManifestBuilder, ensure_arg_pairs, find_workloads, patch_container
from .metrics import MetricsCollector
from .status import ComponentStatus

#: Backward-compatibility alias — new code should use :class:`SutConfiguration`.
default = SutConfiguration

__all__ = [
    'SutConfiguration',
    'default',
    'ComponentStatus',
    'HostProbe',
    'LifecycleManager',
    'LoadingCoordinator',
    'BenchmarkRunner',
    'MetricsCollector',
    'ManifestBuilder',
    'find_workloads',
    'ensure_arg_pairs',
    'patch_container',
    'load_data_asynch',
]
