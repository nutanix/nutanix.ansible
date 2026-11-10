#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_alerts_info_v2
short_description: Fetch alerts info in Nutanix Prism Central
version_added: 2.7.0
description:
  - Fetch details of an alert identified by external ID.
  - List alerts optionally filtered or paginated when C(ext_id) is not provided.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get alert by ext_id) -
      Required Roles: Account Owner, Administrator, Disaster Recovery Admin, Disaster Recovery Viewer,
      Files Admin, Files Viewer, Flow Admin, Flow Policy Author, Flow Viewer, Monitoring Admin,
      Monitoring Viewer, NCM Connector, Prism Admin, Prism Viewer, Project Admin, Project Manager,
      Super Admin, Tenant Admin, Tenant Consumer
    - >-
      B(List all the alerts) -
      Required Roles: Account Owner, Administrator, Disaster Recovery Admin, Disaster Recovery Viewer,
      Files Admin, Files Viewer, Flow Admin, Flow Policy Author, Flow Viewer, Monitoring Admin,
      Monitoring Viewer, NCM Connector, Prism Admin, Prism Viewer, Project Admin, Project Manager,
      Super Admin, Tenant Admin, Tenant Consumer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  ext_id:
    description:
      - UUID of the generated alert.
      - When set, only the referenced alert is returned.
    type: str
  expand:
    description:
      - A URL query parameter that allows clients to request related resources when a resource
        that satisfies a particular request is retrieved.
      - Supported expand values are C(project) and C(shared_with_projects).
    type: str
  apply:
    description:
      - A URL query parameter that allows clients to specify a sequence of transformations to the
        entity set, such as groupby, orderby, aggregate etc.
      - For example C(groupby((property))) will get the entity set grouped by "property".
      - The sequence must start with groupby, which may include multiple nested aggregates.
        It may optionally be followed by orderby and/or pagination parameters.
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
- name: Get alert using ext_id
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "af3a40be-d079-454a-968a-9903d1bf0549"
  register: result

- name: Get alert using ext_id with expand
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "af3a40be-d079-454a-968a-9903d1bf0549"
    expand: "project"
  register: result

- name: List all alerts
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List alerts with filter
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "isResolved eq false"
  register: result

- name: List alerts with limit
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List alerts with apply
  nutanix.ncp.ntnx_alerts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    apply: "groupby((severity))"
  register: result

- name: List all alerts with fetch_all
  nutanix.ncp.ntnx_alerts_info_v2:
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
    - The response from the Nutanix PC alerts info v4 API.
    - It can be a single alert if external ID is provided.
    - List of multiple alerts if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "alert_type": "A802005",
      "cluster_uuid": "c54feb73-6b69-4d70-ace4-7df5bae94e1f",
      "creation_time": "2026-11-10T01:56:42.850645+00:00",
      "ext_id": "bb9f7753-2492-4b64-98d3-cfef0ca60fff",
      "is_acknowledged": true,
      "is_resolved": true,
      "severity": "CRITICAL",
      "title": "Network gateway gw_ansible_izvwiHdzjnCJ_all is down"
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
  description: This indicates whether the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the alert.
  type: str
  returned: when external ID is provided
  sample: "af3a40be-d079-454a-968a-9903d1bf0549"

total_available_results:
  description: The total number of available alerts in PC.
  type: int
  returned: when all alerts are fetched
  sample: 5
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
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        expand=dict(type="str"),
        apply=dict(type="str"),
    )

    return module_args


def get_alert_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    expand = module.params.get("expand")
    resp = get_alert(module, api_instance, ext_id, expand=expand)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_alerts(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand", "apply"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating alerts info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_alerts,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching alerts info",
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
            ("ext_id", "apply"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_alerts_api_instance(module)
    if module.params.get("ext_id"):
        get_alert_using_ext_id(module, api_instance, result)
    else:
        get_alerts(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
