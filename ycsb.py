"""
Entry script of the ycsb benchmark: ``python ycsb.py <mode> [options]`` or ``bexhoma ycsb ...``.

The code is in :mod:`bexhoma.benchmarks.ycsb.cli`.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.ycsb.cli import main

if __name__ == '__main__':
    main()
