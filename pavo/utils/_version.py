import pkg_resources

from ._files import cd_is_project
from ._config import get_config_value


def _safely_get_configuration_version() -> str | None:
    """Get the value from configuration, or return `None` on throwing.

    Returns:
        The configuration version as `str` if found, else `None`
    """
    try:
        version = get_config_value("version")

        if isinstance(version, str):
            return version

        return None
    except FileNotFoundError:
        return None


def has_matching_versions() -> bool:
    """Checks the configuration value for version with the Pavo distribution version.

    Notes:
        When current directory is not a project, will always return True.

    Returns:
        bool: Whether the configuration version matches the actual distribution version.
    """
    if not cd_is_project():
        return True

    return DISTRIBUTION_VERSION == CONFIGURATION_VERSION


DISTRIBUTION_VERSION = pkg_resources.get_distribution("pavo").version
CONFIGURATION_VERSION = _safely_get_configuration_version()
