class Deploy:
    """Provides the deploy command. Will run terraform apply.

    Args:
        app_name (string): Prefix name to use on all deployed resources.
        resource_group_tag_name (string): Tag name to attach to all resources to group them (value will be app_name)

    Returns:
        None
    """
    def __init__(self, app_name, resource_group_tag_name):
        raise NotImplementedError
