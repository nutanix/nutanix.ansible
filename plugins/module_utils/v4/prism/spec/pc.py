# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from copy import deepcopy

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ...sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


class PrismSpecs:
    """Module specs related to prism"""

    # cloud_init_script_allowed_types = {
    #     "user_data": prism_sdk.Userdata,
    #     "custom_key_values": prism_sdk.CustomKeyValues,
    # }

    location_allowed_types = {
        "cluster_location": prism_sdk.ClusterLocation,
        "object_store_location": prism_sdk.ObjectStoreLocation,
    }

    build_info_spec = dict(
        version=dict(type="str"),
    )

    # kvpair_spec = dict(name=dict(type="str"), value=dict(type="raw", no_log=False))

    # custom_key_values_spec = dict(
    #     key_value_pairs=dict(
    #         type="list",
    #         elements="dict",
    #         options=kvpair_spec,
    #         obj=prism_sdk.KVPair,
    #         no_log=False,
    #     ),
    # )
    # user_data = dict(
    #     value=dict(type="str", required=True),
    # )
    # cloud_init_script = dict(
    #     user_data=dict(type="dict", options=user_data, obj=prism_sdk.Userdata),
    #     custom_key_values=dict(
    #         type="dict",
    #         options=custom_key_values_spec,
    #         obj=prism_sdk.CustomKeyValues,
    #         no_log=False,
    #     ),
    # )

    # cloud_init_config_spec = dict(
    #     datasource_type=dict(type="str", choices=["CONFIG_DRIVE_V2"]),
    #     metadata=dict(type="str"),
    #     cloud_init_script=dict(
    #         type="dict",
    #         options=cloud_init_script,
    #         obj=cloud_init_script_allowed_types,
    #         mutually_exclusive=[("user_data", "custom_key_values")],
    #     ),
    # )
    # environment_info_spec = dict(
    #     type=dict(type="str", choices=["NTNX_CLOUD", "ONPREM"]),
    #     provider_type=dict(
    #         type="str", choices=["VSPHERE", "AZURE", "NTNX", "GCP", "AWS"]
    #     ),
    #     provisioning_type=dict(type="str", choices=["NATIVE", "NTNX"]),
    # )
    # bootstrap_config_spec = dict(
    #     cloud_init_config=dict(
    #         type="lsit",
    #         elements="dict",
    #         options=cloud_init_config_spec,
    #         obj=prism_sdk.CloudInit,
    #     ),
    #     environment_info=dict(
    #         type="dict",
    #         options=environment_info_spec,
    #         obj=prism_sdk.EnvironmentInfo,
    #     ),
    # )

    # credentials_spec = dict(
    #     username=dict(type="str", required=True),
    #     password=dict(type="str", required=True, no_log=True),
    # )

    resource_config_spec = dict(
        container_ext_ids=dict(type="list", elements="str"),
        data_disk_size_bytes=dict(type="int"),
        memory_size_bytes=dict(type="int"),
        num_vcpus=dict(type="int"),
    )

    config_spec = dict(
        should_enable_lockdown_mode=dict(type="bool"),
        build_info=dict(
            type="dict", options=build_info_spec, obj=prism_sdk.BuildInfo, required=True
        ),
        name=dict(type="str", required=True),
        size=dict(
            type="str",
            choices=["SMALL", "LARGE", "EXTRALARGE", "STARTER"],
            required=True,
        ),
        # bootstrap_config=dict(
        #     type="dict", options=bootstrap_config_spec, obj=prism_sdk.BootstrapConfig
        # ),
        # credentials=dict(
        #     type="dict",
        #     options=credentials_spec,
        #     obj=prism_sdk.Credentials,
        #     required=True,
        # ),
        resource_config=dict(
            type="dict",
            options=resource_config_spec,
            obj=prism_sdk.DomainManagerResourceConfig,
        ),
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
        ipv4=dict(type="dict", options=ipv4_spec, obj=prism_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=prism_sdk.IPv6Address),
    )

    fqdn_spec = dict(
        value=dict(type="str"),
    )

    ipaddress_or_fqdn_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=prism_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=prism_sdk.IPv6Address),
        fqdn=dict(type="dict", options=fqdn_spec, obj=prism_sdk.FQDN),
    )

    ip_ranges_spec = dict(
        begin=dict(type="dict", options=ip_address_spec, obj=prism_sdk.IPAddress),
        end=dict(type="dict", options=ip_address_spec, obj=prism_sdk.IPAddress),
    )

    internal_networks_spec = dict(
        default_gateway=dict(
            type="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
        ),
        subnet_mask=dict(
            type="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
        ),
        ip_ranges=dict(
            type="list",
            elements="dict",
            options=ip_ranges_spec,
            obj=prism_sdk.IpRange,
            required=True,
        ),
    )

    external_networks_spec = dict(
        default_gateway=dict(
            type="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
        ),
        subnet_mask=dict(
            type="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
        ),
        ip_ranges=dict(
            type="list",
            elements="dict",
            options=ip_ranges_spec,
            obj=prism_sdk.IpRange,
            required=True,
        ),
        network_ext_id=dict(type="str", required=True),
    )

    network_spec = dict(
        external_address=dict(
            type="dict", options=ip_address_spec, obj=prism_sdk.IPAddress
        ),
        name_servers=dict(
            type="list",
            elements="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
        ),
        ntp_servers=dict(
            type="list",
            elements="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
        ),
        internal_networks=dict(
            type="list",
            elements="dict",
            options=internal_networks_spec,
            obj=prism_sdk.BaseNetwork,
        ),
        external_networks=dict(
            type="list",
            elements="dict",
            options=external_networks_spec,
            obj=prism_sdk.ExternalNetwork,
            required=True,
        ),
    )
    prism_spec = dict(
        config=dict(
            type="dict",
            options=config_spec,
            obj=prism_sdk.DomainManagerClusterConfig,
            required=True,
        ),
        network=dict(
            type="dict",
            options=network_spec,
            obj=prism_sdk.DomainManagerNetwork,
            required=True,
        ),
        should_enable_high_availability=dict(type="bool", default=False),
    )

    cluster_reference = dict(
        ext_id=dict(type="str", required=True),
    )

    cluster_location_spec = dict(
        config=dict(
            type="dict",
            options=cluster_reference,
            obj=prism_sdk.ClusterReference,
            required=True,
        ),
    )

    access_key_credentials = dict(
        access_key_id=dict(type="str", required=True),
        secret_access_key=dict(type="str", required=True, no_log=True),
    )

    provider_config_spec = dict(
        bucket_name=dict(type="str", required=True),
        region=dict(type="str", default="us-east-1"),
        credentials=dict(
            type="dict",
            options=access_key_credentials,
            obj=prism_sdk.AccessKeyCredentials,
        ),
    )

    backup_policy_spec = dict(
        rpo_in_minutes=dict(type="int", required=True),
    )

    object_store_location_spec = dict(
        provider_config=dict(
            type="dict",
            options=provider_config_spec,
            obj=prism_sdk.AWSS3Config,
            required=True,
        ),
        backup_policy=dict(
            type="dict",
            options=backup_policy_spec,
            obj=prism_sdk.BackupPolicy,
        ),
    )

    location_spec = dict(
        cluster_location=dict(
            type="dict",
            options=cluster_location_spec,
            obj=prism_sdk.ClusterLocation,
        ),
        object_store_location=dict(
            type="dict",
            options=object_store_location_spec,
            obj=prism_sdk.ObjectStoreLocation,
        ),
    )

    location_backup_spec = dict(
        location=dict(
            type="dict",
            options=location_spec,
            obj=location_allowed_types,
            mutually_exclusive=[("cluster_location", "object_store_location")],
        ),
    )

    @classmethod
    def get_prism_spec(cls):
        return deepcopy(cls.prism_spec)

    @classmethod
    def get_location_backup_spec(cls):
        return deepcopy(cls.location_backup_spec)
