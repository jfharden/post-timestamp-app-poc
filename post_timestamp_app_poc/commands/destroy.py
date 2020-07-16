from post_timestamp_app_poc.commands.base_command import BaseCommand


class Destroy(BaseCommand):
    """Provides the destroy command. Will run terraform destroy.
    """

    def execute(self, region):
        """Execute terraform destroy

            Args:
                region (string): AWS region to destroy

            Returns:
                None
        """
        destroy_cmd = [
            "terraform", "destroy",
            "-var", "aws_region={}".format(region),
            "-auto-approve",
        ]
        self._run(destroy_cmd, cwd="terraform/")
