#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_collect_logs_info_v2
short_description: Fetch log-collection tags for a Nutanix cluster
version_added: 2.7.0
description:
    - This module allows you to fetch information about CollectLog in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific CollectLog.
    - If C(ext_id) is not provided, list multiple CollectLog optionally filtered / paginated.
    - The listed items are Logbay tags supported by the referenced cluster;
      the tag external IDs returned by this module can be plugged into
      C(include_tags) / C(exclude_tags) of the C(ntnx_monitoring_collect_log_v2)
      module.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(List log-collection tags) -
      Required Roles: Prism Viewer, Prism Admin, Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
    cluster_ext_id:
        description:
            - External ID (UUID) of the Nutanix cluster whose log-collection
              tags are requested. This maps to the C(clusterExtId) path
              parameter of the List tags API.
        type: str
        required: true
    ext_id:
        description:
            - External ID of the log-collection tag to fetch. When
              provided, the module fetches the full tag list on the
              cluster and returns only the entry whose C(ext_id) matches.
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
- name: List all log-collection tags on the cluster
  nutanix.ncp.ntnx_collect_logs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
  register: result

- name: List log-collection tags with filter and limit
  nutanix.ncp.ntnx_collect_logs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    filter: "startswith(name, 'cluster')"
    limit: 5

- name: Fetch a single log-collection tag by ext_id
  nutanix.ncp.ntnx_collect_logs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    ext_id: "cluster_health_logs"
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC CollectLog info v4 API.
        - It can be a single CollectLog if external ID is provided.
        - List of multiple CollectLog if external ID is not provided with
          optional filter or limit.
    returned: always
    type: dict
    sample:
        [
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
            }
        ]

changed:
    description: Always False for info modules.
    returned: always
    type: bool
    sample: false

failed:
    description: True on failure.
    returned: always
    type: bool
    sample: false

ext_id:
    description: External ID of the log-collection tag when a single entity is requested.
    returned: when C(ext_id) is provided
    type: str
    sample: "6624a35d-3fed-aace-c13f-7af3e51b491f"

total_available_results:
    description: Total number of tags available on the cluster.
    returned: when listing all tags
    type: int
    sample: 201

msg:
    description: Status or error message.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching log-collection tags"

error:
    description: Detailed error information if the operation failed.
    returned: When an error occurs
    type: str
"""

import warnings  # noqa: E402

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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )

    return module_args


def _list_tags(module, api_instance, list_kwargs):
    cluster_ext_id = module.params.get("cluster_ext_id")
    try:
        resp = api_instance.list_tags(clusterExtId=cluster_ext_id, **list_kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching log-collection tags",
        )
    return resp


def get_tag_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = _list_tags(module, api_instance, {})
    tags = resp.data or []
    match = None
    for tag in tags:
        if getattr(tag, "ext_id", None) == ext_id:
            match = tag
            break
    if match is None:
        module.fail_json(
            msg="Log-collection tag with ext_id '{0}' not found on cluster {1}".format(
                ext_id, module.params.get("cluster_ext_id")
            ),
            **result,
        )
    result["response"] = strip_internal_attributes(match.to_dict())


def get_tags(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating log-collection tags info spec", **result
        )

    resp = _list_tags(module, api_instance, kwargs)

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
    api_instance = get_cluster_logs_api_instance(module)
    if module.params.get("ext_id"):
        get_tag_by_ext_id(module, api_instance, result)
    else:
        get_tags(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
