#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_events_info_v2
short_description: Fetch events info in Nutanix Prism Central
version_added: 2.7.0
description:
  - Fetch details of an event identified by external ID.
  - List events optionally filtered or paginated when C(ext_id) is not provided.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get event by ext_id) -
      Required Roles: Files Admin, Files Viewer, Monitoring Admin, Monitoring Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - >-
      B(List all the events) -
      Required Roles: Backup Admin, Files Admin, Files Viewer, Monitoring Admin, Monitoring Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  ext_id:
    description:
      - UUID of the generated event.
      - When set, only the referenced event is returned.
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
- name: Get event using ext_id
  nutanix.ncp.ntnx_events_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "32632d45-b7f8-4969-b284-c01c032f7c33"
  register: result

- name: List all events
  nutanix.ncp.ntnx_events_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List events with filter
  nutanix.ncp.ntnx_events_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "eventType eq 'MulticlusterAudit'"
  register: result

- name: List events with limit
  nutanix.ncp.ntnx_events_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List all events with fetch_all
  nutanix.ncp.ntnx_events_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC events info v4 API.
    - It can be a single event if external ID is provided.
    - List of multiple events if external ID is not provided with optional filter or limit.
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
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching events info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the event.
  type: str
  returned: when external ID is provided
  sample: "32632d45-b7f8-4969-b284-c01c032f7c33"

total_available_results:
  description: The total number of available events in PC.
  type: int
  returned: when all events are fetched
  sample: 5
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
    list_entities,
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


def get_event_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_event(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_events(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating events info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_events,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching events info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

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
    api_instance = get_events_api_instance(module)
    if module.params.get("ext_id"):
        get_event_using_ext_id(module, api_instance, result)
    else:
        get_events(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
