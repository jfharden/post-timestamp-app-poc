import argparse
import sys

from post_timestamp_app_poc.commands.deploy import Deploy
from post_timestamp_app_poc.commands.destroy import Destroy
from post_timestamp_app_poc.commands.post import Post


class CLI:
    """Coordinating class to run the CLI
    """
    def __init__(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        """Initialiser

        Keyword Args:
            stdin (file): file IO object to use for stdin when running commands. (Default sys.stdin)
            stdout (file): file IO object to use for stdout when running commands. (Default sys.stdout)
            stderr (file): file IO object to use for stderr when running commands. (Default sys.stderr)
        """
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def run(self, args=sys.argv[1:]):
        """Execute the cli action

        Keyword Args:
            args (list): List of strings to parse for arguments (Default sys.argv[1:])

        Returns:
            None
        """
        parser = argparse.ArgumentParser(description="Timestamp POST proof of concept by Jonathan Harden")
        subparsers = parser.add_subparsers(dest="command_name", required=True)

        self.__setup_deploy_parser(subparsers)
        self.__setup_destroy_parser(subparsers)
        self.__setup_post_parser(subparsers)

        parsed_args = parser.parse_args(args)

        if parsed_args.command_name == "deploy":
            self.__deploy(parsed_args)
        elif parsed_args.command_name == "destroy":
            self.__destroy(parsed_args)
        elif parsed_args.command_name == "post":
            self.__post(parsed_args)

    def __setup_deploy_parser(self, subparsers):
        deploy_parser = subparsers.add_parser(
            "deploy", description="Deploy the solution into AWS. Will run terraform apply"
        )
        deploy_parser.add_argument(
            "-n", "--app-name",
            default="jfharden-poc",
            help="Name to use for most resources (for some it will be used as a prefix separated with a '-'",
        )
        deploy_parser.add_argument(
            "-r", "--resource-group-tag-name",
            default="project",
            help="Name of a tag (value will be APP_NAME) to add to all resources to allow for grouping",
        )
        deploy_parser.add_argument(
            "--region",
            default="eu-west-2",
            help="AWS region to deploy into (default eu-west-2).",
        )

    def __setup_destroy_parser(self, subparsers):
        destroy_parser = subparsers.add_parser(
            "destroy", description="Destroy the solution in AWS (will run terraform destroy)"
        )
        destroy_parser.add_argument(
            "--region",
            default="eu-west-2",
            help="AWS region to destroy in (default eu-west-2).",
        )

    def __setup_post_parser(self, subparsers):
        post_parser = subparsers.add_parser(
            "post", description="Perform a POST request to the deployed solution"
        )
        post_parser.add_argument(
            "-e", "--endpoint",
            dest="endpoint",
            help="Endpoint URL to POST to. If not provided will be read from the terraform state file",
        )

    def __deploy(self, parsed_args):
        deploy_command = Deploy(self.stdin, self.stdout, self.stderr)
        deploy_command.execute(parsed_args.app_name, parsed_args.resource_group_tag_name, parsed_args.region)

    def __destroy(self, parsed_args):
        destroy_command = Destroy(self.stdin, self.stdout, self.stderr)
        destroy_command.execute(parsed_args.region)

    def __post(self, parsed_args):
        post_command = Post(self.stdin, self.stdout, self.stderr)
        post_command.execute(parsed_args.endpoint)
