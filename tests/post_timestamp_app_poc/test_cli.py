from unittest.mock import patch

from post_timestamp_app_poc.cli import CLI

from tests.helpers.output_capturing_test_case import OutputCapturingTestCase


class TestCLI(OutputCapturingTestCase):
    def setUp(self):
        super().setUp()

        self.cli = CLI(stdin=self.stdin, stdout=self.stdout, stderr=self.stderr)

    def test_help(self):
        args = ['--help']

        with self.assertRaises(SystemExit, msg="0"):
            self.cli.run(args)

        self.assertIn("Timestamp POST proof of concept by Jonathan Harden", self.stdout.getvalue())

    @patch("post_timestamp_app_poc.cli.Deploy", autospec=True)
    def test_deploy(self, deploy_mock_class):
        args = ['deploy']
        self.cli.run(args)
        deploy_mock_class.assert_called_with(self.stdin, self.stdout, self.stderr)
        deploy_mock_class.return_value.execute.assert_called_with("jfharden-poc", "project")

        self._reset_output()

        args = ['deploy', '--app-name', 'foo']
        self.cli.run(args)
        deploy_mock_class.assert_called_with(self.stdin, self.stdout, self.stderr)
        deploy_mock_class.return_value.execute.assert_called_with("foo", "project")

        self._reset_output()

        args = ['deploy', '-n', 'bar']
        self.cli.run(args)
        deploy_mock_class.assert_called_with(self.stdin, self.stdout, self.stderr)
        deploy_mock_class.return_value.execute.assert_called_with("bar", "project")

        self._reset_output()

        args = ['deploy', '--resource-group-tag-name', 'baz']
        self.cli.run(args)
        deploy_mock_class.assert_called_with(self.stdin, self.stdout, self.stderr)
        deploy_mock_class.return_value.execute.assert_called_with("jfharden-poc", "baz")

        self._reset_output()

        args = ['deploy', '-r', 'qux']
        self.cli.run(args)
        deploy_mock_class.assert_called_with(self.stdin, self.stdout, self.stderr)
        deploy_mock_class.return_value.execute.assert_called_with("jfharden-poc", "qux")

    @patch("post_timestamp_app_poc.cli.Destroy", autospec=True)
    def test_destroy(self, destroy_mock_class):
        args = ['destroy']
        self.cli.run(args)
        destroy_mock_class.assert_called_with(self.stdin, self.stdout, self.stderr)
        destroy_mock_class.return_value.execute.assert_called_with()

    @patch("post_timestamp_app_poc.cli.Post", autospec=True)
    def test_post(self, post_mock_class):
        args = ['post']
        self.cli.run(args)
        post_mock_class.assert_called_with(self.stdin, self.stdout, self.stderr)
        post_mock_class.return_value.execute.assert_called_with(None)

        self._reset_output()

        args = ['post', '--endpoint', 'foo']
        self.cli.run(args)
        post_mock_class.assert_called_with(self.stdin, self.stdout, self.stderr)
        post_mock_class.return_value.execute.assert_called_with("foo")

        self._reset_output()

        args = ['post', '-e', 'bar']
        self.cli.run(args)
        post_mock_class.assert_called_with(self.stdin, self.stdout, self.stderr)
        post_mock_class.return_value.execute.assert_called_with("bar")
