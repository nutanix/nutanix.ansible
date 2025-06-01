# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from copy import deepcopy

SDK_IMP_ERROR = None
try:
    import ntnx_objects_py_client as objects_sdk  # noqa: E402
except ImportError:

    from ...sdk_mock import mock_sdk as objects_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


class ObjectsSpecs:
    """Module specs related to object stores"""

    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", default=32),
    )

    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", default=128),
    )

    ip_address_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=objects_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=objects_sdk.IPv6Address),
    )

    object_store_spec = dict(
        name=dict(type="str"),
        description=dict(type="str"),
        deployment_version=dict(type="str"),
        domain=dict(type="str"),
        region=dict(type="str"),
        num_worker_nodes=dict(type="int"),
        cluster_ext_id=dict(type="str"),
        storage_network_reference=dict(type="str"),
        storage_network_vip=dict(
            type="dict",
            options=ip_address_spec,
            obj=objects_sdk.IPAddress,
        ),
        storage_network_dns_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=objects_sdk.IPAddress,
        ),
        public_network_reference=dict(type="str"),
        public_network_ips=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            obj=objects_sdk.IPAddress,
        ),
        total_capacity_gi_b=dict(type="int"),
    )

    @classmethod
    def get_object_store_spec(cls):
        return deepcopy(cls.object_store_spec)
