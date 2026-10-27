#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_rackable_units_info_v2
short_description: Fetch rackable unit info from a Nutanix cluster via Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about rackable units of a Nutanix cluster from Prism Central.
  - If C(ext_id) is provided, fetch details of the specific rackable unit of the given cluster.
  - If C(ext_id) is not provided, list all rackable units of the given cluster optionally filtered / paginated.
  - A rackable unit represents a physical block/chassis containing one or more nodes that
    make up a Nutanix cluster. This module is a read-only info source.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(View Cluster Rackable Unit) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin,
    Prism Viewer, Project Manager, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the Prism Element cluster whose rackable units
        should be fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of a specific rackable unit inside the cluster.
      - If provided, only that rackable unit's details are returned.
      - If not provided, the module returns the list of rackable units for the cluster.
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
- name: Get a specific rackable unit using its external ID
  nutanix.ncp.ntnx_rackable_units_info_v2:
    cluster_ext_id: "0005f5b1-2b2a-1cde-0000-000000012345"
    ext_id: "9d2b1c04-4f5a-4e3a-9d3b-bf7b6f4a5c11"
  register: result
  ignore_errors: true

- name: List all rackable units of a cluster
  nutanix.ncp.ntnx_rackable_units_info_v2:
    cluster_ext_id: "0005f5b1-2b2a-1cde-0000-000000012345"
  register: result
  ignore_errors: true

- name: List rackable units of a cluster with filter
  nutanix.ncp.ntnx_rackable_units_info_v2:
    cluster_ext_id: "0005f5b1-2b2a-1cde-0000-000000012345"
    filter: "serial eq '18FM6G460083'"
  register: result
  ignore_errors: true

- name: List rackable units of a cluster with limit
  nutanix.ncp.ntnx_rackable_units_info_v2:
    cluster_ext_id: "0005f5b1-2b2a-1cde-0000-000000012345"
    limit: 1
  register: result
  ignore_errors: true

- name: List all rackable units of a cluster with fetch_all
  nutanix.ncp.ntnx_rackable_units_info_v2:
    cluster_ext_id: "0005f5b1-2b2a-1cde-0000-000000012345"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RackableUnit info v4 API.
    - It can be a single rackable unit if C(ext_id) is provided.
    - List of multiple rackable units of the cluster if C(ext_id) is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "5879195f-5101-4d41-8e6d-af4a6aa52472",
      "id": 10,
      "model": "USELAYOUT",
      "model_name": "NX-1065-G5",
      "serial": "18FM6G460083",
      "rack": null,
      "links": null,
      "tenant_id": null,
      "nodes": [
        {
          "position": 4,
          "svm_id": 2,
          "uuid": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b"
        }
      ]
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
  sample: "Api Exception raised while fetching rackable units info"

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
  description: External ID of the rackable unit (when requested via C(ext_id)).
  type: str
  returned: When external ID is provided
  sample: "5879195f-5101-4d41-8e6d-af4a6aa52472"

total_available_results:
  description: The total number of available rackable units for the cluster.
  type: int
  returned: When listing rackable units for a cluster
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_rackable_unit  # noqa: E402
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
        ext_id=dict(type="str"),
    )

    return module_args


def get_rackable_unit_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_rackable_unit(module, api_instance, ext_id, cluster_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_rackable_units(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating rackable units info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_rackable_units_by_cluster_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching rackable units info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    if module.params.get("ext_id"):
        get_rackable_unit_using_ext_id(module, api_instance, result)
    else:
        get_rackable_units(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
