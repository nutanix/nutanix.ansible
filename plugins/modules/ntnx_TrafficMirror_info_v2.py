#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_TrafficMirror_info_v2
short_description: Fetch Traffic mirror session info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch Traffic mirror sessions info or a specific Traffic mirror session in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch a specific Traffic mirror session using external ID.
  - If C(ext_id) is not provided, fetch multiple Traffic mirror sessions info with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Traffic mirror session by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin.
    - >-
      B(List Traffic mirror sessions) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the Traffic mirror session.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get Traffic mirror session using ext_id
  nutanix.ncp.ntnx_TrafficMirror_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "3f8b1c2d-2e3f-4a5b-6c7d-8e9f0a1b2c3d"
  register: result
  ignore_errors: true

- name: List all Traffic mirror sessions
  nutanix.ncp.ntnx_TrafficMirror_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List Traffic mirror sessions with filter
  nutanix.ncp.ntnx_TrafficMirror_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'traffic_mirror_ansible'"
  register: result
  ignore_errors: true

- name: List Traffic mirror sessions with limit
  nutanix.ncp.ntnx_TrafficMirror_info_v2:
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
    - The response from the Nutanix PC TrafficMirror info v4 API.
    - It can be a single TrafficMirror if external ID is provided.
    - List of multiple TrafficMirror if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_reference_list": ["bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"],
      "description": "Traffic mirror session created by Ansible",
      "destination_list": [
          {
              "is_up": true,
              "nic_type": "VIRTUAL_NIC",
              "nic_uuid": "b4376782-ef64-52cf-bc0c-a17352ca6467"
          }
      ],
      "ext_id": "3f8b1c2d-2e3f-4a5b-6c7d-8e9f0a1b2c3d",
      "host_reference_list": null,
      "is_enabled": true,
      "links": null,
      "metadata": null,
      "name": "traffic_mirror_ansible",
      "source_list": [
          {
              "direction": "BIDIRECTIONAL",
              "is_up": true,
              "nic_type": "VIRTUAL_NIC",
              "nic_uuid": "a3265671-de53-41be-af9b-f06241b95356"
          }
      ],
      "state": "ACTIVE",
      "state_message": null,
      "tenant_id": null,
      "virtual_switch_reference": "2e40ff57-20aa-4d2b-b179-298db969c20d"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Status message describing the outcome of the operation.
  returned: when there is an error
  type: str
  sample: "Api Exception raised while fetching Traffic mirror session info"

error:
  description: Error details when an error occurs during the operation.
  type: str
  returned: when an error occurs

failed:
  description: Indicates whether the module operation failed.
  returned: when the operation fails
  type: bool
  sample: false

ext_id:
  description: External ID of the Traffic mirror session (only returned on get-by-ID).
  type: str
  returned: when external ID is provided
  sample: "3f8b1c2d-2e3f-4a5b-6c7d-8e9f0a1b2c3d"

total_available_results:
  description: The total number of available Traffic mirror sessions in PC.
  type: int
  returned: when Traffic mirror sessions are listed
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


def get_traffic_mirror_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_traffic_mirror(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_traffic_mirrors(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Traffic mirror sessions info spec", **result
        )

    try:
        resp = api_instance.list_traffic_mirrors(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Traffic mirror sessions info",
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
    result = {"changed": False, "response": None, "failed": False, "error": None}
    api_instance = get_traffic_mirrors_api_instance(module)
    if module.params.get("ext_id"):
        get_traffic_mirror_by_ext_id(module, api_instance, result)
    else:
        get_traffic_mirrors(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
