# type: ignore
# pylint: skip-file
# TODO: this is a Work in progress, so we can temporarily disable checking here.
import logging
from pkg_resources import iter_entry_points

from pavo.helpers import config
from pavo.core.errors import DeployUnknownPipelineError


def main(selected_pipeline=None):
    """Helps to deploy your website via a chosen pipeline

    Args:
        selected_pipeline (str): the pipeline to use to deploy the website.

    Returns:
        None

    Raises:
        DeployUnknownPipelineError: the selected pipeline is not installed or is unknown.
    """
    configured_pipeline = None

    if not selected_pipeline:
        selected_pipeline = config.get_config_value('deployment.default-pipeline')

    for pipeline in iter_entry_points('pavo.deploy'):
        if pipeline.name == selected_pipeline:
            configured_pipeline = pipeline.load()

    if configured_pipeline is None:
        raise DeployUnknownPipelineError
    else:
        configured_pipeline()


def get_pipelines():
    """Retrieves all registered pipelines from installed modules

    Returns:
        dict: All registered pipelines.
    """
    pipelines = {}
    for pipeline in iter_entry_points('pavo.deploy'):
        if pipeline.name not in pipelines.keys():
            pipelines[pipeline.name] = pipeline.load()
            log.debug(f'Found and added {pipeline.name}')
        else:
            log.debug(f'{pipeline.name} was already loaded by another source.')

    return pipelines
