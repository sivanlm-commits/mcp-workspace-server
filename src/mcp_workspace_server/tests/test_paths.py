import os
import tempfile
import unittest
from pathlib import Path

from mcp_workspace_server.server import safe_path


class WorkspaceSecurityTests(unittest.TestCase):

    def test_valid_path_stays_inside_workspace(self):
        path = safe_path("notes/example.txt")
        self.assertIsInstance(path, Path)

    def test_parent_traversal_is_blocked(self):
        with self.assertRaises(ValueError):
            safe_path("../secret.txt")


if __name__ == "__main__":
    unittest.main()
