#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_monitoring_events_info_v2
short_description: Fetch monitoring Event(s) from Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about Event in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Event.
  - If C(ext_id) is not provided, list multiple Event optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external ID (UUID) of the generated event.
      - If provided, fetch details of the specific Event.
    type: str
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get Event by ext_id) -
    Required Permission: View_Event. Suitable Roles include Prism Viewer, Operator, and Prism Central Admin.
  - >-
    B(List Events) -
    Required Permission: View_Event. Suitable Roles include Prism Viewer, Operator, and Prism Central Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""
EXAMPLES = r"""
- name: Get monitoring event using ext_id
  nutanix.ncp.ntnx_monitoring_events_info_v2:
    ext_id: "b6e58bb9-1cbf-4e37-8c8d-9a2a19b7bbb1"
  register: result
  ignore_errors: true

- name: List all monitoring events
  nutanix.ncp.ntnx_monitoring_events_info_v2:
  register: result
  ignore_errors: true

- name: List monitoring events with filter on eventType
  nutanix.ncp.ntnx_monitoring_events_info_v2:
    filter: "eventType eq 'ClusterAnomalyAudit'"
  register: result
  ignore_errors: true

- name: List monitoring events with limit and pagination
  nutanix.ncp.ntnx_monitoring_events_info_v2:
    limit: 5
    page: 0
  register: result
  ignore_errors: true

- name: List monitoring events sorted by creationTime descending
  nutanix.ncp.ntnx_monitoring_events_info_v2:
    orderby: "creationTime desc"
  register: result
  ignore_errors: true

- name: List monitoring events with select projection
  nutanix.ncp.ntnx_monitoring_events_info_v2:
    select: "extId,eventType,creationTime,sourceEntity"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Event info v4 API.
    - It can be a single Event if external ID is provided.
    - List of multiple Event if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "affected_entities": null,
      "classifications": ["Storage", "UserAction"],
      "cluster_name": "auto_cluster_prod_36acf9b012ca",
      "cluster_uuid": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "creation_time": "2026-07-20T13:53:20.211796+00:00",
      "event_type": "ContainerAudit",
      "ext_id": "fe096096-df86-48df-a75a-1fffa525aa0a",
      "links": null,
      "message": "Marked Storage Container {container_name} for removal",
      "metric_details": null,
      "operation_type": null,
      "parameters": [
          {
              "param_name": "container_name",
              "param_value": {
                  "string_value": "ansible_storage_container_example_updated"
              }
          },
          {
              "param_name": "audit_user",
              "param_value": {"string_value": "admin"}
          }
      ],
      "service_name": null,
      "source_cluster_uuid": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "source_entity": null,
      "tenant_id": null,
      "title": "Marked Storage Container ansible_storage_container_example_updated for removal"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the Event.
  type: str
  returned: when external ID is provided
  sample: "b6e58bb9-1cbf-4e37-8c8d-9a2a19b7bbb1"

total_available_results:
  description: The total number of available Events in PC.
  type: int
  returned: when all events are listed
  sample: 42

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching monitoring events info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_events_api_instance,
)
from ..module_utils.v4.monitoring.helpers import get_event  # noqa: E402
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


def get_event_using_ext_id(module, events_api, result):
    ext_id = module.params.get("ext_id")
    resp = get_event(module, events_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_events(module, events_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating monitoring events info spec", **result)

    try:
        resp = events_api.list_events(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching monitoring events info",
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
    events_api = get_events_api_instance(module)
    if module.params.get("ext_id"):
        get_event_using_ext_id(module, events_api, result)
    else:
        get_events(module, events_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
