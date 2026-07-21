#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_data_protection_cluster_capabilities_info_v2
short_description: Fetch data protection cluster capabilities in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about DataProtectionClusterCapability in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific DataProtectionClusterCapability.
  - If C(ext_id) is not provided, list multiple DataProtectionClusterCapability optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get data protection cluster capabilities) -
    Required Roles: Backup Admin, Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer,
    Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
  ext_id:
    description:
      - The external ID of the DataProtectionClusterCapability entity.
      - This is the cluster UUID whose data protection capabilities are being retrieved.
      - When provided, only the capabilities for the matching cluster are returned.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get data protection cluster capabilities using ext_id
  nutanix.ncp.ntnx_data_protection_cluster_capabilities_info_v2:
    ext_id: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true

- name: List all data protection cluster capabilities
  nutanix.ncp.ntnx_data_protection_cluster_capabilities_info_v2:
  register: result
  ignore_errors: true

- name: List data protection cluster capabilities with filter on extId
  nutanix.ncp.ntnx_data_protection_cluster_capabilities_info_v2:
    filter: "extId eq '0006555e-4e63-4a5e-185b-ac1f6b6f97e2'"
  register: result
  ignore_errors: true

- name: List data protection cluster capabilities with limit
  nutanix.ncp.ntnx_data_protection_cluster_capabilities_info_v2:
    limit: 1
  register: result
  ignore_errors: true

- name: List data protection cluster capabilities with pagination
  nutanix.ncp.ntnx_data_protection_cluster_capabilities_info_v2:
    page: 0
    limit: 10
  register: result
  ignore_errors: true

- name: List data protection cluster capabilities selecting only extId and clusterExtId
  nutanix.ncp.ntnx_data_protection_cluster_capabilities_info_v2:
    select: "extId,clusterExtId"
  register: result
  ignore_errors: true

- name: List data protection cluster capabilities ordered by extId
  nutanix.ncp.ntnx_data_protection_cluster_capabilities_info_v2:
    orderby: "extId"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC DataProtectionClusterCapability info v4 API.
    - It can be a single DataProtectionClusterCapability if external ID is provided.
    - List of multiple DataProtectionClusterCapability if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "capabilities": [
          {
              "capability_name": "SUPPORTS_NEAR_SYNC",
              "is_supported": true
          },
          {
              "capability_name": "SUPPORTS_POLICY_BASED_RP_RETENTION",
              "is_supported": true
          }
      ],
      "cluster_ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "links": null,
      "tenant_id": null
    }

ext_id:
  description:
    - The external ID of the DataProtectionClusterCapability entity.
  returned: when external ID is provided
  type: str
  sample: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"

total_available_results:
  description:
    - The total number of available DataProtectionClusterCapability entities in PC.
  returned: when listing all DataProtectionClusterCapability entities
  type: int
  sample: 1

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, or DataProtectionClusterCapability is not found by C(ext_id).
  type: str
  sample: "Api Exception raised while fetching data protection cluster capabilities info"

error:
  description:
    - This field typically holds information about any error that occurred during the task execution.
  returned: when an error occurs
  type: str

failed:
  description: This field typically holds information about whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_data_protection_cluster_capabilities_api_instance,
)
from ..module_utils.v4.data_protection.helpers import (  # noqa: E402
    get_data_protection_cluster_capability,
)
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


def get_data_protection_cluster_capability_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    entity = get_data_protection_cluster_capability(module, api_instance, ext_id)
    if entity is None:
        module.fail_json(
            msg=(
                "DataProtectionClusterCapability with ext_id '{0}' not found.".format(
                    ext_id
                )
            ),
            **result,
        )
    result["response"] = strip_internal_attributes(entity.to_dict())


def list_data_protection_cluster_capabilities(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating data protection cluster capabilities info spec",
            **result,
        )

    try:
        resp = api_instance.list_data_protection_cluster_capabilities(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching data protection cluster capabilities info",
        )

    total_available_results = None
    if resp is not None and resp.metadata is not None:
        total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data") if resp else None
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_data_protection_cluster_capabilities_api_instance(module)
    if module.params.get("ext_id"):
        get_data_protection_cluster_capability_using_ext_id(
            module, api_instance, result
        )
    else:
        list_data_protection_cluster_capabilities(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
