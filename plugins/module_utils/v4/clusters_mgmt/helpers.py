# Copyright: (c) 2027, Nutanix
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


def get_storage_config(module, api_instance, cluster_ext_id):
    """
    This method will return the storage configuration of a cluster using
    the cluster external ID.
    Args:
        module: Ansible module
        api_instance: StorageConfigApi instance from sdk
        cluster_ext_id (str): cluster external ID
    return:
        storage config info (object): storage configuration info
    """
    try:
        return api_instance.get_storage_config(clusterExtId=cluster_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching storage config using cluster ext_id",
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


def get_cvm(module, api_instance, ext_id, cluster_ext_id):
    """
    This method will return CVM info using external ID.
    Args:
        module: Ansible module
        api_instance: CvmsApi instance from sdk
        ext_id (str): CVM external ID
        cluster_ext_id (str): parent cluster external ID
    return:
        cvm info (object): CVM info
    """
    try:
        return api_instance.get_cvm_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching CVM info using ext_id",
        )


def get_vcenter_extension(module, api_instance, ext_id):
    """
    Fetch vCenter server extension information for the given ext_id.

    The vCenter server extension identifies the Nutanix Prism registration
    on a vCenter Server that manages an ESXi cluster attached to Prism Central.

    Args:
        module: Ansible module
        api_instance: VcenterExtensionsApi instance from
            ntnx_clustermgmt_py_client sdk
        ext_id (str): The globally unique identifier of vCenter Server
            extension instance (UUID).
    Returns:
        vcenter extension info (object): vCenter extension info
    """
    try:
        return api_instance.get_vcenter_extension_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vCenter extension info using ext_id",
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


def get_cluster_stats(module, api_instance, ext_id, kwargs):
    """
    Fetch cluster performance/capacity statistics for the given cluster
    external ID via the v4 ClustersApi.get_cluster_stats endpoint.

    Args:
        module: Ansible module
        api_instance: ClustersApi instance from sdk
        ext_id (str): cluster external ID
        kwargs (dict): the SDK query parameters
            (_startTime, _endTime, _samplingInterval, _statType, _select).

    Returns:
        The full SDK response object (ClusterStatsApiResponse) — callers
        typically only need ``.data`` from it, but the raw response is
        returned so tests can also assert on the response ``metadata``.
    """
    try:
        return api_instance.get_cluster_stats(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster stats using ext_id",
        )


def get_disk(module, api_instance, ext_id):
    """
    This method will return Disk info using external ID.
    Args:
        module: Ansible module
        api_instance: DisksApi instance from sdk
        ext_id (str): Disk external ID
    return:
        Disk info (object): Disk info
    """
    try:
        return api_instance.get_disk_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Disk info using ext_id: {0}".format(
                ext_id
            ),
        )


def get_external_storage(module, api_instance, ext_id):
    """
    This method will return external storage info using external ID.
    Args:
        module: Ansible module
        api_instance: ExternalStoragesApi instance from sdk
        ext_id (str): external storage external ID
    return:
        external storage info (object): external storage info
    """
    try:
        return api_instance.get_external_storage_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching external storage info using ext_id",
        )


def list_physical_gpu_profiles(module, api_instance, cluster_ext_id, **kwargs):
    """
    This method will return the list of physical GPU profiles for a cluster.
    Physical GPU profiles are automatically discovered from the installed GPU
    hardware across the registered clusters and are attached to virtual machines
    in passthrough mode.
    Args:
        module: Ansible module
        api_instance: ClustersApi instance from sdk
        cluster_ext_id (str): UUID of the cluster
        kwargs (dict): additional query parameters (_page, _limit, _filter, _orderby)
    return:
        physical GPU profiles list API response (object)
    """
    try:
        return api_instance.list_physical_gpu_profiles(
            clusterExtId=cluster_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching physical GPU profiles info",
        )


def list_virtual_gpu_profiles(module, api_instance, cluster_ext_id, **kwargs):
    """
    This method will return the list of virtual GPU profiles for a cluster.
    Virtual GPU profiles define the resource allocation (frame buffer, display
    heads, resolution, licensing) available to virtual machines across the
    registered clusters.
    Args:
        module: Ansible module
        api_instance: ClustersApi instance from sdk
        cluster_ext_id (str): UUID of the cluster
        kwargs (dict): additional query parameters (_page, _limit, _filter, _orderby)
    return:
        virtual GPU profiles list API response (object)
    """
    try:
        return api_instance.list_virtual_gpu_profiles(
            clusterExtId=cluster_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virtual GPU profiles info",
        )


def get_snmp_user(module, api_instance, ext_id, cluster_ext_id=None):
    """
    This method will return snmp user info using snmp user external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): ClustersApi instance from SDK
        ext_id (str): snmp user external ID
        cluster_ext_id (str): Parent cluster external ID
    return:
        snmp_user_info (object): snmp user info
    """
    try:
        return api_instance.get_snmp_user_by_id(
            extId=ext_id, clusterExtId=cluster_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching snmp user info using ext_id",
        )


def get_snmp_trap(module, api_instance, ext_id, cluster_ext_id=None):
    """
    This method will return snmp trap info using snmp trap external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): ClustersApi instance from SDK
        ext_id (str): snmp trap external ID
        cluster_ext_id (str): Parent cluster external ID
    return:
        snmp_trap_info (object): snmp trap info
    """
    try:
        return api_instance.get_snmp_trap_by_id(
            extId=ext_id, clusterExtId=cluster_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching snmp trap info using ext_id",
        )


def get_snmp_config(module, api_instance, cluster_ext_id):
    """
    This method will return snmp config info using cluster external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): ClustersApi instance from SDK
        cluster_ext_id (str): cluster external ID
    return:
        snmp_config_info (object): snmp config info
    """
    try:
        return api_instance.get_snmp_config_by_cluster_id(
            clusterExtId=cluster_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching snmp config info using cluster ext_id",
        )

