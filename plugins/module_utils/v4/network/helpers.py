# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_routing_policy(module, api_instance, ext_id):
    """
    This method will return routing policy info using its ext_id
    Args:
        module: Ansible module
        api_instance: RoutingPoliciesApi instance from ntnx_networking_py_client sdk
        ext_id (str): routing policy info external ID
    return:
        info (object): routing policy info
    """
    try:
        return api_instance.get_routing_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching routing policy info using ext_id",
        )


def get_floating_ip(module, api_instance, ext_id):
    """
    Get Floating ip by ext_id
    Args:
        module: Ansible module
        api_instance: FloatingIpsApi instance from ntnx_networking_py_client sdk
        ext_id: ext_id of Floating ip
    Returns:
        floating_ip (obj): Floating ip info object
    """
    try:
        return api_instance.get_floating_ip_by_id(extId=ext_id).data

    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching floating_ip info using ext_id",
        )


def get_vpc(module, api_instance, ext_id):
    """
    Get vpc by ext_id
    Args:
        module: Ansible module
        api_instance: VpcsApi instance from ntnx_networking_py_client sdk
        ext_id: ext_id of vpc
    Returns:
        vpc (obj): Vpc info object
    """
    try:
        return api_instance.get_vpc_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vpc info using ext_id",
        )


def get_subnet(module, api_instance, ext_id):
    """
    This method will return subnet info using subnet external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): Api client instance
        ext_id (str): subnet external ID
    return:
        subnet_info (object): subnet info
    """
    try:
        return api_instance.get_subnet_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching subnet info using ext_id",
        )


def get_route_table(module, api_instance, ext_id):
    """
    This method will return route table info using route table external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): Route table API instance from SDK
        ext_id (str): route table external ID
    return:
        subnet_info (object): route table info
    """
    try:
        return api_instance.get_route_table_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching route table info using ext_id",
        )


def get_route(module, api_instance, ext_id, route_table_ext_id):
    """
    This method will return route info using route external ID and table external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): Route API instance from SDK
        ext_id (str): route external ID
        route_table_ext_id (str): route table external ID
    return:
        route_info (object): route info
    """
    try:
        return api_instance.get_route_for_route_table_by_id(
            extId=ext_id, routeTableExtId=route_table_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching route info using ext_id and table ext_id",
        )


def get_network_function(module, api_instance, ext_id):
    """
    This method will return network function info using network function external ID.
    Args:
        module (object): Ansible module object
        api_instance (object): NetworkFunctionsApi instance from ntnx_networking_py_client sdk
        ext_id (str): network function external ID
    return:
        network_function_info (object): network function info
    """
    try:
        return api_instance.get_network_function_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network function info using ext_id",
        )


def get_virtual_switch(module, api_instance, ext_id):
    """
    This method will return virtual switch info using its ext_id
    Args:
        module: Ansible module
        api_instance: VirtualSwitchesApi instance from ntnx_networking_py_client sdk
        ext_id (str): virtual switch external ID
    return:
        info (object): virtual switch info
    """
    try:
        return api_instance.get_virtual_switch_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virtual switch info using ext_id",
        )


def get_traffic_mirror(module, api_instance, ext_id):
    """
    This method will return traffic mirror session info using its ext_id
    Args:
        module: Ansible module
        api_instance: TrafficMirrorsApi instance from ntnx_networking_py_client sdk
        ext_id (str): traffic mirror session external ID
    return:
        info (object): traffic mirror session info
    """
    try:
        return api_instance.get_traffic_mirror_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching traffic mirror info using ext_id",
        )


def get_uplink_bond(module, api_instance, ext_id):
    """
    This method will return uplink bond info using its ext_id
    Args:
        module: Ansible module
        api_instance: UplinkBondsApi instance from ntnx_networking_py_client sdk
        ext_id (str): uplink bond external ID
    return:
        info (object): uplink bond info
    """
    try:
        return api_instance.get_uplink_bond_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching uplink bond info using ext_id",
        )


def get_bgp_session(module, api_instance, ext_id):
    """
    This method will return BGP session info using its ext_id.
    Args:
        module: Ansible module
        api_instance: BgpSessionsApi instance from ntnx_networking_py_client sdk
        ext_id (str): BGP session external ID
    return:
        info (object): BGP session info
    """
    try:
        return api_instance.get_bgp_session_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching BGP session info using ext_id",
        )


def get_load_balancer_session(module, api_instance, ext_id):
    """
    This method will return load balancer session info using its ext_id
    Args:
        module: Ansible module
        api_instance: LoadBalancerSessionsApi instance from ntnx_networking_py_client sdk
        ext_id (str): load balancer session external ID
    return:
        info (object): load balancer session info
    """
    try:
        return api_instance.get_load_balancer_session_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching load balancer session info using ext_id",
        )


def get_vpn_connection(module, api_instance, ext_id):
    """
    This method will return VPN connection info using its ext_id
    Args:
        module: Ansible module
        api_instance: VpnConnectionsApi instance from ntnx_networking_py_client sdk
        ext_id (str): VPN connection external ID
    return:
        info (object): VPN connection info
    """
    try:
        return api_instance.get_vpn_connection_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VPN connection info using ext_id",
        )


def get_network_controller(module, api_instance, ext_id):
    """
    This method will return network controller info using its ext_id
    Args:
        module: Ansible module
        api_instance: NetworkControllersApi instance from ntnx_networking_py_client sdk
        ext_id (str): network controller external ID
    return:
        info (object): network controller info
    """
    try:
        return api_instance.get_network_controller_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network controller info using ext_id",
        )


def get_layer2_stretch(module, api_instance, ext_id):
    """
    This method will return Layer2 Stretch info using its ext_id.
    Args:
        module: Ansible module
        api_instance: Layer2StretchesApi instance from ntnx_networking_py_client sdk
        ext_id (str): Layer2 Stretch external ID
    return:
        info (object): Layer2 Stretch info
    """
    try:
        return api_instance.get_layer2_stretch_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Layer2 Stretch info using ext_id",
        )


def get_gateway(module, api_instance, ext_id):
    """
    This method will return network gateway info using its ext_id
    Args:
        module: Ansible module
        api_instance: GatewaysApi instance from ntnx_networking_py_client sdk
        ext_id (str): gateway external ID
    return:
        info (object): gateway info
    """
    try:
        return api_instance.get_gateway_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching gateway info using ext_id",
        )


def get_vpn_appliance_config(module, api_instance, vpn_connection_ext_id, ext_id):
    """
    Fetch third-party VPN appliance configuration for a given VPN connection.

    The API returns the vendor configuration as a plain-text string that a
    user would apply on their on-premise VPN gateway (e.g. Palo Alto,
    Checkpoint, Juniper) to peer with the Nutanix VPN service.

    Args:
        module: Ansible module
        api_instance: VpnConnectionsApi instance from ntnx_networking_py_client sdk
        vpn_connection_ext_id (str): VPN connection external ID
        ext_id (str): third-party VPN appliance external ID
    return:
        config (str): vendor configuration payload
    """
    try:
        return api_instance.get_vpn_appliance_for_vpn_connection_by_id(
            vpnConnectionExtId=vpn_connection_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching third-party VPN appliance "
                "configuration for vpn_connection_ext_id={0} and ext_id={1}".format(
                    vpn_connection_ext_id, ext_id
                )
            ),
        )
