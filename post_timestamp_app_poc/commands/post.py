from post_timestamp_app_poc.commands.base_command import BaseCommand


class Post(BaseCommand):
    """Provides the post command. Will run a curl command to send a POST request to the deployed
    application.

    Args:
        endpoint (string): url to send the POST request to

    Returns:
        None
    """
    def execute(self, endpoint):
        raise NotImplementedError
