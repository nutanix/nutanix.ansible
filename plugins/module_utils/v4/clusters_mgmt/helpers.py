from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_cluster(module, api_instance, ext_id):
    """
    This method will return cluster info using external ID.
    Args:
        module: Ansible module
        api_instance: ClusterApi instance from sdk
        ext_id (str): cluster external ID
    return:
        cluster info (object): cluster info
    """
    try:
        return api_instance.get_cluster_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster info using ext_id",
        )


def get_host(module, api_instance, ext_id, cluster_ext_id):
    """
    This method will return host info using external ID.
    Args:
        module: Ansible module
        api_instance: ClusterApi instance from sdk
        ext_id (str): host external ID
        cluster_ext_id (str): cluster external ID
    return:
        host info (object): host info
    """
    try:
        return api_instance.get_host_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching host info using ext_id",
        )


def get_storage_container(module, api_instance, ext_id):
    """
    This method will return storage container info using external ID.
    Args:
        module: Ansible module
        api_instance: ClusterApi instance from sdk
        ext_id (str): storage container external ID
    return:
        storage container info (object): storage container info
    """
    try:
        return api_instance.get_storage_container_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching storage container info using ext_id",
        )
