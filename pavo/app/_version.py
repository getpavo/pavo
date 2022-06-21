import pkg_resources

from pavo.utils import files, config

DISTRIBUTION_VERSION = pkg_resources.get_distribution("pavo").version
CONFIGURATION_VERSION = config.get_config_value("version")


def has_matching_versions() -> bool:
    """Checks the configuration value for version with the Pavo distribution version.

    Notes:
        When current directory is not a project, will always return True.

    Returns:
        bool: Whether the configuration version matches the actual distribution version.
    """
    if not files.cd_is_project():
        return True

    return DISTRIBUTION_VERSION == CONFIGURATION_VERSION
