"""
:Date: 2025-07-22
:Version: 0.8.10
:Authors: Patrick K. Erdelt

    Classes for collecting and aggregating results from several experiments.

    Copyright (C) 2020  Patrick K. Erdelt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
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


"""
############################################################################
HammerDB
############################################################################
"""

class tpcc(base):
    """
    Class for evaluating Benchbase experiments.
    """
    def __init__(self,
            path,
            codes
            ):
        base.__init__(self, path, codes)


    def get_evaluator(self, code=''):
        if code == '':
            code = self.codes[0]
        return evaluators.tpcc(code=code, path=self.path)
