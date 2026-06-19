"""
Public API of the bexhoma.experiments package.

Exports :class:`ExperimentBase`, :class:`MixedExperiment`,
:class:`DbmsBenchmarkerExperiment`, :class:`TpchExperiment`,
:class:`TpcdsExperiment`, :class:`BenchbaseExperiment`,
:class:`TpccExperiment`, and :class:`YcsbExperiment` experiment classes.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import ExperimentBase
from .mixed import MixedExperiment
from .dbmsbenchmarker import DbmsBenchmarkerExperiment
from .tpch import TpchExperiment
from .tpcds import TpcdsExperiment
from .benchbase import BenchbaseExperiment
from .tpcc import TpccExperiment
from .ycsb import YcsbExperiment

# backward-compat aliases
base = ExperimentBase
mixed = MixedExperiment
dbmsbenchmarker = DbmsBenchmarkerExperiment
tpch = TpchExperiment
tpcds = TpcdsExperiment
benchbase = BenchbaseExperiment
tpcc = TpccExperiment
ycsb = YcsbExperiment

__all__ = [
    "ExperimentBase", "MixedExperiment", "DbmsBenchmarkerExperiment",
    "TpchExperiment", "TpcdsExperiment", "YcsbExperiment", "TpccExperiment",
    "BenchbaseExperiment",
    # backward-compat aliases
    "base", "mixed", "dbmsbenchmarker", "tpch", "tpcds", "ycsb", "tpcc", "benchbase",
]