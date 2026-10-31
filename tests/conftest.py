"""Pytest session setup: isolate the SQLite database per test session."""

import os
import tempfile

SESSION_TMP = tempfile.mkdtemp(prefix="importguard-test-")
os.environ["IMPORTGUARD_DB"] = os.path.join(SESSION_TMP, "test.db")
