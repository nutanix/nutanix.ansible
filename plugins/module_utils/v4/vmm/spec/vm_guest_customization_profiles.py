# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ...sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


class VmGuestCustomizationProfileSpecs:
    """Module specs related to VM Guest Customization Profiles."""

    sysprep_customization_allowed_types = {
        "sysprep_params": vmm_sdk.VmGcProfileSysprepParams,
        "answer_file": vmm_sdk.VmGcProfileAnswerFile,
    }

    computer_name_allowed_types = {
        "use_vm_name": vmm_sdk.VmGcProfileUseVmName,
        "must_provide_during_deployment": vmm_sdk.VmGcProfileMustProvideDuringDeployment,
    }

    workgroup_or_domain_info_allowed_types = {
        "workgroup": vmm_sdk.VmGcProfileWorkgroup,
        "domain_settings": vmm_sdk.VmGcProfileDomainSettings,
    }

    nic_ipv4_config_allowed_types = {
        "use_dhcp": vmm_sdk.VmGcProfileUseDhcp,
        "must_provide_during_deployment": vmm_sdk.VmGcProfileMustProvideDuringDeployment,
    }

    config_allowed_types = {
        "sysprep": vmm_sdk.VmGcProfileSysprepConfig,
    }

    empty_marker_keys = (
        "use_vm_name",
        "must_provide_during_deployment",
        "use_dhcp",
    )

    @classmethod
    def get_module_spec(cls):

        use_vm_name_spec = dict()
        must_provide_during_deployment_spec = dict()
        use_dhcp_spec = dict()

        computer_name_spec = dict(
            use_vm_name=dict(
                type="dict", options=use_vm_name_spec, obj=vmm_sdk.VmGcProfileUseVmName
            ),
            must_provide_during_deployment=dict(
                type="dict",
                options=must_provide_during_deployment_spec,
                obj=vmm_sdk.VmGcProfileMustProvideDuringDeployment,
            ),
        )

        auto_logon_settings_spec = dict(
            logon_count=dict(type="int"),
        )

        general_settings_spec = dict(
            computer_name=dict(
                type="dict",
                options=computer_name_spec,
                obj=cls.computer_name_allowed_types,
                mutually_exclusive=[
                    ("use_vm_name", "must_provide_during_deployment"),
                ],
            ),
            timezone=dict(type="str"),
            administrator_password=dict(type="str", no_log=True),
            auto_logon_settings=dict(
                type="dict",
                options=auto_logon_settings_spec,
                obj=vmm_sdk.VmGcProfileAutoLogonSettings,
            ),
            windows_product_key=dict(type="str", no_log=True),
            registered_owner=dict(type="str"),
            registered_organization=dict(type="str"),
        )

        locale_settings_spec = dict(
            user_locale=dict(type="str"),
            system_locale=dict(type="str"),
            ui_language=dict(type="str"),
        )

        domain_credentials_spec = dict(
            domain_name=dict(type="str"),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
        )

        domain_settings_spec = dict(
            credentials=dict(
                type="dict",
                options=domain_credentials_spec,
                obj=vmm_sdk.VmGcProfileDomainCredentials,
                no_log=False,
            ),
        )

        workgroup_spec = dict(
            name=dict(type="str"),
        )

        workgroup_or_domain_info_spec = dict(
            workgroup=dict(
                type="dict", options=workgroup_spec, obj=vmm_sdk.VmGcProfileWorkgroup
            ),
            domain_settings=dict(
                type="dict",
                options=domain_settings_spec,
                obj=vmm_sdk.VmGcProfileDomainSettings,
            ),
        )

        dns_config_spec = dict(
            preferred_dns_server_address=dict(type="str"),
            alternate_dns_server_addresses=dict(type="list", elements="str"),
        )

        ipv4_config_spec = dict(
            use_dhcp=dict(
                type="dict", options=use_dhcp_spec, obj=vmm_sdk.VmGcProfileUseDhcp
            ),
            must_provide_during_deployment=dict(
                type="dict",
                options=must_provide_during_deployment_spec,
                obj=vmm_sdk.VmGcProfileMustProvideDuringDeployment,
            ),
        )

        nic_config_spec = dict(
            dns_config=dict(
                type="dict", options=dns_config_spec, obj=vmm_sdk.VmGcProfileDnsConfig
            ),
            ipv4_config=dict(
                type="dict",
                options=ipv4_config_spec,
                obj=cls.nic_ipv4_config_allowed_types,
                mutually_exclusive=[
                    ("use_dhcp", "must_provide_during_deployment"),
                ],
            ),
        )

        network_settings_spec = dict(
            nic_config_list=dict(
                type="list",
                elements="dict",
                options=nic_config_spec,
                obj=vmm_sdk.VmGcProfileNicConfig,
            ),
        )

        sysprep_params_spec = dict(
            general_settings=dict(
                type="dict",
                options=general_settings_spec,
                obj=vmm_sdk.VmGcProfileGeneralSettings,
                no_log=False,
            ),
            first_logon_commands=dict(type="list", elements="str"),
            locale_settings=dict(
                type="dict",
                options=locale_settings_spec,
                obj=vmm_sdk.VmGcProfileLocaleSettings,
            ),
            workgroup_or_domain_info=dict(
                type="dict",
                options=workgroup_or_domain_info_spec,
                obj=cls.workgroup_or_domain_info_allowed_types,
                no_log=False,
                mutually_exclusive=[
                    ("workgroup", "domain_settings"),
                ],
            ),
            network_settings=dict(
                type="dict",
                options=network_settings_spec,
                obj=vmm_sdk.VmGcProfileNetworkSettings,
            ),
        )

        answer_file_spec = dict(
            unattend_xml=dict(type="str"),
        )

        sysprep_customization_spec = dict(
            sysprep_params=dict(
                type="dict",
                options=sysprep_params_spec,
                obj=vmm_sdk.VmGcProfileSysprepParams,
                no_log=False,
            ),
            answer_file=dict(
                type="dict",
                options=answer_file_spec,
                obj=vmm_sdk.VmGcProfileAnswerFile,
            ),
        )

        sysprep_config_spec = dict(
            customization=dict(
                type="dict",
                options=sysprep_customization_spec,
                obj=cls.sysprep_customization_allowed_types,
                no_log=False,
                mutually_exclusive=[
                    ("sysprep_params", "answer_file"),
                ],
            ),
        )

        config_spec = dict(
            sysprep=dict(
                type="dict",
                options=sysprep_config_spec,
                obj=vmm_sdk.VmGcProfileSysprepConfig,
                no_log=False,
            ),
        )

        module_args = dict(
            ext_id=dict(type="str"),
            name=dict(type="str"),
            description=dict(type="str"),
            config=dict(
                type="dict",
                options=config_spec,
                obj=cls.config_allowed_types,
                no_log=False,
            ),
        )

        return module_args
