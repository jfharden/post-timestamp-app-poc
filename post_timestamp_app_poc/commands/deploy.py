from post_timestamp_app_poc.commands.base_command import BaseCommand


class Deploy(BaseCommand):
    """Provides the deploy command. Will run terraform apply.
    """

    def execute(self, app_name, resource_group_tag_name, region):
        """Execute terraform init and terraform apply with the provided arguments

            Args:
                app_name (string): Prefix name to use on all deployed resources.
                resource_group_tag_name (string): Name of a tag (value will be app_name) to add to all resources
                region (string): AWS region to deploy to

            Returns:
                None
        """
        init_cmd = ["terraform", "init"]
        self._run(init_cmd, cwd="terraform/")

        apply_cmd = [
            "terraform", "apply",
            "-var", "app_name={}".format(app_name),
            "-var", "resource_group_tag_name={}".format(resource_group_tag_name),
            "-var", "aws_region={}".format(region),
            "-auto-approve",
        ]
        self._run(apply_cmd, cwd="terraform/")
