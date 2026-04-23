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

    def get_total_warnings(self, query_titles=False):
        #print("\n### Warnings (result mismatch)\n")
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = evaluation.get_total_warnings(query_titles)
            df.index = evaluation.code + '-' + df.index.astype(str)
            df_performance = pd.concat([df_performance, df])
        return df_performance
            # num_warnings = df.sum().sum()
            # if num_warnings > 0:
            #     # set readable names
            #     df.index = df.index.map(map_index_to_queryname)
            #     # remove only False rows
            #     df = df[~(df == False).all(axis=1)]
            #     #print(df)
            #     print(df.to_markdown(index=True, floatfmt=".2f"))
            # else:
            #     print("No warnings")
    def get_total_errors(self, query_titles=False):
        #print("\n### Errors (failed queries)\n")
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = evaluation.get_total_warnings(query_titles)
            df.index = evaluation.code + '-' + df.index.astype(str)
            df_performance = pd.concat([df_performance, df])
        return df_performance
            # eva = collect.get_evaluator()
            # eva.get_df_loading()
            # eva.path_base
            # df = eva.evaluation.get_total_errors().T
            # num_errors = df.sum().sum()
            # if num_errors > 0:
            #     df_errors = df.copy()
            #     df_errors = df_errors[~(df_errors == False).all(axis=1)]
            #     list_error_queries = list(df_errors.index)
            #     # set readable names
            #     df.index = df.index.map(map_index_to_queryname)
            #     # remove only False rows
            #     df = df[~(df == False).all(axis=1)]
            #     #print(df)
            #     print(df.to_markdown(index=True, floatfmt=".2f"))
            #     for error in list_error_queries:
            #         numQuery = error[1:]        # remove the leading "Q""
            #         list_errors = evaluate.get_error(numQuery)
            #         list_errors = {k:v for k,v in list_errors.items() if len(v) > 0}
            #         #print(list_errors)
            #         print("* "+map_index_to_queryname(error))
            #         #df_error = pd.DataFrame.from_dict(list_errors, orient='index').sort_index()
            #         #print(df_error)
            #         for k,v in list_errors.items():
            #             print("  * {}: {}".format(k,v))
            # else:
            #     print("No errors")