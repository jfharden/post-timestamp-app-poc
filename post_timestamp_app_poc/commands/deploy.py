class Deploy:
    """Provides the deploy command. Will run terraform apply.

    Args:
        app_name (string): Prefix name to use on all deployed resources
        resource_group_tag_name (string): Tag name to attach to all resources to group them
        resource_group_tag_value (string): Tag value to attach to all resources to group them

    Returns:
        None
    """
    def __init__(self, app_name, resource_group_tag_name, resource_group_tag_value):
        raise NotImplementedError
