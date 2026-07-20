#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_alerts_info_v2
short_description: Fetch information about Alerts in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Alert in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Alert.
  - If C(ext_id) is not provided, list multiple Alert optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get an Alert by ext_id) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin
  - >-
    B(List Alerts) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the Alert.
      - When provided, fetch a single Alert by its external ID.
    type: str
    required: false
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
- name: Fetch an Alert using ext_id
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "1e8b6c9c-4a1e-4b7b-9f9e-5c1e2a3b4c5d"
  register: result
  ignore_errors: true

- name: List all Alerts
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List Alerts filtered on severity
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "severity eq Monitoring.Serviceability.Severity'CRITICAL'"
  register: result
  ignore_errors: true

- name: List Alerts ordered by creationTime desc, limited to first page
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    orderby: "creationTime desc"
    limit: 5
    page: 0
  register: result
  ignore_errors: true

- name: List Alerts selecting only a few fields
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    select: "extId,severity,title,isResolved"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Alert info v4 API.
    - It can be a single Alert if external ID is provided.
    - List of multiple Alert if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "acknowledged_by_username": null,
      "acknowledged_time": null,
      "affected_entities": null,
      "alert_type": "A130200",
      "classifications": [
        "System Indicator"
      ],
      "cluster_name": "cluster-a",
      "cluster_uuid": "0006361b-6855-3644-7458-2268f8ffb2bd",
      "creation_time": "2026-07-19T05:36:52.146000+00:00",
      "ext_id": "1e8b6c9c-4a1e-4b7b-9f9e-5c1e2a3b4c5d",
      "impact_types": [
        "Availability"
      ],
      "is_acknowledged": false,
      "is_auto_resolved": false,
      "is_resolved": false,
      "is_runnable": false,
      "is_user_defined": false,
      "kb_articles": null,
      "last_updated_time": "2026-07-19T05:36:52.146000+00:00",
      "links": null,
      "message": "Sample alert message",
      "metric_details": null,
      "originating_cluster_uuid": "0006361b-6855-3644-7458-2268f8ffb2bd",
      "parameters": null,
      "resolved_by_username": null,
      "resolved_time": null,
      "root_cause_analysis": null,
      "service_name": "Prism Central",
      "severity": "kInfo",
      "severity_trails": null,
      "source_entity": {
        "ext_id": "0006361b-6855-3644-7458-2268f8ffb2bd",
        "name": "cluster-a",
        "type": "cluster"
      },
      "tenant_id": null,
      "title": "Sample alert title"
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
  sample: "Api Exception raised while fetching alerts info"

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
  description: External ID of the Alert.
  type: str
  returned: when external ID is provided
  sample: "1e8b6c9c-4a1e-4b7b-9f9e-5c1e2a3b4c5d"

total_available_results:
  description: The total number of available Alerts in Prism Central.
  type: int
  returned: when Alerts are listed (ext_id not provided)
  sample: 42
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_alerts_api_instance,
)
from ..module_utils.v4.monitoring.helpers import get_alert  # noqa: E402
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


def get_alert_using_ext_id(module, alerts, result):
    ext_id = module.params.get("ext_id")
    resp = get_alert(module, alerts, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_alerts(module, alerts, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating alerts info spec", **result)

    try:
        resp = alerts.list_alerts(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching alerts info",
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
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    alerts = get_alerts_api_instance(module)
    if module.params.get("ext_id"):
        get_alert_using_ext_id(module, alerts, result)
    else:
        get_alerts(module, alerts, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
