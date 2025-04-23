# Copyright: 2025, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
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

    metadata_spec = dict(
        owner_reference_id=dict(type="str"),
        owner_user_name=dict(type="str"),
        project_reference_id=dict(type="str"),
        project_name=dict(type="str"),
        category_ids=dict(type="list", elements="str"),
    )

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

    storage_network_vip_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=objects_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=objects_sdk.IPv6Address),
    )

    storage_network_dns_ip_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=objects_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=objects_sdk.IPv6Address),
    )

    public_network_ips_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=objects_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=objects_sdk.IPv6Address),
    )

    object_store_spec = dict(
        name=dict(type="str"),
        metadata=dict(type="dict", options=metadata_spec, obj=objects_sdk.Metadata),
        description=dict(type="str"),
        deployment_version=dict(type="str"),
        domain=dict(type="str"),
        region=dict(type="str"),
        num_worker_nodes=dict(type="int"),
        cluster_ext_id=dict(type="str"),
        storage_network_reference=dict(type="str"),
        storage_network_vip=dict(
            type="dict",
            options=storage_network_vip_spec,
            obj=objects_sdk.IPAddress,
        ),
        storage_network_dns_ip=dict(
            type="dict",
            options=storage_network_dns_ip_spec,
            obj=objects_sdk.IPAddress,
        ),
        public_network_reference=dict(type="str"),
        public_network_ips=dict(
            type="list",
            elements="dict",
            options=public_network_ips_spec,
            obj=objects_sdk.IPAddress,
        ),
        total_capacity_gi_b=dict(type="int"),
        object_state=dict(
            type="str",
            choices=[
                "DEPLOYING_OBJECT_STORE",
                "OBJECT_STORE_DEPLOYMENT_FAILED",
                "DELETING_OBJECT_STORE",
                "OBJECT_STORE_OPERATION_FAILED",
                "UNDEPLOYED_OBJECT_STORE",
                "OBJECT_STORE_OPERATION_PENDING",
                "OBJECT_STORE_AVAILABLE",
                "OBJECT_STORE_CERT_CREATION_FAILED",
                "CREATING_OBJECT_STORE_CERT",
                "OBJECT_STORE_DELETION_FAILED",
            ],
        ),
    )

    @classmethod
    def get_object_store_spec(cls):
        return deepcopy(cls.object_store_spec)
