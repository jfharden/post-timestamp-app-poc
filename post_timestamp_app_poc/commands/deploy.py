from post_timestamp_app_poc.commands.base_command import BaseCommand


class Deploy(BaseCommand):
    """Provides the deploy command. Will run terraform apply.
    """

    def execute(self, app_name, resource_group_tag_name):
        """Execute terraform apply with the provided arguments

            Args:
                app_name (string): Prefix name to use on all deployed resources.
                resource_group_tag_name (string): Name of a tag (value will be app_name) to add to all resources"

            Returns:
                None
        """
        raise NotImplementedError
