#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_log_tags_info_v2
short_description: Fetch cluster log tags info in Nutanix Prism Central
version_added: 2.7.0
description:
  - Fetches a list of all available tags for a cluster.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View Tags) -
      Required Roles: Monitoring Admin, Prism Admin, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  cluster_ext_id:
    description:
      - Cluster UUID for which log collection tags are requested.
    type: str
    required: true
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
      - It must be a positive integer between 0 and the maximum number of pages that are available
        for that resource.
      - Any number out of this range might lead to no results.
    type: int
    required: false
  limit:
    description:
      - A URL query parameter that specifies the total number of records returned in the result set.
      - Must be a positive integer between 1 and 100.
      - Any number out of this range will lead to a validation error.
      - If the limit is not provided, a default value of 50 records will be returned in the result set.
    type: int
    required: false
  filter:
    description:
      - The filter in OData syntax used for the results.
    type: str
    required: false
  orderby:
    description:
      - The sort order in which results are returned.
    type: str
    required: false
  select:
    description:
      - The attribute name to select.
    type: str
    required: false
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all cluster log tags
  nutanix.ncp.ntnx_cluster_log_tags_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "b4abfa01-94d4-4cf1-a545-91b3d185ee73"
  register: result

- name: List cluster log tags with filter
  nutanix.ncp.ntnx_cluster_log_tags_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "b4abfa01-94d4-4cf1-a545-91b3d185ee73"
    filter: "name eq 'acropolis'"
  register: result

- name: List cluster log tags with limit
  nutanix.ncp.ntnx_cluster_log_tags_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "b4abfa01-94d4-4cf1-a545-91b3d185ee73"
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - List of cluster log tags.
  returned: always
  type: list
  sample:
    [
      {
        "description": "Acropolis logs",
        "ext_id": "acropolis",
        "name": "acropolis"
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching cluster log tags info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task have failed.
  returned: always
  type: bool
  sample: false

cluster_ext_id:
  description: Cluster UUID for which log collection tags were requested.
  type: str
  returned: always
  sample: "b4abfa01-94d4-4cf1-a545-91b3d185ee73"

total_available_results:
  description: The total number of available cluster log tags.
  type: int
  returned: when cluster log tags are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_cluster_logs_api_instance,
)
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
        cluster_ext_id=dict(type="str", required=True),
        page=dict(type="int"),
        limit=dict(type="int"),
        filter=dict(type="str"),
        orderby=dict(type="str"),
        select=dict(type="str"),
    )

    return module_args


def get_cluster_log_tags(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating cluster log tags info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_tags,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster log tags info",
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
        skip_info_args=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_cluster_logs_api_instance(module)
    get_cluster_log_tags(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
