"""
Entry script of the tpcds benchmark: ``python tpcds.py <mode> [options]`` or ``bexhoma tpcds ...``.

The code is in :mod:`bexhoma.benchmarks.tpcds.cli`.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.tpcds.cli import main

if __name__ == '__main__':
    main()
