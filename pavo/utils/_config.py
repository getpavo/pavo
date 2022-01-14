from functools import reduce
from typing import Any
import yaml


def get_config_value(keys: str) -> Any:
    """Retrieves a configuration value from the Pavo configuration file.

    Args:
        keys (str): The string of (nested) dictionary values.

    Note:
        You can find nested keys by introducing '.' in your `keys` value.
        foo.bar will be looked up as: `config[foo][bar]`.
        A value can have any default Yaml scalar type and will be loaded as its Python equivalent.

    Returns:
        The value in the configuration, empty string if not found in the configuration.
    """
    with open('pavoconfig.yaml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return reduce(lambda d, key: d.get(key, '') if isinstance(d, dict) else '', keys.split("."), config)
