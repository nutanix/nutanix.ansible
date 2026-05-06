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


def _empty_options():
    """Options dict for SDK marker types that carry no fields."""
    return dict()


def _scalar_value_options():
    """Options dict for SDK ``{value: str}`` wrapper types."""
    return dict(value=dict(type="str"))


def _scalar_secret_value_options():
    """Same as ``_scalar_value_options`` but with ``no_log=True``."""
    return dict(value=dict(type="str", no_log=True))


def _ip_address_options():
    """Options dict for the SDK ``IPv4Address`` type."""
    return dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )


def _logon_count_options():
    """Options dict shared by ``VmGcProfileAutoLogonSettings`` and its override."""
    return dict(logon_count=dict(type="int"))


def _dns_config_options():
    """Options dict shared by ``VmGcProfileDnsConfig`` and its override."""
    return dict(
        preferred_dns_server_address=dict(type="str"),
        alternate_dns_server_addresses=dict(type="list", elements="str"),
    )


def _domain_credentials_options():
    """Options dict shared by ``VmGcProfileDomainCredentials`` and its override."""
    return dict(
        domain_name=dict(type="str"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )


def _workgroup_options():
    """Options dict shared by ``VmGcProfileWorkgroup`` and its override."""
    return dict(name=dict(type="str"))


def _answer_file_options():
    """Options dict shared by ``VmGcProfileAnswerFile`` and its override."""
    return dict(unattend_xml=dict(type="str"))


class VmGuestCustomizationProfileSpecs:
    """Argument spec for the VM Guest Customization Profile resource.

    Used by ``ntnx_vm_guest_customization_profile_v2`` for create/update.
    Models the saved-profile shape: ``VmGuestCustomizationProfile`` and the
    ``VmGcProfile*`` (non-override) SDK types.
    """

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

        computer_name_spec = dict(
            use_vm_name=dict(
                type="dict",
                options=_empty_options(),
                obj=vmm_sdk.VmGcProfileUseVmName,
            ),
            must_provide_during_deployment=dict(
                type="dict",
                options=_empty_options(),
                obj=vmm_sdk.VmGcProfileMustProvideDuringDeployment,
            ),
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
                options=_logon_count_options(),
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

        domain_settings_spec = dict(
            credentials=dict(
                type="dict",
                options=_domain_credentials_options(),
                obj=vmm_sdk.VmGcProfileDomainCredentials,
                no_log=False,
            ),
        )

        workgroup_or_domain_info_spec = dict(
            workgroup=dict(
                type="dict",
                options=_workgroup_options(),
                obj=vmm_sdk.VmGcProfileWorkgroup,
            ),
            domain_settings=dict(
                type="dict",
                options=domain_settings_spec,
                obj=vmm_sdk.VmGcProfileDomainSettings,
            ),
        )

        ipv4_config_spec = dict(
            use_dhcp=dict(
                type="dict",
                options=_empty_options(),
                obj=vmm_sdk.VmGcProfileUseDhcp,
            ),
            must_provide_during_deployment=dict(
                type="dict",
                options=_empty_options(),
                obj=vmm_sdk.VmGcProfileMustProvideDuringDeployment,
            ),
        )

        nic_config_spec = dict(
            dns_config=dict(
                type="dict",
                options=_dns_config_options(),
                obj=vmm_sdk.VmGcProfileDnsConfig,
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

        sysprep_customization_spec = dict(
            sysprep_params=dict(
                type="dict",
                options=sysprep_params_spec,
                obj=vmm_sdk.VmGcProfileSysprepParams,
                no_log=False,
            ),
            answer_file=dict(
                type="dict",
                options=_answer_file_options(),
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


class VmGcProfileOverrideSpecs:
    """Argument spec for per-request VM Guest Customization Profile overrides.

    Used by:

    * ``ntnx_vms_clone_v2`` to populate
      ``CloneOverrideParams.guest_customization_profile_config``.
    * ``ntnx_templates_deploy_v2`` to populate
      ``VmConfigOverride.guest_customization_profile_config`` for each
      ``override_vms_config`` entry.

    Models the ``VmGcProfile*OverrideSpec`` SDK types. The override-spec
    differs from the saved-profile shape in two ways:

    * Most scalar fields are wrapped in a ``OneOf[<value-wrapper>, DiscardSettings]``
      so the caller can either provide a new value per clone/deploy request or
      explicitly discard the value coming from the referenced profile.
    * ``computer_name`` additionally supports ``UseVmNameOverrideSpec`` and
      ``ipv4_config`` supports ``UseDhcpOverrideSpec``.
    """

    computer_name_allowed_types = {
        "name": vmm_sdk.VmGcProfileComputerName,
        "use_vm_name": vmm_sdk.VmGcProfileUseVmNameOverrideSpec,
        "discard": vmm_sdk.VmGcProfileDiscardSettings,
    }

    timezone_allowed_types = {
        "value": vmm_sdk.VmGcProfileTimezone,
        "discard": vmm_sdk.VmGcProfileDiscardSettings,
    }

    administrator_password_allowed_types = {
        "value": vmm_sdk.VmGcProfileAdministratorPassword,
        "discard": vmm_sdk.VmGcProfileDiscardSettings,
    }

    windows_product_key_allowed_types = {
        "value": vmm_sdk.VmGcProfileWindowsProductKey,
        "discard": vmm_sdk.VmGcProfileDiscardSettings,
    }

    registered_owner_allowed_types = {
        "value": vmm_sdk.VmGcProfileRegisteredOwner,
        "discard": vmm_sdk.VmGcProfileDiscardSettings,
    }

    registered_organization_allowed_types = {
        "value": vmm_sdk.VmGcProfileRegisteredOrganization,
        "discard": vmm_sdk.VmGcProfileDiscardSettings,
    }

    locale_setting_allowed_types = {
        "value": vmm_sdk.VmGcProfileLocaleSettingOverride,
        "discard": vmm_sdk.VmGcProfileDiscardSettings,
    }

    workgroup_or_domain_info_allowed_types = {
        "workgroup": vmm_sdk.VmGcProfileWorkgroupOverrideSpec,
        "domain_settings": vmm_sdk.VmGcProfileDomainSettingsOverrideSpec,
        "discard": vmm_sdk.VmGcProfileDiscardSettings,
    }

    nic_ipv4_config_allowed_types = {
        "use_dhcp": vmm_sdk.VmGcProfileUseDhcpOverrideSpec,
        "static_config": vmm_sdk.VmGcProfileNicIpv4ConfigOverrideSpec,
    }

    sysprep_customization_allowed_types = {
        "sysprep_params": vmm_sdk.VmGcProfileSysprepParamsOverrideSpec,
        "answer_file": vmm_sdk.VmGcProfileAnswerFileOverrideSpec,
    }

    @staticmethod
    def _value_or_discard_spec(value_obj, secret=False):
        """Build a OneOf[value-wrapper, DiscardSettings] options dict."""
        options = _scalar_secret_value_options() if secret else _scalar_value_options()
        value_entry = dict(type="dict", options=options, obj=value_obj)
        if secret:
            value_entry["no_log"] = False
        return dict(
            value=value_entry,
            discard=dict(
                type="dict",
                options=_empty_options(),
                obj=vmm_sdk.VmGcProfileDiscardSettings,
            ),
        )

    @classmethod
    def get_module_spec(cls):

        computer_name_spec = dict(
            name=dict(
                type="dict",
                options=_scalar_value_options(),
                obj=vmm_sdk.VmGcProfileComputerName,
            ),
            use_vm_name=dict(
                type="dict",
                options=_empty_options(),
                obj=vmm_sdk.VmGcProfileUseVmNameOverrideSpec,
            ),
            discard=dict(
                type="dict",
                options=_empty_options(),
                obj=vmm_sdk.VmGcProfileDiscardSettings,
            ),
        )

        general_settings_spec = dict(
            computer_name=dict(
                type="dict",
                options=computer_name_spec,
                obj=cls.computer_name_allowed_types,
                mutually_exclusive=[("name", "use_vm_name", "discard")],
            ),
            timezone=dict(
                type="dict",
                options=cls._value_or_discard_spec(vmm_sdk.VmGcProfileTimezone),
                obj=cls.timezone_allowed_types,
                mutually_exclusive=[("value", "discard")],
            ),
            administrator_password=dict(
                type="dict",
                options=cls._value_or_discard_spec(
                    vmm_sdk.VmGcProfileAdministratorPassword, secret=True
                ),
                obj=cls.administrator_password_allowed_types,
                no_log=False,
                mutually_exclusive=[("value", "discard")],
            ),
            auto_logon_settings=dict(
                type="dict",
                options=_logon_count_options(),
                obj=vmm_sdk.VmGcProfileAutoLogonSettingsOverrideSpec,
            ),
            windows_product_key=dict(
                type="dict",
                options=cls._value_or_discard_spec(
                    vmm_sdk.VmGcProfileWindowsProductKey, secret=True
                ),
                obj=cls.windows_product_key_allowed_types,
                no_log=False,
                mutually_exclusive=[("value", "discard")],
            ),
            registered_owner=dict(
                type="dict",
                options=cls._value_or_discard_spec(vmm_sdk.VmGcProfileRegisteredOwner),
                obj=cls.registered_owner_allowed_types,
                mutually_exclusive=[("value", "discard")],
            ),
            registered_organization=dict(
                type="dict",
                options=cls._value_or_discard_spec(
                    vmm_sdk.VmGcProfileRegisteredOrganization
                ),
                obj=cls.registered_organization_allowed_types,
                mutually_exclusive=[("value", "discard")],
            ),
        )

        locale_settings_spec = dict(
            user_locale=dict(
                type="dict",
                options=cls._value_or_discard_spec(
                    vmm_sdk.VmGcProfileLocaleSettingOverride
                ),
                obj=cls.locale_setting_allowed_types,
                mutually_exclusive=[("value", "discard")],
            ),
            system_locale=dict(
                type="dict",
                options=cls._value_or_discard_spec(
                    vmm_sdk.VmGcProfileLocaleSettingOverride
                ),
                obj=cls.locale_setting_allowed_types,
                mutually_exclusive=[("value", "discard")],
            ),
            ui_language=dict(
                type="dict",
                options=cls._value_or_discard_spec(
                    vmm_sdk.VmGcProfileLocaleSettingOverride
                ),
                obj=cls.locale_setting_allowed_types,
                mutually_exclusive=[("value", "discard")],
            ),
        )

        domain_settings_spec = dict(
            credentials=dict(
                type="dict",
                options=_domain_credentials_options(),
                obj=vmm_sdk.VmGcProfileDomainCredentialsOverrideSpec,
                no_log=False,
            ),
        )

        workgroup_or_domain_info_spec = dict(
            workgroup=dict(
                type="dict",
                options=_workgroup_options(),
                obj=vmm_sdk.VmGcProfileWorkgroupOverrideSpec,
            ),
            domain_settings=dict(
                type="dict",
                options=domain_settings_spec,
                obj=vmm_sdk.VmGcProfileDomainSettingsOverrideSpec,
                no_log=False,
            ),
            discard=dict(
                type="dict",
                options=_empty_options(),
                obj=vmm_sdk.VmGcProfileDiscardSettings,
            ),
        )

        nic_ipv4_static_config_spec = dict(
            ip_address=dict(
                type="dict",
                options=_ip_address_options(),
                obj=vmm_sdk.IPv4Address,
            ),
            default_gateways=dict(type="list", elements="str"),
        )

        ipv4_config_spec = dict(
            use_dhcp=dict(
                type="dict",
                options=_empty_options(),
                obj=vmm_sdk.VmGcProfileUseDhcpOverrideSpec,
            ),
            static_config=dict(
                type="dict",
                options=nic_ipv4_static_config_spec,
                obj=vmm_sdk.VmGcProfileNicIpv4ConfigOverrideSpec,
            ),
        )

        nic_config_spec = dict(
            dns_config=dict(
                type="dict",
                options=_dns_config_options(),
                obj=vmm_sdk.VmGcProfileDnsConfigOverrideSpec,
            ),
            ipv4_config=dict(
                type="dict",
                options=ipv4_config_spec,
                obj=cls.nic_ipv4_config_allowed_types,
                mutually_exclusive=[("use_dhcp", "static_config")],
            ),
        )

        network_settings_spec = dict(
            nic_config_list=dict(
                type="list",
                elements="dict",
                options=nic_config_spec,
                obj=vmm_sdk.VmGcProfileNicConfigOverrideSpec,
            ),
        )

        sysprep_params_spec = dict(
            general_settings=dict(
                type="dict",
                options=general_settings_spec,
                obj=vmm_sdk.VmGcProfileGeneralSettingsOverrideSpec,
                no_log=False,
            ),
            first_logon_commands=dict(type="list", elements="str"),
            locale_settings=dict(
                type="dict",
                options=locale_settings_spec,
                obj=vmm_sdk.VmGcProfileLocaleSettingsOverrideSpec,
            ),
            workgroup_or_domain_info=dict(
                type="dict",
                options=workgroup_or_domain_info_spec,
                obj=cls.workgroup_or_domain_info_allowed_types,
                no_log=False,
                mutually_exclusive=[
                    ("workgroup", "domain_settings", "discard"),
                ],
            ),
            network_settings=dict(
                type="dict",
                options=network_settings_spec,
                obj=vmm_sdk.VmGcProfileNetworkSettingsOverrideSpec,
            ),
        )

        sysprep_customization_spec = dict(
            sysprep_params=dict(
                type="dict",
                options=sysprep_params_spec,
                obj=vmm_sdk.VmGcProfileSysprepParamsOverrideSpec,
                no_log=False,
            ),
            answer_file=dict(
                type="dict",
                options=_answer_file_options(),
                obj=vmm_sdk.VmGcProfileAnswerFileOverrideSpec,
            ),
        )

        config_override_spec = dict(
            customization=dict(
                type="dict",
                options=sysprep_customization_spec,
                obj=cls.sysprep_customization_allowed_types,
                no_log=False,
                mutually_exclusive=[("sysprep_params", "answer_file")],
            ),
        )

        profile_reference_spec = dict(
            ext_id=dict(type="str", required=True),
        )

        return dict(
            profile=dict(
                type="dict",
                options=profile_reference_spec,
                obj=vmm_sdk.VmGcProfileReference,
            ),
            config_override_spec=dict(
                type="dict",
                options=config_override_spec,
                obj=vmm_sdk.VmGcProfileSysprepConfigOverrideSpec,
                no_log=False,
            ),
        )

    @classmethod
    def get_guest_customization_profile_config_spec(cls):
        return cls.get_module_spec()
