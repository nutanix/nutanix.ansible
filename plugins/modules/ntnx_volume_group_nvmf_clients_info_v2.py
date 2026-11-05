#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_nvmf_clients_info_v2
short_description: Fetch NVMe-TCP (NVMf) client info from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about NvmfClient in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific NvmfClient.
  - If C(ext_id) is not provided, list multiple NvmfClient optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get a NVMe-TCP client details) -
    Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin, Prism Viewer,
    Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
  - >-
    B(List all the NVMe-TCP clients) -
    Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin, Prism Viewer,
    Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  ext_id:
    description:
      - The external identifier of the NVMe-TCP (NVMf) client.
      - If provided, fetch the NVMf client with the given external ID.
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
- name: Fetch a specific NVMe-TCP client by external ID
  nutanix.ncp.ntnx_volume_group_nvmf_clients_info_v2:
    ext_id: "aea43b5c-ae4d-4b60-934b-f8f581275dec"
  register: result
  ignore_errors: true

- name: List all NVMe-TCP clients across Volume Groups
  nutanix.ncp.ntnx_volume_group_nvmf_clients_info_v2:
  register: result
  ignore_errors: true

- name: List NVMe-TCP clients filtered by clusterReference
  nutanix.ncp.ntnx_volume_group_nvmf_clients_info_v2:
    filter: "clusterReference eq '00061663-9fa0-28ca-185b-ac1f6b6f97e2'"
  register: result
  ignore_errors: true

- name: List NVMe-TCP clients with pagination and ordering
  nutanix.ncp.ntnx_volume_group_nvmf_clients_info_v2:
    page: 0
    limit: 10
    orderby: "extId asc"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC NvmfClient info v4 API.
    - It can be a single NvmfClient if external ID is provided.
    - List of multiple NvmfClient if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "attached_targets": null,
      "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
      "ext_id": "aea43b5c-ae4d-4b60-934b-f8f581275dec",
      "links": [
        {
          "href": "https://10.44.76.28:9440/api/volumes/v4.2/config/nvmf-clients/aea43b5c-ae4d-4b60-934b-f8f581275dec",
          "rel": "self"
        }
      ],
      "nvmf_initiator_name": "nqn.2014-08.org.nvmexpress:uuid:ansible-nvmf-test",
      "tenant_id": null
    }

ext_id:
  description: External identifier of the NVMe-TCP client (only when a single entity is fetched).
  type: str
  returned: when external ID is provided
  sample: "aea43b5c-ae4d-4b60-934b-f8f581275dec"

total_available_results:
  description: The total number of NVMe-TCP clients available in Prism Central.
  type: int
  returned: when all NVMe-TCP clients are fetched
  sample: 2

changed:
  description: Indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/error message emitted by the module.
  returned: when there is an error
  type: str
  sample: "Api Exception raised while fetching given NVMe-TCP client"

error:
  description: Error details if the task failed.
  type: str
  returned: when an error occurs
  sample: null
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_nvmf_client_api_instance,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_nvmf_client(module, api_instance, result):
    """Fetch a single NVMe-TCP client by external ID."""
    ext_id = module.params.get("ext_id")
    try:
        resp = api_instance.get_nvmf_client_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching given NVMe-TCP client",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_nvmf_clients(module, api_instance, result):
    """List NVMe-TCP clients with optional filtering, pagination and ordering."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating NVMe-TCP clients info spec", **result)

    try:
        resp = api_instance.list_nvmf_clients(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching all available NVMe-TCP clients",
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
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "error": None}
    api_instance = get_nvmf_client_api_instance(module)
    if module.params.get("ext_id"):
        get_nvmf_client(module, api_instance, result)
    else:
        get_nvmf_clients(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
