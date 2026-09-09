# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_lcm_status(module, api_instance, cluster_ext_id=None):
    """
    This method will return LCM status info.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM status api instance
        cluster_ext_id (str): External id of cluster
    Returns:
        lcm_status_info (dict): LCM status info
    """
    try:
        return api_instance.get_status(X_Cluster_Id=cluster_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM status info",
        )


def get_lcm_config(module, api_instance, cluster_ext_id=None):
    """
    This method will return LCM config info.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM config api instance
        cluster_ext_id (str): External id of cluster
    Returns:
        lcm_config_info (dict): LCM config info
    """
    try:
        return api_instance.get_config(X_Cluster_Id=cluster_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM config info",
        )


def get_lcm_entity(module, api_instance, ext_id):
    """
    This method will return entity info using external identifier of the entity.
    Args:
        module (object): Ansible module object
        api_instance (object): Entity api instance
        ext_id (str): External id of entity
    Returns:
        entity_info (dict): Entity info
    """
    try:
        return api_instance.get_entity_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching entity info using external identifier of the entity",
        )


def get_hardware_provider(module, api_instance, ext_id):
    """
    This method will return a hardware provider using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): Hardware providers api instance
        ext_id (str): External id of the hardware provider
    Returns:
        hardware_provider (object): Hardware provider info
    """
    try:
        return api_instance.get_hardware_provider_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching hardware provider info "
            "using external identifier of the hardware provider",
        )


def get_connection(module, api_instance, hardware_provider_ext_id, ext_id):
    """
    This method will return a connection using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): Hardware providers api instance
        hardware_provider_ext_id (str): External id of the hardware provider
        ext_id (str): External id of the connection
    Returns:
        connection (object): Connection info
    """
    try:
        return api_instance.get_connection_by_id(
            hardwareProviderExtId=hardware_provider_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching connection info "
            "using external identifier of the connection",
        )


def get_connection_node(
    module, api_instance, hardware_provider_ext_id, connection_ext_id, ext_id
):
    """
    This method will return a discovered node using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): Hardware providers api instance
        hardware_provider_ext_id (str): External id of the hardware provider
        connection_ext_id (str): External id of the connection
        ext_id (str): External id of the discovered node
    Returns:
        node (object): Discovered node info
    """
    try:
        return api_instance.get_connection_node_by_id(
            hardwareProviderExtId=hardware_provider_ext_id,
            connectionExtId=connection_ext_id,
            extId=ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching discovered node info "
            "using external identifier of the node",
        )


def get_ip_pool(
    module, api_instance, hardware_provider_ext_id, connection_ext_id, ext_id
):
    """
    This method will return an IP address pool using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): Hardware providers api instance
        hardware_provider_ext_id (str): External id of the hardware provider
        connection_ext_id (str): External id of the connection
        ext_id (str): External id of the IP address pool
    Returns:
        ip_pool (object): IP address pool info
    """
    try:
        return api_instance.get_ip_pool_by_id(
            hardwareProviderExtId=hardware_provider_ext_id,
            connectionExtId=connection_ext_id,
            extId=ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching IP address pool info "
            "using external identifier of the pool",
        )


def get_mac_pool(
    module, api_instance, hardware_provider_ext_id, connection_ext_id, ext_id
):
    """
    This method will return a MAC address pool using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): Hardware providers api instance
        hardware_provider_ext_id (str): External id of the hardware provider
        connection_ext_id (str): External id of the connection
        ext_id (str): External id of the MAC address pool
    Returns:
        mac_pool (object): MAC address pool info
    """
    try:
        return api_instance.get_mac_pool_by_id(
            hardwareProviderExtId=hardware_provider_ext_id,
            connectionExtId=connection_ext_id,
            extId=ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching MAC address pool info "
            "using external identifier of the pool",
        )


def get_server_identity_pool(
    module, api_instance, hardware_provider_ext_id, connection_ext_id, ext_id
):
    """
    This method will return a server identity pool using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): Hardware providers api instance
        hardware_provider_ext_id (str): External id of the hardware provider
        connection_ext_id (str): External id of the connection
        ext_id (str): External id of the server identity pool
    Returns:
        server_identity_pool (object): Server identity pool info
    """
    try:
        return api_instance.get_server_identity_pool_by_id(
            hardwareProviderExtId=hardware_provider_ext_id,
            connectionExtId=connection_ext_id,
            extId=ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching server identity pool info "
            "using external identifier of the pool",
        )
