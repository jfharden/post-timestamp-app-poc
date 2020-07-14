from unittest.mock import patch

from post_timestamp_app_poc.commands.destroy import Destroy

from tests.helpers.output_capturing_test_case import OutputCapturingTestCase


class TestDestroy(OutputCapturingTestCase):
    def setUp(self):
        super().setUp()

        self.destroy_command = Destroy(self.stdin, self.stdout, self.stderr)

    @patch("post_timestamp_app_poc.commands.base_command.subprocess")
    def test_execute(self, subprocess_mock):
        self.destroy_command.execute()
        subprocess_mock.run.assert_called_with(
            ["terraform", "destroy"],
            cwd="terraform/",
            stdin=self.stdin,
            stdout=self.stdout,
            stderr=self.stderr,
        )
