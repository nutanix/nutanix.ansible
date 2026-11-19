#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_host_gpus_info_v2
short_description: Fetch host GPU info in Nutanix Prism Central
version_added: "2.7.0"
description:
  - This module allows you to fetch information about Host GPU in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Host GPU on the given host.
  - If C(ext_id) is not provided, list multiple Host GPUs optionally filtered / paginated
    using C(filter), C(limit), C(page), C(orderby) and C(select).
  - When C(cluster_ext_id) and C(host_ext_id) are both provided without C(ext_id),
    host GPUs are listed for that host; when only C(cluster_ext_id) is provided,
    GPUs are listed for that cluster; otherwise a global list is returned.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View Host GPU) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the host GPU.
      - If provided, fetches single GPU; requires cluster_ext_id and host_ext_id.
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster that owns the host GPU.
    type: str
    required: false
  host_ext_id:
    description:
      - The external ID (UUID) of the host that owns the host GPU.
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
- name: Fetch a specific host GPU
  nutanix.ncp.ntnx_cluster_host_gpus_info_v2:
    cluster_ext_id: "0005b3f7-1234-4321-abcd-0123456789ab"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    ext_id: "d6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821"
  register: result
  ignore_errors: true

- name: List all host GPUs across Prism Central
  nutanix.ncp.ntnx_cluster_host_gpus_info_v2:
  register: result
  ignore_errors: true

- name: List host GPUs by cluster
  nutanix.ncp.ntnx_cluster_host_gpus_info_v2:
    cluster_ext_id: "0005b3f7-1234-4321-abcd-0123456789ab"
  register: result
  ignore_errors: true

- name: List host GPUs by host
  nutanix.ncp.ntnx_cluster_host_gpus_info_v2:
    cluster_ext_id: "0005b3f7-1234-4321-abcd-0123456789ab"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Host GPU info v4 API.
    - It can be a single Host GPU if external ID is provided.
    - List of multiple Host GPUs if external ID is not provided with optional filter, limit, orderby, or select.
  returned: always
  type: dict
  sample:
    {
        "config": {
            "assignable": 1,
            "device_id": 0,
            "device_name": "NVIDIA A100",
            "vendor_name": "NVIDIA"
        },
        "ext_id": "084af8fb-87f8-46e6-a2f4-cabeffc81850",
        "node_uuid": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b"
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
  sample: "Api Exception raised while fetching host GPU info"
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
  description: External ID of the host GPU (when requested via C(ext_id)).
  type: str
  returned: When external ID is provided
  sample: "084af8fb-87f8-46e6-a2f4-cabeffc81850"
total_available_results:
  description: The total number of available host GPUs matching the query.
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
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
        host_ext_id=dict(type="str"),
    )
    return module_args


def get_host_gpu_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")
    if not cluster_ext_id or not host_ext_id:
        module.fail_json(
            msg="cluster_ext_id and host_ext_id are required when ext_id is provided",
            **result,
        )
    try:
        resp = api_instance.get_host_gpu_by_id(
            clusterExtId=cluster_ext_id, hostExtId=host_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching host GPU info",
        )
    result["ext_id"] = ext_id
    result["response"] = (
        strip_internal_attributes(resp.data.to_dict()) if resp.data else {}
    )


def get_host_gpus(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating host GPU info spec", **result)
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")
    try:
        if cluster_ext_id and host_ext_id:
            resp = list_entities(
                api_instance.list_host_gpus_by_host_id,
                kwargs=kwargs,
                clusterExtId=cluster_ext_id,
                hostExtId=host_ext_id,
            )
        elif cluster_ext_id:
            resp = list_entities(
                api_instance.list_host_gpus_by_cluster_id,
                kwargs=kwargs,
                clusterExtId=cluster_ext_id,
            )
        else:
            resp = list_entities(api_instance.list_host_gpus, kwargs=kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching host GPU info",
        )
    total_available_results = (
        resp.metadata.total_available_results
        if hasattr(resp.metadata, "total_available_results")
        else 0
    )
    result["total_available_results"] = total_available_results
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(argument_spec=get_module_spec(), supports_check_mode=False)
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    if module.params.get("ext_id"):
        get_host_gpu_using_ext_id(module, api_instance, result)
    else:
        get_host_gpus(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
