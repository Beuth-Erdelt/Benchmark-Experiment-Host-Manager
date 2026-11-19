"""
The version is written in three places; Zenodo and citations read the latter two.
They must agree; bump_version.py sets all three.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import json
import os
import re
import unittest

from bexhoma.__version__ import __version__

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class VersionTest(unittest.TestCase):

    def test_citation_cff(self):
        with open(os.path.join(REPO, 'CITATION.cff'), encoding='utf-8') as f:
            match = re.search(r'^version:\s*"?([^"\s]+)"?\s*$', f.read(), re.MULTILINE)
        self.assertIsNotNone(match, 'CITATION.cff has no version')
        self.assertEqual(match.group(1), __version__)

    def test_codemeta(self):
        with open(os.path.join(REPO, 'codemeta.json'), encoding='utf-8') as f:
            self.assertEqual(json.load(f)['version'], __version__)


if __name__ == '__main__':
    unittest.main()
