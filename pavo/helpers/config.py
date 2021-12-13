from functools import reduce
from typing import Union
import yaml


def get_config_value(keys: str) -> Union[dict, str]:
    """Retrieves a configuration value from the Pavo configuration file.

    Args:
        keys (str): The string of (nested) dictionary values.

    Note:
        You can find nested keys by introducing '.' in your ``keys`` value.
        foo.bar will be looked up as: ``config[foo][bar]``

    Returns:
        dict/str: Dictionary with values if not fully nested, string with value if fully unnested.
    """
    with open('.pavoconfig', 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return reduce(lambda d, key: d.get(key, '') if isinstance(d, dict) else '', keys.split("."), config)
