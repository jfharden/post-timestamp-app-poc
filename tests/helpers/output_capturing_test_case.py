from io import StringIO
import sys
import unittest


class OutputCapturingTestCase(unittest.TestCase):
    """TestCase class which will handle capturing stdin, stdout, stderr, and resetting them
    after the test
    """

    def setUp(self):
        self.saved_stdin = sys.stdin
        self.saved_stdout = sys.stdout
        self.saved_stderr = sys.stderr

        self.stdin = StringIO()
        self.stdout = StringIO()
        self.stderr = StringIO()

        sys.stdin = self.stdin
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    def tearDown(self):
        sys.stdin = self.saved_stdin
        sys.stdout = self.saved_stdout
        sys.stderr = self.saved_stderr

    def _reset_output(self):
        self.stdin.truncate(0)
        self.stdout.truncate(0)
        self.stderr.truncate(0)
