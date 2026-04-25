"""
Collector for Benchbase experiments.

Provides :class:`benchbase`, a thin subclass of :class:`base` that wires up
:class:`evaluators.benchbase` as the evaluator. All data collection and
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


class benchbase(base):
    """
    Collector for Benchbase experiments.

    Overrides :meth:`get_evaluator` to return a :class:`evaluators.benchbase` instance.
    All data collection and aggregation methods are inherited from :class:`base`.
    """
    def __init__(self, path, codes):
        base.__init__(self, path, codes)

    def get_evaluator(self, code=''):
        if code == '':
            code = self.codes[0]
        return evaluators.benchbase(code=code, path=self.path)
