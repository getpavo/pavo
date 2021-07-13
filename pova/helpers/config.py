import yaml
from functools import reduce


def get_config_value(keys):
    """Retrieves a configuration value from the Pova configuration file.

    Args:
        keys (str): The string of (nested) dictionary values.

    Note:
        You can find nested keys by introducing '.' in your ``keys`` value.
        foo.bar will be looked up as: ``config[foo][bar]``

    Returns:
        dict/str: Dictionary with values if not fully nested, string with value if fully unnested.
    """
    with open('.povaconfig', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return reduce(lambda d, key: d.get(key, '') if isinstance(d, dict) else '', keys.split("."), config)
