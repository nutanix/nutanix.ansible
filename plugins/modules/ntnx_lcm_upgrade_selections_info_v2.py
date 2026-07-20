#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_upgrade_selections_info_v2
short_description: Fetch LCM Upgrade Selection info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about UpgradeSelection in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific UpgradeSelection.
  - If C(ext_id) is not provided, list multiple UpgradeSelection optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get LCM upgrade selection by ext_id) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - >-
      B(Get list of LCM upgrade selections) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  ext_id:
    description:
      - The external ID of the LCM Upgrade Selection.
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
- name: Get LCM upgrade selection using ext_id
  nutanix.ncp.ntnx_lcm_upgrade_selections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b7dbcf46-8ba3-4dcd-a7c3-4b09b0f7a11a"
  register: result
  ignore_errors: true

- name: List all LCM upgrade selections
  nutanix.ncp.ntnx_lcm_upgrade_selections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List LCM upgrade selections with filter
  nutanix.ncp.ntnx_lcm_upgrade_selections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "status eq Lifecycle.Resources.UpgradeSelectionStatus'UPGRADE_READY'"
  register: result
  ignore_errors: true

- name: List LCM upgrade selections with limit
  nutanix.ncp.ntnx_lcm_upgrade_selections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC UpgradeSelection info v4 API.
    - It can be a single UpgradeSelection if external ID is provided.
    - List of multiple UpgradeSelection if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "00062e00-87eb-ef15-0000-00000000b71a",
      "ext_id": "b7dbcf46-8ba3-4dcd-a7c3-4b09b0f7a11a",
      "links": null,
      "selected_upgrades": [
        {
          "entity_uuid": "15570c98-beaf-4633-afd2-b6a306ff1001",
          "to_version": "5.0.0"
        }
      ],
      "status": "UPGRADE_READY",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching LCM upgrade selections info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the LCM upgrade selection.
  type: str
  returned: When external ID is provided
  sample: "b7dbcf46-8ba3-4dcd-a7c3-4b09b0f7a11a"

total_available_results:
  description: The total number of available LCM upgrade selections in PC.
  type: int
  returned: When all LCM upgrade selections are fetched
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_upgrade_selections_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_upgrade_selection  # noqa: E402
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


def get_upgrade_selection_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    entity = get_upgrade_selection(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(entity.to_dict())


def list_upgrade_selections(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating LCM upgrade selections info spec", **result
        )

    try:
        resp = api_instance.list_upgrade_selections(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM upgrade selections info",
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
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_upgrade_selections_api_instance(module)
    if module.params.get("ext_id"):
        get_upgrade_selection_using_ext_id(module, api_instance, result)
    else:
        list_upgrade_selections(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
