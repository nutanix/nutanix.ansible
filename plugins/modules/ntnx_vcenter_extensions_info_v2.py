#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vcenter_extensions_info_v2
short_description: Fetch vCenter Server extensions info from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VcenterExtension in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VcenterExtension.
  - If C(ext_id) is not provided, list multiple VcenterExtension optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get vCenter Server extension by ext_id) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(Get list of vCenter Server extensions) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the vCenter Server extension (UUID).
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get vCenter Server extension using ext_id
  nutanix.ncp.ntnx_vcenter_extensions_info_v2:
    ext_id: "00061c8b-2f6e-4a1c-8b41-abc123abc123"
  register: result

- name: List all vCenter Server extensions
  nutanix.ncp.ntnx_vcenter_extensions_info_v2:
  register: result

- name: List vCenter Server extensions with a filter
  nutanix.ncp.ntnx_vcenter_extensions_info_v2:
    filter: "isRegistered eq true"
  register: result

- name: List vCenter Server extensions with a limit
  nutanix.ncp.ntnx_vcenter_extensions_info_v2:
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VcenterExtension info v4 API.
    - It can be a single VcenterExtension if external ID is provided.
    - List of multiple VcenterExtension if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "ext_id": "00061c8b-2f6e-4a1c-8b41-abc123abc123",
      "ip_address": "10.10.10.20",
      "is_registered": true,
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching vCenter extensions info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the vCenter Server extension
  type: str
  returned: when external ID is provided
  sample: "00061c8b-2f6e-4a1c-8b41-abc123abc123"

total_available_results:
  description: The total number of available vCenter Server extensions in PC.
  type: int
  returned: when all vCenter Server extensions are fetched
  sample: 0
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_vcenter_extension_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_vcenter_extension(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_vcenter_extensions(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vCenter extensions info spec", **result)

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
        mutually_exclusive=[
            ("ext_id", "filter"),
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
            ("ext_id", "select"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vcenter_extensions_api_instance(module)
    if module.params.get("ext_id"):
        get_vcenter_extension_using_ext_id(module, api_instance, result)
    else:
        get_vcenter_extensions(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
