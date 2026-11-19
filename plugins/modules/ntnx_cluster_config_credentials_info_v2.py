#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_config_credentials_info_v2
short_description: Fetch cluster config credentials
version_added: "2.7.0"
description:
  - This module allows you to fetch information about cluster config credentialss in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific cluster config credentials.
  - If C(ext_id) is not provided, list multiple cluster config credentialss optionally filtered or paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View Cluster Config Credentials) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster.
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
- name: Fetch cluster config credentials using ext_id
  nutanix.ncp.ntnx_cluster_config_credentials_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true

- name: List cluster config credentialss
  nutanix.ncp.ntnx_cluster_config_credentials_info_v2:
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC cluster config credentialss info v4 API.
    - It can be a single cluster config credentials if external ID is provided.
    - List of multiple cluster config credentialss if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
        "name": "sample-cluster config credentials"
    }
changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching cluster config credentials info"
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
  description: External ID of the cluster config credentials (when requested via C(ext_id)).
  type: str
  returned: When external ID is provided
  sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
total_available_results:
  description: The total number of available cluster config credentialss matching the query.
  type: int
  returned: When a list call is made (no C(ext_id) provided).
  sample: 4
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_single(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    try:
        resp = api_instance.get_config_credentials_by_cluster_id(
            clusterExtId=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster config credentials info",
        )
    result["response"] = (
        strip_internal_attributes(resp.data.to_dict()) if resp.data else {}
    )
    result["ext_id"] = module.params.get("cluster_ext_id")


def list_entities_func(module, api_instance, result):
    module.fail_json(msg="Listing not supported for this resource", **result)


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    if (
        module.params.get("ext_id")
        or module.params.get("cluster_ext_id")
        and "true" == "true"
    ):
        # for singleton with cluster_ext_id only, check that
        get_single(module, api_instance, result)
    elif module.params.get("ext_id"):
        get_single(module, api_instance, result)
    else:
        list_entities_func(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
