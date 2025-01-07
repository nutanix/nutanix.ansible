# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from copy import deepcopy

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:
    from ....v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


class ClusterSpecs:
    """Module specs related to cluster and its sub entities"""

    ipv4_address = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    fqdn = dict(value=dict(type="str", required=True))

    ip_address_or_fqdn = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address,
            obj=clusters_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address,
            obj=clusters_sdk.IPv6Address,
            required=False,
        ),
        fqdn=dict(type="dict", options=fqdn, obj=clusters_sdk.FQDN, required=False),
    )

    ip_address = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address,
            obj=clusters_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address,
            obj=clusters_sdk.IPv6Address,
            required=False,
        ),
    )

    smtp_network = dict(
        ip_address=dict(
            type="dict", options=ip_address_or_fqdn, obj=clusters_sdk.IPAddress
        ),
        port=dict(type="int"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )

    smtp_server = dict(
        email_address=dict(type="str"),
        server=dict(type="dict", options=smtp_network, obj=clusters_sdk.SmtpNetwork),
        type=dict(type="str", choices=["PLAIN", "STARTTLS", "SSL"]),
    )

    management_server = dict(
        ip=dict(type="dict", options=ip_address, obj=clusters_sdk.IPAddress),
        type=dict(type="str", choices=["VCENTER"]),
        is_registered=dict(type="bool"),
        in_use=dict(type="bool"),
        is_drs_enabled=dict(type="bool"),
    )

    backplane_network = dict(
        is_segmentation_enabled=dict(type="bool"),
        vlan_tag=dict(type="int"),
        subnet=dict(type="dict", options=ipv4_address, obj=clusters_sdk.IPv4Address),
        netmask=dict(type="dict", options=ipv4_address, obj=clusters_sdk.IPv4Address),
    )
    http_proxy_list = dict(
        ip_address=dict(type="dict", options=ip_address, obj=clusters_sdk.IPAddress),
        port=dict(type="int"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        name=dict(type="str", required=True),
        proxy_types=dict(
            type="list", elements="str", choices=["HTTP", "HTTPS", "SOCKS"]
        ),
    )
    http_proxy_white_list = dict(
        target_type=dict(
            type="str",
            choices=[
                "IPV6_ADDRESS",
                "HOST_NAME",
                "DOMAIN_NAME_SUFFIX",
                "IPV4_NETWORK_MASK",
                "IPV4_ADDRESS",
            ],
            required=True,
        ),
        target=dict(type="str", required=True),
    )
    cluster_network_config = dict(
        external_address=dict(
            type="dict", options=ip_address, obj=clusters_sdk.IPAddress
        ),
        external_data_service_ip=dict(
            type="dict", options=ip_address, obj=clusters_sdk.IPAddress
        ),
        nfs_subnet_whitelist=dict(type="list", elements="str"),
        ntp_server_ip_list=dict(
            type="list",
            elements="dict",
            options=ip_address_or_fqdn,
            obj=clusters_sdk.IPAddressOrFQDN,
        ),
        name_server_ip_list=dict(
            type="list",
            elements="dict",
            options=ip_address_or_fqdn,
            obj=clusters_sdk.IPAddressOrFQDN,
        ),
        smtp_server=dict(
            type="dict", options=smtp_server, obj=clusters_sdk.SmtpServerRef
        ),
        masquerading_ip=dict(
            type="dict", options=ip_address, obj=clusters_sdk.IPAddress
        ),
        management_server=dict(
            type="dict", options=management_server, obj=clusters_sdk.ManagementServerRef
        ),
        fqdn=dict(type="str"),
        key_management_server_type=dict(
            type="str", choices=["LOCAL", "PRISM_CENTRAL", "EXTERNAL"]
        ),
        backplane=dict(
            type="dict",
            options=backplane_network,
            obj=clusters_sdk.BackplaneNetworkParams,
        ),
        http_proxy_list=dict(
            type="list",
            elements="dict",
            options=http_proxy_list,
            obj=clusters_sdk.HttpProxyConfig,
        ),
        http_proxy_white_list=dict(
            type="list",
            elements="dict",
            options=http_proxy_white_list,
            obj=clusters_sdk.HttpProxyWhiteListConfig,
        ),
    )
    node = dict(
        controller_vm_ip=dict(
            type="dict", options=ip_address, obj=clusters_sdk.IPAddress, required=True
        ),
        host_ip=dict(
            type="dict", options=ip_address, obj=clusters_sdk.IPAddress, required=False
        ),
    )

    nodes = dict(
        node_list=dict(
            type="list",
            elements="dict",
            options=node,
            obj=clusters_sdk.NodeListItemReference,
            required=True,
        )
    )

    public_key = dict(
        name=dict(type="str", required=True),
        key=dict(type="str", required=True, no_log=False),
    )

    fault_tolerance_state = dict(
        domain_awareness_level=dict(
            type="str", required=True, choices=["NODE", "BLOCK", "RACK", "DISK"]
        ),
        desired_cluster_fault_tolerance=dict(
            type="str",
            choices=["CFT_1N_OR_1D", "CFT_2N_OR_2D", "CFT_1N_AND_1D", "CFT_0N_AND_0D"],
        ),
    )
    cluster_config = dict(
        cluster_function=dict(
            type="list", elements="str", choices=["AOS", "ONE_NODE", "TWO_NODE"]
        ),
        authorized_public_key_list=dict(
            type="list", elements="dict", options=public_key, obj=clusters_sdk.PublicKey
        ),
        redundancy_factor=dict(type="int"),
        cluster_arch=dict(type="str", choices=["X86_64", "PPC64LE"]),
        fault_tolerance_state=dict(
            type="dict",
            options=fault_tolerance_state,
            obj=clusters_sdk.FaultToleranceState,
        ),
        operation_mode=dict(
            type="str",
            choices=[
                "NORMAL",
                "READ_ONLY",
                "STAND_ALONE",
                "SWITCH_TO_TWO_NODE",
                "OVERRIDE",
            ],
        ),
        encryption_in_transit_status=dict(type="str", choices=["ENABLED", "DISABLED"]),
    )

    cluster = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        nodes=dict(type="dict", options=nodes, obj=clusters_sdk.NodeReference),
        config=dict(
            type="dict", options=cluster_config, obj=clusters_sdk.ClusterConfigReference
        ),
        network=dict(
            type="dict",
            options=cluster_network_config,
            obj=clusters_sdk.ClusterNetworkReference,
        ),
        container_name=dict(type="str"),
        categories=dict(type="dict"),
    )

    @classmethod
    def get_cluster_spec(cls):
        return deepcopy(cls.cluster)
