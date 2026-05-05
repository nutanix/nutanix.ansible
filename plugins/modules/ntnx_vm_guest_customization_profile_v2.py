#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_guest_customization_profile_v2
short_description: Create, update and delete VM Guest Customization Profiles in Nutanix Prism Central
version_added: 2.6.0
description:
  - Create, update and delete VM Guest Customization Profiles.
  - A VM Guest Customization Profile is a reusable template that describes how to customize
    a guest operating system at deployment-time (currently Windows Sysprep, either by
    specifying parameters individually or by providing an unattend XML file).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a VM Guest Customization Profile.) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - >-
      B(Update the specified VM Guest Customization Profile.) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - >-
      B(Delete the specified VM Guest Customization Profile.) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - >-
      Profiles created by this module are consumed by
      M(nutanix.ncp.ntnx_vms_clone_v2) and M(nutanix.ncp.ntnx_templates_deploy_v2)
      via their C(guest_customization_profile_config) option. For the profile to
      be applied successfully at clone or deploy time, Nutanix Guest Tools (NGT)
      must be installed on the source VM (or the source VM that backs the
      template); otherwise, the corresponding clone or deploy request will be
      rejected by the API.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - If C(state) is present, it will create or update the VM guest customization profile.
      - If C(state) is set to C(present) and C(ext_id) is not provided, the operation will create the profile.
      - If C(state) is set to C(present) and C(ext_id) is provided, the operation will update the profile.
      - If C(state) is set to C(absent) and C(ext_id) is provided, the operation will delete the profile.
    type: str
    choices: ["present", "absent"]
  ext_id:
    description:
      - VM Guest Customization Profile external ID.
      - Required for updating or deleting the profile.
    type: str
  name:
    description:
      - Name of the VM Guest Customization Profile.
      - Required for creating a profile.
    type: str
  description:
    description:
      - A description of the VM Guest Customization Profile.
    type: str
  config:
    description:
      - The customization configuration that will be applied to the guest OS.
      - Currently only Windows Sysprep customization is supported.
    type: dict
    suboptions:
      sysprep:
        description:
          - Configuration of the VM Guest Customization Profile for customization of a Windows guest operating system.
        type: dict
        suboptions:
          customization:
            description:
              - Either specify the values for the parameters (sysprep_params) or an unattend XML file (answer_file).
              - C(sysprep_params) and C(answer_file) are mutually exclusive.
            type: dict
            suboptions:
              sysprep_params:
                description:
                  - A set of various unattended settings supported by Windows Sysprep.
                  - The Windows unattend XML file is generated based on the values provided for these elements.
                type: dict
                suboptions:
                  general_settings:
                    description:
                      - Generic Windows installation settings such as computer name, timezone, product key,
                        registered owner/organization and the administrator password.
                    type: dict
                    suboptions:
                      computer_name:
                        description:
                          - Mechanism to use to generate the computer name of the VM.
                          - Either UseVmName or MustProvideDuringDeployment should be provided.
                          - If MustProvideDuringDeployment is specified, then the user must provide the value for the computer name during the VM deployment;
                            otherwise, the deployment request fails.
                          - If the UseVmName is specified, then during VM deployment, the name of the VM needs to meet the sysprep's computer name
                            requirements; otherwise, the request fails.
                        type: dict
                        suboptions:
                          use_vm_name:
                            description:
                              - Use the VM name as the computer name.
                              - Specify C(use_vm_name) with no value or with an empty dictionary to enable this option.
                            type: dict
                          must_provide_during_deployment:
                            description:
                              - Indicates that this value must be provided during deployment.
                              - Specify C(must_provide_during_deployment) with no value or with an empty dictionary to enable this option.
                            type: dict
                      timezone:
                        description:
                          - The computer's time zone in string format.
                          - For different timezone values, refer to the Windows unattend installation documentation.
                        type: str
                      administrator_password:
                        description:
                          - Password to be configured for built-in Administrator account.
                        type: str
                      auto_logon_settings:
                        description:
                          - Autologon settings that need to be specified to enable autologon.
                            Currently, it is for only the Administrator account, and the value for the Administrator Password should be provided in the
                            General Settings section when configuring this setting.
                        type: dict
                        suboptions:
                          logon_count:
                            description:
                              - The number of automatic logons allowed for the computer using the specified local account.
                              - The C(logon_count) must be specified if the C(auto_logon_settings) is used.
                            type: int
                      windows_product_key:
                        description:
                          - The product key to use to install and activate Windows.
                          - Note that entering an invalid product key causes Windows Setup to fail.
                        type: str
                      registered_owner:
                        description:
                          - Full name of the end user. Note that this is the full name in the format, not only the username.
                        type: str
                      registered_organization:
                        description:
                          - Name of the organization of the end user.
                        type: str
                  first_logon_commands:
                    description:
                      - List of commands to be executed automatically when a user logs in for the first time after Windows setup.
                      - This is an ordered list. The first command in the list is given the order as 1, and so on,
                        in FirstLogonCommands in the generated unattend XML.
                      - For more information, refer to Windows unattend installation documentation.
                    type: list
                    elements: str
                  locale_settings:
                    description:
                      - Language and locale settings for the system and the user.
                    type: dict
                    suboptions:
                      user_locale:
                        description:
                          - Per-user settings to be used for formatting dates, times, currency, and numbers.
                          - Its value is based on the language-tagging conventions of RFC 3066.
                          - The pattern language-region is used, where language is a language code and region is a country or region identifier.
                        type: str
                      system_locale:
                        description:
                          - Default language to use for non-Unicode programs.
                          - Its value is based on the language-tagging conventions of RFC 3066.
                          - The pattern language-region is used, where language is a language code and region is a country or region identifier.
                        type: str
                      ui_language:
                        description:
                          - Default system language to use to display user interface (UI) items.
                          - Its value is based on the language-tagging conventions of RFC 3066.
                          - The pattern language-region is used, where language is a language code and region is a country or region identifier.
                        type: str
                  workgroup_or_domain_info:
                    description:
                      - Either join a workgroup or join an Active Directory domain.
                      - C(workgroup) and C(domain_settings) are mutually exclusive.
                    type: dict
                    suboptions:
                      workgroup:
                        description:
                          - Workgroup configuration of the computer.
                        type: dict
                        suboptions:
                          name:
                            description:
                              - Name of workgroup to be applied to the computer when joining the workgroup. It must be a valid NetBIOS name.
                            type: str
                      domain_settings:
                        description:
                          - Domain Settings Configuration.
                        type: dict
                        suboptions:
                          credentials:
                            description:
                              - Credentials of the domain account to use to join the domain.
                            type: dict
                            suboptions:
                              domain_name:
                                description:
                                  - The name of the domain to use for authentication of the account before the computer
                                    can be joined to a domain. A domain name can be the fully qualified DNS name or the NetBIOS name of the domain.
                                type: str
                              username:
                                description:
                                  - Name of the domain user account with permission to add the computer to a domain.
                                type: str
                              password:
                                description:
                                  - The password of the domain user account to use for authenticating an account to the domain before
                                    the computer can be joined to a domain.
                                type: str
                  network_settings:
                    description:
                      - Network settings to apply to the NICs attached to the VM.
                    type: dict
                    suboptions:
                      nic_config_list:
                        description:
                          - List of NIC configurations to be applied to the NICs attached to the VM in serial order.
                          - The first configuration provided in the list is applied to the first NIC attached to the VM, and so on for other NICs.
                        type: list
                        elements: dict
                        suboptions:
                          dns_config:
                            description:
                              - DNS configuration to be applied to the NIC.
                            type: dict
                            suboptions:
                              preferred_dns_server_address:
                                description:
                                  - An IPv4 address is preferred to search first when searching for the DNS server on the network.
                                type: str
                              alternate_dns_server_addresses:
                                description:
                                  - List of IPv4 addresses to look for after preferred DNS server when searching for the DNS server on the network.
                                type: list
                                elements: str
                          ipv4_config:
                            description:
                              - Mechanism to configure IPv4 settings of the NIC.
                              - Either UseDhcp or MustProvideDuringDeployment should be specified as a value.
                              - If UseDhcp is specified, DhcpEnabled is set to True for the interface in the unattend XML.
                              - If MustProvideDuringDeployment is specified, the IPv4 address, prefix length, and gateway must be supplied during deployment.
                              - C(use_dhcp) and C(must_provide_during_deployment) are mutually exclusive.
                            type: dict
                            suboptions:
                              use_dhcp:
                                description:
                                  - The NIC will obtain its IPv4 address via DHCP.
                                  - Specify C(use_dhcp) with no value or with an empty dictionary to enable this option.
                                type: dict
                              must_provide_during_deployment:
                                description:
                                  - The IPv4 configuration must be provided at deployment-time.
                                  - Specify C(must_provide_during_deployment) with no value or with an empty dictionary to enable this option.
                                type: dict
              answer_file:
                description:
                  - A pre-built Windows unattend XML file used as the customization input.
                type: dict
                suboptions:
                  unattend_xml:
                    description:
                      - The unattend XML file as a string value.
                      - Note that double quotes in the XML file need to be escaped to maintain correctness.
                      - The XML file needs to be Base64 encoded (e.g. using the Ansible C(b64encode) filter).
                    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create VM Guest Customization Profile with sysprep params (Workgroup join, DHCP)
  nutanix.ncp.ntnx_vm_guest_customization_profile_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: "win-sysprep-profile"
    description: "Windows Sysprep profile description"
    config:
      sysprep:
        customization:
          sysprep_params:
            general_settings:
              computer_name:
                use_vm_name:
              timezone: "Pacific Standard Time"
              administrator_password: "admin123"
              registered_owner: "admin"
              registered_organization: "admin"
            locale_settings:
              user_locale: "en-US"
              system_locale: "en-US"
              ui_language: "en-US"
            first_logon_commands:
              - "powershell -Command Enable-PSRemoting -Force"
            workgroup_or_domain_info:
              workgroup:
                name: "workgroup"
            network_settings:
              nic_config_list:
                - dns_config:
                    preferred_dns_server_address: "8.8.8.8"
                    alternate_dns_server_addresses:
                      - "8.8.4.4"
                  ipv4_config:
                    use_dhcp:

- name: Create VM Guest Customization Profile with an unattend XML answer file
  nutanix.ncp.ntnx_vm_guest_customization_profile_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: "answer-file-profile"
    description: "Answer file profile description"
    config:
      sysprep:
        customization:
          answer_file:
            unattend_xml: "{{ lookup('file', 'unattend.xml') | b64encode }}"

- name: Update VM Guest Customization Profile (switch to domain join, must-provide IP)
  nutanix.ncp.ntnx_vm_guest_customization_profile_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "a3265671-de53-41be-af9b-f06241b95356"
    name: "sysprep-profile-domain-updated"
    description: "Updated profile description"
    config:
      sysprep:
        customization:
          sysprep_params:
            general_settings:
              computer_name:
                must_provide_during_deployment: {}
              timezone: "UTC"
              administrator_password: "admin123"
            workgroup_or_domain_info:
              domain_settings:
                credentials:
                  domain_name: "domain.com"
                  username: "admin"
                  password: "admin123"
            network_settings:
              nic_config_list:
                - ipv4_config:
                    must_provide_during_deployment: {}

- name: Delete VM Guest Customization Profile
  nutanix.ncp.ntnx_vm_guest_customization_profile_v2:
    state: absent
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "a3265671-de53-41be-af9b-f06241b95356"
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating or deleting the VM Guest Customization Profile.
    - VM Guest Customization Profile details if C(wait) is true and the operation is create or update.
    - Task details if C(wait) is false or the operation is delete.
  type: dict
  returned: always
  sample:
    {
      "config": {
          "customization": {
              "first_logon_commands": [
                  "powershell -Command Enable-PSRemoting -Force"
              ],
              "general_settings": {
                  "administrator_password": "MASKED_FIELD",
                  "auto_logon_settings": null,
                  "computer_name": {},
                  "registered_organization": "admin",
                  "registered_owner": "admin",
                  "timezone": "Pacific Standard Time",
                  "windows_product_key": null
              },
              "locale_settings": {
                  "system_locale": "en-US",
                  "ui_language": "en-US",
                  "user_locale": "en-US"
              },
              "network_settings": {
                  "nic_config_list": [
                      {
                          "dns_config": {
                              "alternate_dns_server_addresses": [
                                  "10.0.0.11"
                              ],
                              "preferred_dns_server_address": "10.0.0.10"
                          },
                          "ipv4_config": {}
                      }
                  ]
              },
              "workgroup_or_domain_info": {
                  "name": "workgroup"
              }
          }
      },
      "create_time": "2026-05-05T11:26:57.496782+00:00",
      "created_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000"
      },
      "description": "Sysprep profile created by integration tests",
      "ext_id": "08bed846-7bf2-48b5-5c92-741500be3a3f",
      "links": null,
      "name": "vm_gc_profile_ansible_test_sysprep_WQOHNIIZdzzT",
      "tenant_id": null,
      "update_time": "2026-05-05T11:26:57.496782+00:00",
      "updated_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000"
      }
    }
ext_id:
  description:
    - External ID of the VM Guest Customization Profile.
  type: str
  returned: always
task_ext_id:
  description: Task External ID
  returned: always
  type: str
  sample: "ZXJnb24=:350f0fd5-097d-4ece-8f44-6e5bfbe2dc08"
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating VM Guest Customization Profile"
error:
  description: Error message if any
  returned: always
  type: str
changed:
  description: Indicates if the module made any changes
  returned: always
  type: bool
  sample: true
failed:
  description: Indicates if the module failed
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    remove_fields_from_spec,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_vm_guest_customization_profiles_api_instance,
)
from ..module_utils.v4.vmm.helpers import (  # noqa: E402
    get_vm_guest_customization_profile,
)
from ..module_utils.v4.vmm.spec.vm_guest_customization_profiles import (  # noqa: E402
    VmGuestCustomizationProfileSpecs as profile_specs,
)

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    return profile_specs.get_module_spec()


def normalize_oneof_marker_values(params):
    """Normalize one-of marker variants from ``null`` to ``{}``.

    The empty-marker variants (``use_vm_name``, ``must_provide_during_deployment``,
    ``use_dhcp``) map to SDK classes with no user-facing fields; the variant is
    selected purely by *which* key is present. Users may write either
    ``use_vm_name: {}`` or simply ``use_vm_name:`` (null) in their playbook.
    The latter form would otherwise be stripped by ``remove_param_with_none_value``
    before the spec generator could dispatch it, so we promote ``null`` to ``{}``
    for known marker keys here.
    """
    marker_keys = profile_specs.empty_marker_keys
    if isinstance(params, dict):
        for key, value in params.items():
            if key in marker_keys and value is None:
                params[key] = {}
            elif isinstance(value, dict):
                normalize_oneof_marker_values(value)
            elif isinstance(value, list):
                for item in value:
                    normalize_oneof_marker_values(item)


def create_profile(module, result, profiles):
    validate_required_params(module, ["config"])
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.VmGuestCustomizationProfile()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create VM Guest Customization Profile spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = profiles.create_vm_guest_customization_profile(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating VM Guest Customization Profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task,
            rel=TASK_CONSTANTS.RelEntityType.VM_GUEST_CUSTOMIZATION_PROFILE,
        )
        if ext_id:
            resp = get_vm_guest_customization_profile(module, profiles, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


SECRET_FIELDS = {"administrator_password", "windows_product_key", "password"}


def check_idempotency(current_spec, update_spec):
    current_dict = (
        current_spec.to_dict() if hasattr(current_spec, "to_dict") else current_spec
    )
    update_dict = (
        update_spec.to_dict() if hasattr(update_spec, "to_dict") else update_spec
    )
    strip_internal_attributes(current_dict)
    strip_internal_attributes(update_dict)
    remove_fields_from_spec(current_dict, SECRET_FIELDS, deep=True)
    remove_fields_from_spec(update_dict, SECRET_FIELDS, deep=True)
    return current_dict == update_dict


def update_profile(module, result, profiles):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_vm_guest_customization_profile(module, profiles, ext_id=ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating VM Guest Customization Profile",
            **result,
        )

    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM Guest Customization Profile update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    result["current_spec"] = strip_internal_attributes(current_spec.to_dict())
    result["update_spec"] = strip_internal_attributes(update_spec.to_dict())

    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = profiles.update_vm_guest_customization_profile_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating VM Guest Customization Profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_vm_guest_customization_profile(module, profiles, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_profile(module, result, profiles):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "VM Guest Customization Profile with ext_id:{0} will be deleted.".format(
                ext_id
            )
        )
        return

    current_spec = get_vm_guest_customization_profile(module, profiles, ext_id=ext_id)
    etag = get_etag(data=current_spec)
    kwargs = {"if_match": etag} if etag else {}

    try:
        resp = profiles.delete_vm_guest_customization_profile_by_id(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting VM Guest Customization Profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    normalize_oneof_marker_values(module.params)
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    profiles = get_vm_guest_customization_profiles_api_instance(module)
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_profile(module, result, profiles)
        else:
            create_profile(module, result, profiles)
    else:
        delete_profile(module, result, profiles)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
