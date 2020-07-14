from post_timestamp_app_poc.commands.base_command import BaseCommand


class Destroy(BaseCommand):
    """Provides the destroy command. Will run terraform destroy.
    """

    def execute(self):
        """Execute terraform destroy

            Returns:
                None
        """
        destroy_cmd = ["terraform", "destroy"]
        self._run(destroy_cmd, cwd="terraform/")
