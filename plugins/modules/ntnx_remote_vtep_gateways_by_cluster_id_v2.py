#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_remote_vtep_gateways_by_cluster_id_v2
short_description: Fetch a single remote VTEP gateway discovered under a Prism Element cluster
version_added: 2.7.0
description:
  - This module fetches a single Remote VTEP Gateway that has been discovered on
    a specific Prism Element cluster registered with Prism Central.
  - The Remote VTEP Gateway resource is exposed by the Prism Central v4
    networking API as a B(read-only) discovery surface — it is used by workflows
    such as L2 Subnet Extension (a.k.a. L2 stretch) to pick a peer VTEP gateway
    on a remote availability zone. Create, Update and Delete operations are B(not)
    supported by the underlying SDK for this entity.
  - Both C(cluster_ext_id) and C(ext_id) are required for this module — the
    Prism Central v4 API path is
    C(/api/networking/v4.3/config/clusters/{clusterExtId}/remote-vtep-gateways/{extId}).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get a Remote VTEP Gateway by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_ext_id:
    description:
      - External ID of the Prism Element cluster that owns the remote VTEP gateway.
      - Required.
    type: str
    required: true
  ext_id:
    description:
      - External ID of the remote VTEP gateway to fetch.
      - Required.
    type: str
    required: true
  read_timeout:
    description:
      - Read timeout in milliseconds for API calls.
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
- name: Fetch a single remote VTEP gateway discovered under a Prism Element cluster
  nutanix.ncp.ntnx_remote_vtep_gateways_by_cluster_id_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response for fetching a remote VTEP gateway using its external ID.
    - Contains the full RemoteVtepGateway payload returned by the
      Nutanix PC networking v4 API for the C(GetRemoteVtepGatewayForClusterById) operation.
  returned: always
  type: dict
  sample:
    {
      "cluster_name": "PE-cluster-01",
      "cluster_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "high_availability_group": {
          "algorithm": "ACTIVE_BACKUP",
          "is_ha_enabled": true,
          "peered_gateways": [
              {
                  "ext_id": "9f6cca9c-4a53-4ad5-9f4d-3f5a8a1e7db1",
                  "status": "UP"
              }
          ]
      },
      "is_active": true,
      "is_local": false,
      "links": null,
      "metadata": null,
      "name": "remote-vtep-gw-ansible",
      "tenant_id": null,
      "vpc_name": "vpc_ansible",
      "vpc_reference": "1c6bc5f3-c18c-4702-4c2d-b769fd5f9401",
      "vxlan_port": 4789
    }

ext_id:
  description:
    - External ID of the fetched remote VTEP gateway.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

cluster_ext_id:
  description:
    - External ID of the Prism Element cluster used to scope the fetch.
  returned: always
  type: str
  sample: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"

changed:
  description: This indicates whether the task resulted in any changes. Always false for this read-only module.
  returned: always
  type: bool
  sample: false

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

error:
  description: This field typically holds information about any error that occurred during the task execution.
  type: str
  returned: when an error occurs

msg:
  description: This indicates the message associated with the operation, primarily on error.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching remote VTEP gateway info using cluster ext_id and ext_id"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_remote_entities_api_instance,
)
from ..module_utils.v4.network.helpers import (  # noqa: E402
    get_remote_vtep_gateway_for_cluster,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )

    return module_args


def get_remote_vtep_gateway_by_cluster_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_remote_vtep_gateway_for_cluster(
        module, api_instance, cluster_ext_id, ext_id
    )
    result["cluster_ext_id"] = cluster_ext_id
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "cluster_ext_id": None,
    }
    api_instance = get_remote_entities_api_instance(module)
    get_remote_vtep_gateway_by_cluster_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
