class Post:
    """Provides the post command. Will run a curl command to send a POST request to the deployed
    application.

    Args:
        endpoint (string): url to send the POST request to

    Returns:
        None
    """
    def __init__(self, endpoint):
        raise NotImplementedError
