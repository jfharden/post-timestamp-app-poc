from post_timestamp_app_poc.commands.deploy import Deploy
from post_timestamp_app_poc.commands.destroy import Destroy
from post_timestamp_app_poc.commands.post import Post


class CLI:
    """Coordinating class to run the CLI

    Args:
        args (list): List of strings to parse

    Returns:
        None
    """
    def __init__(self, args):
        raise NotImplementedError
