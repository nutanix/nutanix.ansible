#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_traffic_mirrors_info_v2
short_description: Fetch traffic mirror sessions info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about TrafficMirror in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific TrafficMirror.
  - If C(ext_id) is not provided, list multiple TrafficMirror optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get traffic mirror by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin
    - >-
      B(List traffic mirror sessions) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the traffic mirror session.
    type: str
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
- name: Get traffic mirror session using ext_id
  nutanix.ncp.ntnx_traffic_mirrors_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result

- name: List all traffic mirror sessions
  nutanix.ncp.ntnx_traffic_mirrors_info_v2:
  register: result

- name: List traffic mirror sessions with filter
  nutanix.ncp.ntnx_traffic_mirrors_info_v2:
    filter: "name eq 'tm_ansible_local'"
  register: result

- name: List traffic mirror sessions with limit
  nutanix.ncp.ntnx_traffic_mirrors_info_v2:
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC TrafficMirror info v4 API.
    - It can be a single TrafficMirror if external ID is provided.
    - List of multiple TrafficMirror if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_reference_list": [
          "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
      ],
      "description": "Traffic mirror session created by Ansible",
      "destination_list": [
          {
              "is_up": true,
              "nic_type": "VIRTUAL_NIC",
              "nic_uuid": "5d2ac2b8-b60a-4de6-9345-6f34e79e7a19"
          }
      ],
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "host_reference_list": [
          "8300384a-56ee-4750-aeb8-3d1c42908bee"
      ],
      "is_enabled": true,
      "links": null,
      "metadata": null,
      "name": "tm_ansible_local",
      "source_list": [
          {
              "direction": "BIDIRECTIONAL",
              "is_up": true,
              "nic_type": "VIRTUAL_NIC",
              "nic_uuid": "b1f8ce4b-6c8a-4d13-9c8f-8e2d1a1f8b3e"
          }
      ],
      "state": "ACTIVE",
      "state_message": null,
      "tenant_id": null,
      "virtual_switch_reference": null
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
  sample: "Api Exception raised while fetching traffic mirror info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the traffic mirror session.
  type: str
  returned: when external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: The total number of available traffic mirror sessions in PC.
  type: int
  returned: when all traffic mirror sessions are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_traffic_mirrors_api_instance,
)
from ..module_utils.v4.network.helpers import get_traffic_mirror  # noqa: E402
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


def get_traffic_mirror_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_traffic_mirror(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_traffic_mirrors(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating traffic mirrors info spec", **result)

    try:
        resp = api_instance.list_traffic_mirrors(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching traffic mirrors info",
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
    api_instance = get_traffic_mirrors_api_instance(module)
    if module.params.get("ext_id"):
        get_traffic_mirror_using_ext_id(module, api_instance, result)
    else:
        get_traffic_mirrors(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
