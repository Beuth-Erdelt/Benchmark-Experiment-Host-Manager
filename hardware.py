"""
Entry script of the hardware benchmark: ``python hardware.py <mode> [options]`` or ``bexhoma hardware ...``.

The code is in :mod:`bexhoma.benchmarks.hardware.cli`.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.hardware.cli import main

if __name__ == '__main__':
    main()
