import json
import os
import sys

from post_timestamp_app_poc.commands.base_command import BaseCommand


class Post(BaseCommand):
    """Provides the post command. Will run a curl command to send a POST request to the deployed
    application.

    Args:
        endpoint (string): url to send the POST request to. If set to None it will be loaded from the state file

    Returns:
        None
    """
    def execute(self, endpoint):
        if endpoint is None:
            endpoint = self._load_endpoint_from_state()

        post_cmd = ["curl", "-X", "POST", endpoint]

        self._run(post_cmd)

    def _load_endpoint_from_state(self):
        try:
            with open(os.path.join("terraform", "terraform.tfstate")) as state_file:
                state = json.load(state_file)
        except FileNotFoundError:
            self.stderr.write("Terraform state not found, perhaps you need to deploy first\n")
            sys.exit(1)

        try:
            return state["outputs"]["api_gateway_url"]["value"]
        except KeyError:
            self.stderr.write("Terraform state didn't contain api_gateway_url, perhaps you need to deploy\n")
            sys.exit(1)
