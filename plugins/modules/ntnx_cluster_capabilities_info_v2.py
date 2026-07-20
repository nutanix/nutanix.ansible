#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_capabilities_info_v2
short_description: Fetch cluster capabilities info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ClusterCapability in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ClusterCapability.
  - If C(ext_id) is not provided, list multiple ClusterCapability optionally filtered / paginated.
  - The Networking Cluster Capabilities API exposes the per-cluster networking
    capabilities supported by the Prism Element clusters registered against
    the Prism Central instance.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM operation to be granted
      to the calling user on the C(cluster_networking_capabilities) legacy
      object kind - C(View_Cluster_Networking_Capabilities).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external identifier of the cluster capability entity, which is
        the UUID of the Prism Element cluster whose networking capabilities
        should be returned.
      - When provided, the module fetches the single ClusterCapability entity
        that matches C(clusterId == ext_id) via an OData filter push-down
        against the C(list_cluster_capabilities) endpoint (the underlying
        API does not expose a get-by-ID endpoint for this entity).
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
- name: List all cluster capabilities registered against Prism Central
  nutanix.ncp.ntnx_cluster_capabilities_info_v2:
  register: all_capabilities

- name: List cluster capabilities filtered by clusterId
  nutanix.ncp.ntnx_cluster_capabilities_info_v2:
    filter: "clusterId eq '00061de6-4a87-6b06-185b-ac1f6b6f97e2'"
  register: filtered_capabilities

- name: List cluster capabilities with a page size limit
  nutanix.ncp.ntnx_cluster_capabilities_info_v2:
    limit: 1
  register: limited_capabilities

- name: List cluster capabilities sorted by clusterId descending
  nutanix.ncp.ntnx_cluster_capabilities_info_v2:
    orderby: "clusterId desc"
  register: sorted_capabilities

- name: Fetch a single cluster capability entity by external ID
  nutanix.ncp.ntnx_cluster_capabilities_info_v2:
    ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
  register: single_capability
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ClusterCapability info v4 API.
    - It can be a single ClusterCapability if external ID is provided.
    - List of multiple ClusterCapability if external ID is not provided with
      optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "capabilities": [
        {
          "capability_name": "NIC_TEAM_TBL_SYNC_ENABLE",
          "is_supported": true
        },
        {
          "capability_name": "SUPPORTS_NETWORK_ASYNC_RPCS",
          "is_supported": true
        },
        {
          "capability_name": "SUPPORTS_PC_DVS_V1",
          "is_supported": true
        },
        {
          "capability_name": "SUPPORTS_SPAN_V2",
          "is_supported": true
        }
      ],
      "cluster_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "ext_id": null,
      "links": null,
      "metadata": null,
      "tenant_id": null
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
  sample: "Api Exception raised while fetching cluster capabilities info"

error:
  description:
    - This field typically holds information about if the task have errors
      that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task has failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - External ID of the cluster capability entity - the Prism Element
      cluster UUID whose networking capabilities were returned.
  type: str
  returned: when external ID is provided
  sample: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"

total_available_results:
  description:
    - The total number of available cluster capability entities in PC.
    - The Networking Cluster Capabilities API historically returned
      C(null) for this field (see NET-20210 / ENG-681255); it is only
      populated on Prism Central builds that carry the fix.
  type: int
  returned: when all cluster capabilities are fetched
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_cluster_capabilities_api_instance,
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
        ext_id=dict(type="str"),
    )

    return module_args


def _list_cluster_capabilities(module, api_instance, **kwargs):
    """
    Wrapper around C(list_cluster_capabilities) which handles SDK exceptions in
    the standard Ansible way.
    """
    try:
        return api_instance.list_cluster_capabilities(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster capabilities info",
        )


def get_cluster_capability_using_ext_id(module, api_instance, result):
    """
    The ClusterCapabilities SDK does not expose a get-by-ID endpoint; the only
    supported entrypoint is C(list_cluster_capabilities), and the API only
    accepts an OData filter keyed by C(clusterId). The C(ext_id) surfaced by
    this module maps to the Prism Element cluster UUID that owns the
    capability entry, so we push down a C(clusterId eq '<ext_id>') filter
    and unwrap the single result.
    """
    ext_id = module.params.get("ext_id")
    kwargs = {"_filter": "clusterId eq '{0}'".format(ext_id)}
    resp = _list_cluster_capabilities(module, api_instance, **kwargs)

    resp = strip_internal_attributes(resp.to_dict())
    data = resp.get("data") or []
    if not data:
        module.fail_json(
            msg="Cluster capability with ext_id '{0}' was not found".format(ext_id),
            response=resp,
            failed=True,
        )
    result["ext_id"] = ext_id
    result["response"] = data[0]


def get_cluster_capabilities(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating cluster capabilities info spec", **result
        )

    # `select` is exposed by the shared info doc fragment but the
    # ClusterCapabilities SDK does not accept it; drop it before the SDK call.
    kwargs.pop("_select", None)

    resp = _list_cluster_capabilities(module, api_instance, **kwargs)

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    data = resp.get("data")
    if not data:
        data = []
    result["response"] = data


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
    api_instance = get_cluster_capabilities_api_instance(module)
    if module.params.get("ext_id"):
        get_cluster_capability_using_ext_id(module, api_instance, result)
    else:
        get_cluster_capabilities(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
