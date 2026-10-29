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


def get_host_nic(module, api_instance, ext_id, cluster_ext_id, host_ext_id):
    """
    This method will return host NIC info using external ID.
    Args:
        module: Ansible module
        api_instance: ClustersApi instance from sdk
        ext_id (str): host NIC external ID
        cluster_ext_id (str): cluster external ID
        host_ext_id (str): host external ID
    return:
        host NIC info (object): host NIC info
    """
    try:
        return api_instance.get_host_nic_by_id(
            clusterExtId=cluster_ext_id,
            hostExtId=host_ext_id,
            extId=ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching host NIC info using ext_id",
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


def list_data_stores_by_cluster_id(module, api_instance, cluster_ext_id, **kwargs):
    """
    This method will return the list of datastores associated with a cluster.
    Args:
        module: Ansible module
        api_instance: StorageContainersApi instance from sdk
        cluster_ext_id (str): cluster external ID
        kwargs (dict): additional query parameters (_page, _limit, _filter, _orderby)
    return:
        datastores list API response (object)
    """
    try:
        return api_instance.list_data_stores_by_cluster_id(
            clusterExtId=cluster_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing datastores for cluster with ext_id: {0}".format(
                cluster_ext_id
            ),
        )


def find_data_store_by_name(module, api_instance, cluster_ext_id, datastore_name):
    """
    This method will return the datastore matching ``datastore_name`` inside
    the cluster identified by ``cluster_ext_id``.
    Args:
        module: Ansible module
        api_instance: StorageContainersApi instance from sdk
        cluster_ext_id (str): cluster external ID
        datastore_name (str): datastore name to look up
    return:
        datastore info (object) or None if not found
    """
    resp = list_data_stores_by_cluster_id(
        module,
        api_instance,
        cluster_ext_id,
        _filter="datastoreName eq '{0}'".format(datastore_name),
    )
    data_stores = getattr(resp, "data", None) or []
    if data_stores:
        return data_stores[0]
    return None


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


def get_certificate_authority(module, api_instance, ext_id, cluster_ext_id):
    """
    This method will return Certificate Authority (CA) info using external ID.
    Args:
        module: Ansible module
        api_instance: CertificateManagerApi instance from sdk
        ext_id (str): Certificate Authority external ID
        cluster_ext_id (str): cluster external ID
    return:
        certificate authority info (object): certificate authority info
    """
    try:
        return api_instance.get_certificate_authority_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching certificate authority info using ext_id",
        )


def get_certificate(module, api_instance, ext_id, cluster_ext_id):
    """
    This method will return Certificate info using external ID.
    Args:
        module: Ansible module
        api_instance: CertificateManagerApi instance from sdk
        ext_id (str): Certificate external ID
        cluster_ext_id (str): cluster external ID
    return:
        certificate info (object): certificate info
    """
    try:
        return api_instance.get_certificate_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching certificate info using ext_id",
        )


def get_csr(module, api_instance, ext_id, cluster_ext_id):
    """
    This method will return Certificate Signing Request (CSR) info using external ID.
    Args:
        module: Ansible module
        api_instance: CertificateManagerApi instance from sdk
        ext_id (str): CSR external ID
        cluster_ext_id (str): cluster external ID
    return:
        csr info (object): csr info
    """
    try:
        return api_instance.get_csr_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching CSR info using ext_id",
        )


def download_csr(module, api_instance, cluster_ext_id, csr_ext_id):
    """
    This method will download a Certificate Signing Request (CSR) file.
    Args:
        module: Ansible module
        api_instance: CertificateManagerApi instance from sdk
        cluster_ext_id (str): cluster external ID
        csr_ext_id (str): CSR external ID
    return:
        download response (object): SDK download CSR API response
    """
    try:
        return api_instance.download_csr_by_id(
            clusterExtId=cluster_ext_id, csrExtId=csr_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while downloading CSR with ext_id: {0}".format(
                csr_ext_id
            ),
        )


def get_cluster_stats(module, api_instance, ext_id, **kwargs):
    """
    This method will return cluster stats using external ID.
    Args:
        module: Ansible module
        api_instance: ClustersApi instance from sdk
        ext_id (str): cluster external ID
        kwargs (dict): additional query parameters
            (_startTime, _endTime, _samplingInterval, _statType, _select)
    return:
        cluster stats info (object): cluster stats info
    """
    try:
        return api_instance.get_cluster_stats(extId=ext_id, **kwargs).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster stats using ext_id",
        )


def get_bmc_info(module, api_instance, cluster_ext_id, host_ext_id):
    """
    This method will return BMC info for a specific host in a cluster.
    Args:
        module: Ansible module
        api_instance: BmcApi instance from sdk
        cluster_ext_id (str): cluster external ID
        host_ext_id (str): host external ID
    return:
        bmc info (object): BMC info entity
    """
    try:
        return api_instance.get_bmc_info(
            clusterExtId=cluster_ext_id, extId=host_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching BMC info using cluster and host ext_id",
        )


def get_rackable_unit(module, api_instance, ext_id, cluster_ext_id):
    """
    This method will return rackable unit info using external ID.
    Args:
        module: Ansible module
        api_instance: ClustersApi instance from sdk
        ext_id (str): rackable unit external ID
        cluster_ext_id (str): parent cluster external ID
    return:
        rackable unit info (object): rackable unit info
    """
    try:
        return api_instance.get_rackable_unit_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching rackable unit info using ext_id",
        )


def get_virtual_nic(module, api_instance, ext_id, cluster_ext_id, host_ext_id):
    """
    This method will return virtual NIC info using external ID.
    Args:
        module: Ansible module
        api_instance: ClustersApi instance from sdk
        ext_id (str): virtual NIC external ID
        cluster_ext_id (str): parent cluster external ID
        host_ext_id (str): parent host external ID
    return:
        virtual NIC info (object): virtual NIC info
    """
    try:
        return api_instance.get_virtual_nic_by_id(
            clusterExtId=cluster_ext_id,
            hostExtId=host_ext_id,
            extId=ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virtual NIC info using ext_id",
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


def get_rsyslog_server(module, api_instance, cluster_ext_id, ext_id):
    """
    This method will return rsyslog server info using external ID.
    Args:
        module: Ansible module
        api_instance: ClustersApi instance from sdk
        cluster_ext_id (str): cluster external ID
        ext_id (str): rsyslog server external ID
    return:
        rsyslog server info (object): rsyslog server info
    """
    try:
        return api_instance.get_rsyslog_server_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching rsyslog server info using ext_id",
        )


def list_rsyslog_servers(module, api_instance, cluster_ext_id):
    """
    List RSYSLOG servers for a cluster.
    Args:
        module: Ansible module
        api_instance: ClustersApi instance from sdk
        cluster_ext_id (str): cluster external ID
    return:
        ListRsyslogServersByClusterIdApiResponse instance
    """
    try:
        return api_instance.list_rsyslog_servers_by_cluster_id(
            clusterExtId=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching RSYSLOG servers info",
        )
