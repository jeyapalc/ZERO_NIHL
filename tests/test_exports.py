"""Ensure committed exports rebuild byte-for-byte across hash seeds."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExportTests(unittest.TestCase):
    def test_reproducible_exports(self):
        paths = [*ROOT.glob('data/*.csv'), *ROOT.glob('lists/*'),
                 ROOT / 'CATALOG.md', ROOT / 'CANADA_LTE_CATALOG.md']
        expected = {path.relative_to(ROOT): path.read_bytes()
                    for path in paths if path.is_file()}
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / 'repo'
            shutil.copytree(ROOT, checkout,
                            ignore=shutil.ignore_patterns('.git', '__pycache__'))
            for seed in ('1', '2', '42'):
                env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONUTF8='0')
                result = subprocess.run(
                    [sys.executable, 'tools/build.py'], cwd=checkout, env=env,
                    capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                for relative, content in expected.items():
                    with self.subTest(seed=seed, path=str(relative)):
                        self.assertEqual((checkout / relative).read_bytes(), content)
