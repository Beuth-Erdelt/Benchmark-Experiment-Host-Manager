"""
Entry script of the tpch benchmark: ``python tpch.py <mode> [options]`` or ``bexhoma tpch ...``.

The code is in :mod:`bexhoma.benchmarks.tpch.cli`.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.tpch.cli import main

if __name__ == '__main__':
    main()
