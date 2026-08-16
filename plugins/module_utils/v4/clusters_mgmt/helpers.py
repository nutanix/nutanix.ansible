# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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


def get_ssl_certificates(module, api_instance, ext_id):
    """
    This method will return SSL certificate info using external ID.
    Args:
        module: Ansible module
        api_instance: SSLCertificateApi instance from sdk
        ext_id (str): cluster external ID
    return:
        SSL certificate info (object): SSL certificate info
    """
    try:
        return api_instance.get_ssl_certificate(clusterExtId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching SSL certificate info using cluster ext_id",
        )


def get_cluster_profile(module, api_instance, ext_id):
    """
    This method will return cluster profile info using external ID.
    Args:
        module: Ansible module
        api_instance: ClusterProfilesApi instance from sdk
        ext_id (str): cluster profile external ID
    return:
        cluster profile info (object): cluster profile info
    """
    try:
        return api_instance.get_cluster_profile_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster profile info using ext_id",
        )


def get_virtual_gpu_profile(module, api_instance, cluster_ext_id, ext_id):
    """
    This method will return a virtual GPU profile by external ID.

    The underlying V4 ClustersApi only exposes a list endpoint
    (list_virtual_gpu_profiles). We emulate a "get by ext_id" by listing
    profiles for the given cluster and returning the entry whose ext_id
    matches. If the profile is not found, the module will be failed with a
    descriptive error.

    Args:
        module: Ansible module
        api_instance: ClustersApi instance from sdk
        cluster_ext_id (str): cluster external ID (path parameter)
        ext_id (str): virtual GPU profile external ID to look up
    return:
        virtual GPU profile (object): matching VirtualGpuProfile object
    """
    try:
        resp = api_instance.list_virtual_gpu_profiles(clusterExtId=cluster_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virtual GPU profiles for cluster",
        )
    profiles = resp.data or []
    for profile in profiles:
        if getattr(profile, "ext_id", None) == ext_id:
            return profile
    module.fail_json(
        msg=(
            "Virtual GPU profile with ext_id '{0}' not found on cluster '{1}'".format(
                ext_id, cluster_ext_id
            )
        )
    )
