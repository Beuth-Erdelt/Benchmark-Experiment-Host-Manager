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

def map_index_to_queryname(numQuery):
    """
    Maps a query index string (e.g., 'q1', 'q2', etc.) to a human-readable query title 
    from the global `query_properties` dictionary.

    If the title is not found in `query_properties`, the input string is returned as-is.

    Parameters
    ----------
    numQuery : str
        A string representing the query index, typically starting with a letter followed by a number (e.g., 'q1').

    Returns
    -------
    str
        The title of the query if available in `query_properties`, otherwise the original input string.
    """
    global query_properties
    if numQuery[1:] in query_properties and 'config' in query_properties[numQuery[1:]] and 'title' in query_properties[numQuery[1:]]['config']:
        return query_properties[numQuery[1:]]['config']['title']
    else:
        return numQuery


"""
############################################################################
DBMSBenchmarker
############################################################################
"""

class dbmsbenchmarker(base):
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
        return evaluators.dbmsbenchmarker(code=code, path=self.path)
