#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_remote_subnet_for_cluster_v2
short_description: Fetch a specific remote subnet for a cluster from Nutanix Prism Central
version_added: 2.5.0
description:
  - This module fetches configuration details of a specific remote subnet visible
    from the given Prism Central cluster in Nutanix Prism Central.
  - RemoteSubnetForCluster is a read-only construct exposed by the Networking v4.3
    RemoteEntitiesApi. It cannot be created, updated or deleted via this API;
    modifications must happen on the Prism Central that owns the subnet.
  - Setting C(state=absent) is intentionally rejected because the underlying API
    does not support delete/update/create operations on remote subnets.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation. The required roles depend on the operation being performed.
    - >-
      B(Get remote subnet by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin,
      Prism Viewer, Project Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) the module fetches the specified remote subnet.
      - C(state=absent) is not supported for remote subnets and will fail because
        RemoteSubnetForCluster is a read-only entity exposed via the RemoteEntitiesApi.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  cluster_ext_id:
    description:
      - Reference to the Prism Central cluster from which the remote subnet is queried.
      - Required for all operations.
    type: str
    required: true
  ext_id:
    description:
      - Reference to the specified remote subnet.
      - Required for fetching the remote subnet.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch a remote subnet visible from a Prism Central cluster
  nutanix.ncp.ntnx_remote_subnet_for_cluster_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for fetching a specific remote subnet for the given cluster.
    - Contains the remote subnet detail returned by the Nutanix PC networking v4 API.
  returned: always
  type: dict
  sample:
    {
      "bridge_name": null,
      "cluster_name": null,
      "cluster_name_list": null,
      "cluster_reference": null,
      "cluster_reference_list": null,
      "description": null,
      "dhcp_options": null,
      "dynamic_ip_addresses": null,
      "external_dhcp_servers": null,
      "ext_id": "b57a5527-72ca-45aa-be07-829ba18f9f8b",
      "hypervisor_type": null,
      "ip_config": [
          {
              "ipv4": {
                  "default_gateway_ip": {
                      "prefix_length": 32,
                      "value": "192.168.170.1"
                  },
                  "dhcp_server_address": null,
                  "ip_subnet": {
                      "ip": {
                          "prefix_length": 32,
                          "value": "192.168.170.0"
                      },
                      "prefix_length": 24
                  },
                  "pool_list": null
              },
              "ipv6": null
          }
      ],
      "ip_prefix": null,
      "ip_usage": null,
      "is_advanced_networking": null,
      "is_external": null,
      "is_nat_enabled": null,
      "layer2_stretch_reference": null,
      "links": null,
      "metadata": null,
      "migration_state": null,
      "name": "GNHQMOOkSSrI_ansible-clear-rp-counter_subnet",
      "network_function_chain_reference": null,
      "network_id": null,
      "reserved_ip_addresses": null,
      "subnet_type": null,
      "tenant_id": null,
      "virtual_switch": null,
      "virtual_switch_reference": null,
      "vpc": null,
      "vpc_name": "GNHQMOOkSSrI_ansible-clear-rp-counter_vpc",
      "vpc_reference": "305ed978-23d3-4d4d-8f5d-c49bf8ab5ecd"
    }

ext_id:
  description:
    - The external ID of the remote subnet.
  returned: always
  type: str
  sample: "b57a5527-72ca-45aa-be07-829ba18f9f8b"

task_ext_id:
  description:
    - The external ID of the task.
    - Always C(null) for remote subnet reads because no task is created.
  returned: always
  type: str
  sample: null

changed:
  description: This indicates whether the module made any changes.
  returned: always
  type: bool
  sample: false

skipped:
  description:
    - Indicates whether the operation was skipped.
    - Always false for successful get, and only set to true in C(check_mode).
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description:
    - Status/error message.
    - Populated when C(state=absent) is passed (remote subnets are read-only)
      or in C(check_mode).
  returned: When there is an error, unsupported state, or check mode
  type: str
  sample: "RemoteSubnetForCluster is a read-only entity; state=absent is not supported."
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_remote_entities_api_instance,
)
from ..module_utils.v4.network.helpers import (  # noqa: E402
    get_remote_subnet_for_cluster,
)
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
    validate_required_params,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def read_remote_subnet_for_cluster(module, result, api_instance):
    """Fetch a specific remote subnet from a given Prism Central cluster.

    RemoteSubnetForCluster is a read-only entity in the Networking v4.3 API.
    This method calls the SDK's GET-by-id endpoint and populates ``result``
    with the fetched data.
    """
    validate_required_params(module, ["cluster_ext_id", "ext_id"])

    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Remote subnet with ext_id:{0} on cluster ext_id:{1} would be fetched.".format(
                ext_id, cluster_ext_id
            )
        )
        result["skipped"] = True
        return

    resp = get_remote_subnet_for_cluster(module, api_instance, cluster_ext_id, ext_id)
    if resp is None:
        module.fail_json(
            msg=(
                "Remote subnet ext_id='{0}' was not found on cluster ext_id='{1}'.".format(
                    ext_id, cluster_ext_id
                )
            ),
            **result,
        )
    result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = False


def reject_delete_remote_subnet_for_cluster(module, result):
    """Explicitly reject state=absent for the read-only RemoteSubnetForCluster.

    The Networking v4.3 RemoteEntitiesApi does not expose a delete/update/create
    method for remote subnets. Fail fast with a clear, actionable message so
    playbook authors are not left wondering why nothing happened.
    """
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = ext_id
    result["failed"] = True
    module.fail_json(
        msg=(
            "RemoteSubnetForCluster is a read-only entity in the Nutanix Networking "
            "v4 API; state=absent is not supported. Remote subnet ext_id='{0}' on "
            "cluster ext_id='{1}' can only be modified on the Prism Central that "
            "owns it."
        ).format(ext_id, cluster_ext_id),
        **result,
    )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("cluster_ext_id", "ext_id")),
            ("state", "absent", ("cluster_ext_id", "ext_id")),
        ],
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }
    api_instance = get_remote_entities_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        read_remote_subnet_for_cluster(module, result, api_instance)
    else:
        reject_delete_remote_subnet_for_cluster(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
