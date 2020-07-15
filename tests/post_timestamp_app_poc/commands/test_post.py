import os

from unittest.mock import patch, mock_open

from post_timestamp_app_poc.commands.post import Post

from tests.helpers.output_capturing_test_case import OutputCapturingTestCase


class TestPost(OutputCapturingTestCase):
    def setUp(self):
        super().setUp()

        self.post_command = Post(self.stdin, self.stdout, self.stderr)

    @patch("post_timestamp_app_poc.commands.base_command.subprocess")
    def test_execute_specified_endpoint(self, subprocess_mock):
        self.post_command.execute("http://www.example.com")
        subprocess_mock.run.assert_called_with(
            ["curl", "-X", "POST", "http://www.example.com"],
            cwd=None,
            stdin=self.stdin,
            stdout=self.stdout,
            stderr=self.stderr,
        )

    @patch("post_timestamp_app_poc.commands.base_command.subprocess")
    def test_execute_endpoint_from_state(self, subprocess_mock):
        open_mock = mock_open(read_data=self.__load_valid_statefile())
        with patch('post_timestamp_app_poc.commands.post.open', open_mock):
            self.post_command.execute(None)

            subprocess_mock.run.assert_called_with(
                ["curl", "-X", "POST", "http://www.example.net"],
                cwd=None,
                stdin=self.stdin,
                stdout=self.stdout,
                stderr=self.stderr,
            )

    def test_execute_no_statefile(self):
        open_mock = mock_open()
        open_mock.side_effect = FileNotFoundError()

        with patch('post_timestamp_app_poc.commands.post.open', open_mock):
            with self.assertRaises(SystemExit) as exception_context_manager:
                self.post_command.execute(None)

            self.assertEqual(
                "Terraform state not found, perhaps you need to deploy first\n",
                self.stderr.getvalue(),
            )

            self.assertEqual(1, exception_context_manager.exception.code)

    def test_execute_destroyed_statefile(self):
        open_mock = mock_open(read_data=self.__load_destroyed_statefile())

        with patch('post_timestamp_app_poc.commands.post.open', open_mock):
            with self.assertRaises(SystemExit) as exception_context_manager:
                self.post_command.execute(None)

            self.assertEqual(
                "Terraform state didn't contain api_gateway_url, perhaps you need to deploy\n",
                self.stderr.getvalue(),
            )

            self.assertEqual(1, exception_context_manager.exception.code)

    def __load_valid_statefile(self):
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, "..", "..", "fixtures", "terraform.tfstate.valid")) as state_file:
            return state_file.read()

    def __load_destroyed_statefile(self):
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, "..", "..", "fixtures", "terraform.tfstate.destroyed")) as state_file:
            return state_file.read()
