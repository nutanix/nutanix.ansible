# Copyright: (c) 2025, Nutanix
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


class ClusterProfileSpecs:
    """Module specs related to cluster profile and its sub entities"""

    ipv4_address = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    fqdn = dict(value=dict(type="str", required=False))

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
            type="dict",
            options=ip_address_or_fqdn,
            obj=clusters_sdk.IPAddressOrFQDN,
            required=True,
        ),
        port=dict(type="int"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )

    users_spec = dict(
        username=dict(type="str", required=True),
        auth_type=dict(
            type="str",
            choices=["MD5", "SHA"],
            obj=clusters_sdk.SnmpAuthType,
            required=True,
        ),
        auth_key=dict(type="str", required=True, no_log=True),
        priv_type=dict(
            type="str",
            choices=["DES", "AES"],
            obj=clusters_sdk.SnmpPrivType,
        ),
        priv_key=dict(type="str", no_log=True),
    )

    protocol_spec = dict(
        type="str",
        required=True,
        choices=["UDP", "TCP", "UDP6", "TCP6"],
        obj=clusters_sdk.SnmpProtocol,
    )

    traps_spec = dict(
        address=dict(
            type="dict", options=ip_address, obj=clusters_sdk.IPAddress, required=True
        ),
        username=dict(type="str"),
        protocol=protocol_spec,
        port=dict(type="int"),
        should_inform=dict(type="bool"),
        engine_id=dict(type="str", required=False),
        version=dict(
            type="str",
            required=True,
            choices=["V2", "V3"],
            obj=clusters_sdk.SnmpTrapVersion,
        ),
        reciever_name=dict(type="str"),
        community_string=dict(type="str", required=False),
    )

    modules_spec = dict(
        name=dict(
            type="str",
            obj=clusters_sdk.RsyslogModuleName,
            choices=[
                "AUDIT",
                "CALM",
                "MINERVA_CVM",
                "STARGATE",
                "FLOW_SERVICE_LOGS",
                "SYSLOG_MODULE",
                "CEREBRO",
                "API_AUDIT",
                "GENESIS",
                "PRISM",
                "ZOOKEEPER",
                "FLOW",
                "EPSILON",
                "ACROPOLIS",
                "UHARA",
                "LCM",
                "APLOS",
                "NCM_AIOPS",
                "CURATOR",
                "CASSANDRA",
                "LAZAN",
            ],
            required=True,
        ),
        log_severity_level=dict(
            type="str",
            obj=clusters_sdk.RsyslogModuleLogSeverityLevel,
            choices=[
                "EMERGENCY",
                "NOTICE",
                "ERROR",
                "ALERT",
                "INFO",
                "WARNING",
                "DEBUG",
                "CRITICAL",
            ],
            required=True,
        ),
        should_log_monitor_files=dict(type="bool"),
    )

    rsyslog_server_spec = dict(
        server_name=dict(type="str", required=True),
        ip_address=dict(
            type="dict", options=ip_address, obj=clusters_sdk.IPAddress, required=True
        ),
        port=dict(type="int", required=True),
        network_protocol=dict(
            type="str",
            required=True,
            choices=["UDP", "TCP", "RELP"],
            obj=clusters_sdk.RsyslogNetworkProtocol,
        ),
        modules=dict(
            type="list",
            elements="dict",
            obj=clusters_sdk.RsyslogModuleItem,
            options=modules_spec,
        ),
    )
    transports_spec = dict(
        protocol=protocol_spec,
        port=dict(type="int", required=True),
    )
    snmp_config_spec = dict(
        is_enabled=dict(type="bool"),
        users=dict(
            type="list",
            elements="dict",
            options=users_spec,
            obj=clusters_sdk.SnmpUser,
        ),
        transports=dict(
            type="list",
            elements="dict",
            options=transports_spec,
            obj=clusters_sdk.SnmpTransport,
        ),
        traps=dict(
            type="list", elements="dict", options=traps_spec, obj=clusters_sdk.SnmpTrap
        ),
    )

    pulse_status_spec = dict(
        is_enabled=dict(type="bool"),
        pii_scrubbing_level=dict(
            type="str", choices=["ALL", "DEFAULT"], obj=clusters_sdk.PIIScrubbingLevel
        ),
    )

    smtp_server_spec = dict(
        email_address=dict(type="str", required=True),
        server=dict(
            type="dict",
            options=smtp_network,
            obj=clusters_sdk.SmtpNetwork,
            required=True,
        ),
        type=dict(
            type="str", choices=["PLAIN", "STARTTLS", "SSL"], obj=clusters_sdk.SmtpType
        ),
    )

    cluster_profile = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        allowed_overrides=dict(
            type="list",
            elements="str",
            obj=clusters_sdk.ConfigType,
            choices=[
                "NFS_SUBNET_WHITELIST_CONFIG",
                "NTP_SERVER_CONFIG",
                "SNMP_SERVER_CONFIG",
                "SMTP_SERVER_CONFIG",
                "PULSE_CONFIG",
                "NAME_SERVER_CONFIG",
                "RSYSLOG_SERVER_CONFIG",
            ],
        ),
        name_server_ip_list=dict(
            type="list",
            elements="dict",
            options=ip_address,
            obj=clusters_sdk.IPAddress,
        ),
        ntp_server_ip_list=dict(
            type="list",
            elements="dict",
            options=ip_address_or_fqdn,
            obj=clusters_sdk.IPAddressOrFQDN,
        ),
        smtp_server=dict(
            type="dict", options=smtp_server_spec, obj=clusters_sdk.SmtpServerRef
        ),
        nfs_subnet_whitelist=dict(type="list", elements="str"),
        snmp_config=dict(
            type="dict", options=snmp_config_spec, obj=clusters_sdk.SnmpConfig
        ),
        rsyslog_server_list=dict(
            type="list",
            elements="dict",
            options=rsyslog_server_spec,
            obj=clusters_sdk.RsyslogServer,
        ),
        pulse_status=dict(
            type="dict", options=pulse_status_spec, obj=clusters_sdk.PulseStatus
        ),
    )

    @classmethod
    def get_cluster_profile_spec(cls):
        return deepcopy(cls.cluster_profile)
