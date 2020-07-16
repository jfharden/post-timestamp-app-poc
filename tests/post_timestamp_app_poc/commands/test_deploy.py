from unittest.mock import patch, call

from post_timestamp_app_poc.commands.deploy import Deploy

from tests.helpers.output_capturing_test_case import OutputCapturingTestCase


class TestDeploy(OutputCapturingTestCase):
    def setUp(self):
        super().setUp()

        self.deploy_command = Deploy(self.stdin, self.stdout, self.stderr)

    @patch("post_timestamp_app_poc.commands.base_command.subprocess")
    def test_execute(self, subprocess_mock):
        self.deploy_command.execute("foo", "bar", "baz")
        subprocess_mock.run.assert_has_calls([
            call(
                ["terraform", "init"],
                cwd="terraform/",
                stdin=self.stdin,
                stdout=self.stdout,
                stderr=self.stderr,
            ),
            call(
                ["terraform", "apply",
                    "-var", "app_name=foo",
                    "-var", "resource_group_tag_name=bar",
                    "-var", "aws_region=baz",
                    "-auto-approve"],
                cwd="terraform/",
                stdin=self.stdin,
                stdout=self.stdout,
                stderr=self.stderr,
            )
        ])
