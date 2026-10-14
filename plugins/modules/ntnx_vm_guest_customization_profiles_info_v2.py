#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vm_guest_customization_profiles_info_v2
short_description: Fetch information about VM Guest Customization Profile(s)
description:
  - This module fetches information about Nutanix VM Guest Customization Profile(s).
  - Fetch a specific VM Guest Customization Profile using external ID.
  - Fetch the list of VM Guest Customization Profiles if external ID is not provided with optional filter.
  - This module uses PC v4 APIs based SDKs.
version_added: "2.6.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get the VM Guest Customization Profile for this extId) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, Virtual Machine Admin, Virtual Machine Viewer
    - >-
      B(Get the list of existing VM Guest Customization Profiles.) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, Virtual Machine Admin, Virtual Machine Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID of the VM Guest Customization Profile.
    type: str
    required: false
author:
  - George Ghawali (@george-ghawali)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: List all VM Guest Customization Profiles
  nutanix.ncp.ntnx_vm_guest_customization_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List VM Guest Customization Profiles with filter
  nutanix.ncp.ntnx_vm_guest_customization_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'win-sysprep-profile'"
  register: result

- name: List VM Guest Customization Profiles with limit
  nutanix.ncp.ntnx_vm_guest_customization_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: Get details of a specific VM Guest Customization Profile
  nutanix.ncp.ntnx_vm_guest_customization_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "a3265671-de53-41be-af9b-f06241b95356"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response for fetching VM Guest Customization Profile(s).
    - Single profile if external ID is provided.
    - List of multiple VM Guest Customization Profiles if external ID is not provided.
  type: dict
  returned: always
  sample:
    {
      "config": {
          "customization": {
              "first_logon_commands": [
                  "powershell -Command Enable-PSRemoting -Force",
                  "powershell -Command Set-ExecutionPolicy RemoteSigned -Force"
              ],
              "general_settings": {
                  "administrator_password": "MASKED_FIELD",
                  "auto_logon_settings": null,
                  "computer_name": {},
                  "registered_organization": "admin Updated",
                  "registered_owner": "admin Updated",
                  "timezone": "Eastern Standard Time",
                  "windows_product_key": null
              },
              "locale_settings": {
                  "system_locale": "en-GB",
                  "ui_language": "en-GB",
                  "user_locale": "en-GB"
              },
              "network_settings": {
                  "nic_config_list": [
                      {
                          "dns_config": {
                              "alternate_dns_server_addresses": [
                                  "10.0.0.51"
                              ],
                              "preferred_dns_server_address": "10.0.0.50"
                          },
                          "ipv4_config": {}
                      }
                  ]
              },
              "workgroup_or_domain_info": {
                  "name": "QA"
              }
          }
      },
      "create_time": "2026-05-05T11:26:57.496782+00:00",
      "created_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000"
      },
      "description": "Updated sysprep profile description",
      "ext_id": "08bed846-7bf2-48b5-5c92-741500be3a3f",
      "links": null,
      "name": "vm_gc_profile_ansible_test_sysprep_WQOHNIIZdzzT_updated",
      "tenant_id": null,
      "update_time": "2026-05-05T11:27:21.493223+00:00",
      "updated_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000"
      }
    }
changed:
  description: Indicates if the module made any changes.
  returned: always
  type: bool
  sample: true
failed:
  description: Indicates if the module failed.
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM Guest Customization Profiles info"
error:
  description: Error message if any error occurs.
  type: str
  returned: always
ext_id:
  description: The external ID of the VM Guest Customization Profile that was fetched.
  type: str
  returned: when fetching a specific profile
  sample: "a3265671-de53-41be-af9b-f06241b95356"
total_available_results:
  description: The total number of available VM Guest Customization Profiles in the PC.
  type: int
  returned: when listing all profiles
  sample: 10
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_guest_customization_profiles_api_instance,
)
from ..module_utils.v4.vmm.helpers import (  # noqa: E402
    get_vm_guest_customization_profile,
)


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_profile_using_ext_id(module, profiles, result):
    ext_id = module.params.get("ext_id")
    resp = get_vm_guest_customization_profile(
        module=module,
        api_instance=profiles,
        ext_id=ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_profiles(module, profiles, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM Guest Customization Profiles info Spec", **result
        )

    try:
        resp = profiles.list_vm_guest_customization_profiles(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM Guest Customization Profiles info",
        )
    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    profiles = get_vm_guest_customization_profiles_api_instance(module)
    if module.params.get("ext_id"):
        get_profile_using_ext_id(module, profiles, result)
    else:
        get_profiles(module, profiles, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
