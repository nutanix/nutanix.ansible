#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vcenter_extensions_info_v2
short_description: Retrieve information about vCenter server extensions from Nutanix Prism Central
version_added: "2.6.0"
description:
    - This module retrieves information about vCenter server extensions from Nutanix Prism Central.
    - Fetch particular vCenter extension info using external ID.
    - Fetch multiple vCenter extensions info with/without using filters, limit, etc.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get vCenter extension by ext_id) -
      Operation Name: View VCenter Extension -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List vCenter extensions) -
      Operation Name: View VCenter Extension -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The globally unique identifier of vCenter Server extension instance. It should be of type UUID.
      - If not provided, multiple vCenter extension records will be fetched.
    type: str
    required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch vCenter extension info using external ID
  nutanix.ncp.ntnx_vcenter_extensions_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  register: result

- name: Fetch all vCenter extensions info
  nutanix.ncp.ntnx_vcenter_extensions_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: result

- name: Fetch vCenter extensions with filter
  nutanix.ncp.ntnx_vcenter_extensions_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    filter: "isRegistered eq true"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VcenterExtension info v4 API.
    - It can be a single VcenterExtension if external ID is provided.
    - List of multiple VcenterExtension if external ID is not provided.
  type: dict
  returned: always
  sample:
    {
      "cluster_ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
      "ext_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "ip_address": "10.0.0.1",
      "is_registered": true
    }
changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false
ext_id:
  description: The external ID of the vCenter extension if given in input.
  type: str
  returned: when single entity
  sample: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
msg:
  description: Status or error message.
  returned: contextual
  type: str
  sample: "Api Exception raised while fetching vCenter extensions info"
error:
  description: Error details.
  returned: always
  type: str
  sample: null
failed:
  description: True on failure.
  returned: when something fails
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_vcenter_extensions_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_vcenter_extension  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_vcenter_extension_by_ext_id(module, api_instance, result):
    """
    Fetch a single vCenter extension by external ID.
    Args:
        module: AnsibleModule instance
        api_instance: VcenterExtensionsApi instance
        result (dict): Module result dict
    """
    ext_id = module.params.get("ext_id")
    resp = get_vcenter_extension(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_vcenter_extensions(module, api_instance, result):
    """
    List all vCenter extensions.
    Args:
        module: AnsibleModule instance
        api_instance: VcenterExtensionsApi instance
        result (dict): Module result dict
    """
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(module.params)
    if err:
        module.fail_json(
            msg="Failed creating query parameters for fetching vCenter extensions info"
        )
    resp = None
    try:
        resp = api_instance.list_vcenter_extensions(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vCenter extensions info",
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
        skip_info_args=False,
        mutually_exclusive=[("ext_id", "filter")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_vcenter_extensions_api_instance(module)
    if module.params.get("ext_id"):
        get_vcenter_extension_by_ext_id(module, api_instance, result)
    else:
        list_vcenter_extensions(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
