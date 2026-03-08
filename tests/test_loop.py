import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))
import unittest
from unittest.mock import patch
import subprocess
from tdd_loop import run_loop, generate_test
from pathlib import Path
from tempfile import TemporaryDirectory


class TestLoop(unittest.TestCase):
    def test_loop_autopatch(self):
        with TemporaryDirectory() as td:
            f = Path(td) / "bad.py"
            f.write_text("def x():\n    pritn('hi')\n")
            ok, logs = run_loop(str(f), retries=3)
            self.assertTrue(ok)
            self.assertGreaterEqual(len(logs), 1)

    def test_loop_autopatch_prnit_variant(self):
        with TemporaryDirectory() as td:
            f = Path(td) / "bad2.py"
            f.write_text("def x():\n    prnit('hi')\n")
            ok, logs = run_loop(str(f), retries=3)
            self.assertTrue(ok)
            self.assertGreaterEqual(len(logs), 1)

    def test_retries_zero_is_clamped(self):
        with TemporaryDirectory() as td:
            f = Path(td) / "bad3.py"
            f.write_text("def x():\n    pritn('hi')\n")
            ok, logs = run_loop(str(f), retries=0)
            self.assertTrue(ok)
            self.assertGreaterEqual(len(logs), 1)

    def test_loop_autopatch_prin_variant(self):
        with TemporaryDirectory() as td:
            f = Path(td) / "bad_prin.py"
            f.write_text("def x():\n    prin('hi')\n")
            ok, _ = run_loop(str(f), retries=3)
            self.assertTrue(ok)

    def test_timeout_is_reported(self):
        with TemporaryDirectory() as td:
            f = Path(td) / "bad_timeout.py"
            f.write_text("def x():\n    pass\n")
            with patch("tdd_loop.subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="x", timeout=1)):
                ok, logs = run_loop(str(f), retries=1)
            self.assertFalse(ok)
            self.assertEqual(logs[0][1], 124)

    def test_generate_test_sanitizes_filename(self):
        with TemporaryDirectory() as td:
            f = Path(td) / "hello-world.py"
            f.write_text("def x():\n    return 1\n")
            t = generate_test(f)
            self.assertTrue(t.name.startswith("test_hello_world"))

    def test_generate_test_avoids_overwrite(self):
        with TemporaryDirectory() as td:
            f = Path(td) / "dup.py"
            f.write_text("def x():\n    return 1\n")
            first = generate_test(f)
            second = generate_test(f)
            self.assertNotEqual(first.name, second.name)

    def test_missing_target_file(self):
        ok, logs = run_loop("/tmp/does-not-exist-xyz.py", retries=2)
        self.assertFalse(ok)
        self.assertIn("Target file not found", logs[0][2])


if __name__ == '__main__':
    unittest.main()
