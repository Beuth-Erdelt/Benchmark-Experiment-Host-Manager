"""
Collector for HammerDB TPC-C experiments.

Provides :class:`tpcc`, a thin subclass of :class:`base` that wires up
:class:`evaluators.tpcc` as the evaluator. All data collection and
aggregation logic is inherited from :class:`base`.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
import seaborn as sns
from math import floor
import ast
import json
import re
import numpy as np
from scipy.stats import gmean
import pprint

from dbmsbenchmarker import parameter, inspector

from bexhoma import evaluators
from .base import base


class tpcc(base):
    """
    Collector for HammerDB TPC-C experiments.

    Overrides :meth:`get_evaluator` to return a :class:`evaluators.tpcc` instance.
    All data collection and aggregation methods are inherited from :class:`base`.
    """
    def __init__(self, path, codes):
        """
        :param path: Base filesystem path that contains the experiment directories.
        :type path: str
        :param codes: List of experiment codes to collect results for.
        :type codes: list[str]
        """
        base.__init__(self, path, codes)

    def get_evaluator(self, code=''):
        """
        Returns a :class:`evaluators.tpcc` instance for the given experiment code.

        :param code: Experiment identifier. Defaults to the first code in ``self.codes``.
        :type code: str
        :return: TPC-C evaluator for the specified experiment.
        :rtype: evaluators.tpcc
        """
        if code == '':
            code = self.codes[0]
        return evaluators.tpcc(code=code, path=self.path)
