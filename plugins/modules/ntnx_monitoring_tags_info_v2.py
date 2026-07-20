#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_monitoring_tags_info_v2
short_description: Fetch Logbay log-collection tags of a cluster in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Tag in Nutanix Prism Central.
  - Tag here refers to a Logbay log-collection tag (for example C(acropolis), C(cassandra), C(ahv_logs))
    that identifies the component whose logs can be collected for a cluster.
  - The list is scoped to a specific Prism Element cluster via C(cluster_ext_id).
  - Since Tag has no create/update/delete operations, this module exposes list-only functionality.
  - Supports pagination via C(page) and C(limit) and OData filtering via C(filter), C(orderby),
    and C(select) on the C(name) field.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List Logbay tags for a cluster) -
      Required Roles: Prism Admin, Super Admin, Prism Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  cluster_ext_id:
    description:
      - Cluster UUID for which Logbay log collection tags are requested.
      - This is required to scope the list to a specific Prism Element cluster.
    type: str
    required: true
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
- name: List all Logbay tags for a cluster
  nutanix.ncp.ntnx_monitoring_tags_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0005f10c-5a2e-4c86-4c39-ac1f6b3b6a4a"
  register: tags_all
  ignore_errors: true

- name: List Logbay tags filtered by name
  nutanix.ncp.ntnx_monitoring_tags_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0005f10c-5a2e-4c86-4c39-ac1f6b3b6a4a"
    filter: "name eq 'acropolis'"
  register: tags_filtered
  ignore_errors: true

- name: List Logbay tags with pagination
  nutanix.ncp.ntnx_monitoring_tags_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0005f10c-5a2e-4c86-4c39-ac1f6b3b6a4a"
    page: 0
    limit: 10
    orderby: "name asc"
    select: "name"
  register: tags_paginated
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Tag info v4 API.
    - Returns a list of Logbay tags available for the requested cluster.
    - Filter, limit, orderby, select and page parameters are applied when provided.
  returned: always
  type: dict
  sample: [
    {
      "description": "ABAC service logs",
      "ext_id": "6624a35d-3fed-aace-c13f-7af3e51b491f",
      "links": null,
      "name": "abac",
      "tenant_id": null
    },
    {
      "description": "Acropolis log files",
      "ext_id": "93eef4ed-1c91-4a04-3ff9-41e0c4c3a313",
      "links": null,
      "name": "acropolis",
      "tenant_id": null
    },
    {
      "description": "Cassandra log files",
      "ext_id": "121c60df-0c03-083d-2693-c251f15fdfb2",
      "links": null,
      "name": "cassandra",
      "tenant_id": null
    }
  ]

total_available_results:
  description: The total number of Logbay tags available for the cluster.
  type: int
  returned: when all tags are fetched
  sample: 201

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching Logbay tags info"

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

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_cluster_logs_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as monitoring_sdk  # noqa: F401
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as monitoring_sdk  # noqa: F401

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args


def list_monitoring_tags(module, cluster_logs_api, result):
    """List Logbay tags for the given cluster and store the response in result."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Logbay tags info spec", **result)

    kwargs["clusterExtId"] = module.params.get("cluster_ext_id")

    try:
        resp = cluster_logs_api.list_tags(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Logbay tags info",
        )

    total_available_results = getattr(
        getattr(resp, "metadata", None), "total_available_results", None
    )
    result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_monitoring_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    cluster_logs_api = get_cluster_logs_api_instance(module)
    list_monitoring_tags(module, cluster_logs_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
