#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_transport_v2
short_description: Manage SNMP transport configuration for a Nutanix cluster
description:
    - This module allows you to add and remove SNMP transport ports and protocol details for a Nutanix cluster.
    - >-
      When C(state=present), it adds an SNMP transport (protocol and port) to the cluster.
      If the same transport already exists, the operation is skipped (idempotent).
    - >-
      When C(state=absent), it removes the specified SNMP transport from the cluster.
      If the transport does not exist, the operation is skipped (idempotent).
    - This module uses PC v4 APIs based SDKs
version_added: "2.6.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Add/Remove SNMP Transport) -
      Operation Name: Manage SNMP Configuration -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
        - Specify state.
        - If C(state) is set to C(present) then the module will add an SNMP transport.
        - If C(state) is set to C(absent) then the module will remove an SNMP transport.
    choices:
        - present
        - absent
    type: str
    default: present
  wait:
    description: Wait for the operation to complete.
    type: bool
    required: false
    default: true
  cluster_ext_id:
    description:
        - The external ID of the cluster.
    type: str
    required: true
  protocol:
    description:
        - SNMP protocol type.
    type: str
    required: true
    choices:
        - UDP
        - UDP6
        - TCP
        - TCP6
  port:
    description:
        - SNMP port number.
    type: int
    required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Add SNMP transport with UDP protocol
  nutanix.ncp.ntnx_snmp_transport_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: <cluster_ext_id>
    protocol: UDP
    port: 162

- name: Add SNMP transport with TCP protocol
  nutanix.ncp.ntnx_snmp_transport_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: <cluster_ext_id>
    protocol: TCP
    port: 161

- name: Remove SNMP transport
  nutanix.ncp.ntnx_snmp_transport_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: <cluster_ext_id>
    protocol: UDP
    port: 162
    state: absent
"""

RETURN = r"""
response:
    description:
        - Response for the SNMP transport operation.
        - Task details if C(wait) is false.
        - SNMP config details if C(wait) is true.
    type: dict
    returned: always
    sample:
        {
            "ext_id": "00064079-9b02-8c5e-185b-ac1f6b6f97e2",
            "is_enabled": true,
            "transports": [
                {
                    "port": 162,
                    "protocol": "UDP"
                }
            ]
        }
task_ext_id:
    description:
        - The external ID of the task.
    type: str
    returned: when applicable
    sample: ZXJnb24=:d0fe946a-83b7-464d-bafb-4826282a75b1
ext_id:
    description:
        - External ID of the cluster.
    type: str
    returned: always
    sample: 00064079-9b02-8c5e-185b-ac1f6b6f97e2
changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true
error:
    description: This field holds information about errors that occurred during the task execution.
    returned: always
    type: bool
    sample: false
failed:
    description: This field holds information about if the task has failed.
    returned: always
    type: bool
    sample: false
skipped:
    description: This field indicates whether the task was skipped due to idempotency.
    returned: always
    type: bool
    sample: false
msg:
    description: A message describing the result.
    returned: when applicable
    type: str
    sample: "SNMP transport already exists. Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_snmp_config  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
from ansible.module_utils.basic import missing_required_lib  # noqa: E402

try:
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        protocol=dict(
            type="str",
            required=True,
            choices=["UDP", "UDP6", "TCP", "TCP6"],
        ),
        port=dict(type="int", required=True),
    )
    return module_args


def _transport_exists(transports, protocol, port):
    """Check if a transport with the given protocol and port already exists."""
    if not transports:
        return False
    for t in transports:
        if t.protocol == protocol and t.port == port:
            return True
    return False


def create_snmp_transport(module, clusters_api, result):
    """Add an SNMP transport to the cluster."""
    cluster_ext_id = module.params.get("cluster_ext_id")
    protocol = module.params.get("protocol")
    port = module.params.get("port")
    result["ext_id"] = cluster_ext_id

    spec = clustermgmt_sdk.SnmpTransport(
        protocol=protocol,
        port=port,
    )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_config = get_snmp_config(module, clusters_api, cluster_ext_id)
    if _transport_exists(current_config.transports, protocol, port):
        result["skipped"] = True
        result["msg"] = "SNMP transport already exists. Nothing to change."
        module.exit_json(**result)

    try:
        resp = clusters_api.add_snmp_transport(
            clusterExtId=cluster_ext_id,
            body=spec,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while adding SNMP transport",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_snmp_config(module, clusters_api, cluster_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_snmp_transport(module, clusters_api, result):
    """Remove an SNMP transport from the cluster."""
    cluster_ext_id = module.params.get("cluster_ext_id")
    protocol = module.params.get("protocol")
    port = module.params.get("port")
    result["ext_id"] = cluster_ext_id

    if module.check_mode:
        result["msg"] = "SNMP transport {0}:{1} on cluster {2} will be deleted.".format(
            protocol, port, cluster_ext_id
        )
        return

    current_config = get_snmp_config(module, clusters_api, cluster_ext_id)
    if not _transport_exists(current_config.transports, protocol, port):
        result["skipped"] = True
        result["msg"] = "SNMP transport does not exist. Nothing to change."
        module.exit_json(**result)

    spec = clustermgmt_sdk.SnmpTransport(
        protocol=protocol,
        port=port,
    )

    try:
        resp = clusters_api.remove_snmp_transport(
            clusterExtId=cluster_ext_id,
            body=spec,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while removing SNMP transport",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_snmp_config(module, clusters_api, cluster_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
        "msg": None,
        "failed": False,
    }

    state = module.params.get("state")
    clusters_api = get_clusters_api_instance(module)

    if state == "present":
        create_snmp_transport(module, clusters_api, result)
    elif state == "absent":
        delete_snmp_transport(module, clusters_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
