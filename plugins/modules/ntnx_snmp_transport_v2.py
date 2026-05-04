#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_transport_v2
short_description: Manage SNMP transports for a cluster in Nutanix Prism Central
description:
    - This module allows you to add, update, and remove SNMP transport configurations for a specific cluster.
    - SNMP transports define the protocol and port used for SNMP communication.
    - For update operations, provide the current transport details and the new transport details.
    - This module uses PC v4 APIs based SDKs
version_added: 2.6.0
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Add SNMP transport) -
      Operation Name: Add SNMP Transport -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - >-
      B(Remove SNMP transport) -
      Operation Name: Remove SNMP Transport -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
        - Specify state.
        - If C(state) is set to C(present), the module will add an SNMP transport to the cluster.
        - If C(state) is set to C(present) and the transport already exists, idempotency will skip the operation.
        - If C(state) is set to C(absent), the module will remove the SNMP transport from the cluster.
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
      - The SNMP transport protocol.
    type: str
    required: true
    choices:
      - UDP
      - UDP6
      - TCP
      - TCP6
  port:
    description:
      - The SNMP transport port number.
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
- name: Add SNMP transport to a cluster
  nutanix.ncp.ntnx_snmp_transport_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    protocol: UDP
    port: 162
    state: present

- name: Remove SNMP transport from a cluster
  nutanix.ncp.ntnx_snmp_transport_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
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
        "ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
        "is_enabled": true,
        "transports": [
          {
            "port": 162,
            "protocol": "UDP"
          }
        ],
        "traps": [],
        "users": []
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
    sample: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: always
    type: bool
    sample: false
skipped:
    description: This field indicates whether the task was skipped due to idempotency.
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or idempotency skip
    type: str
    sample: "SNMP transport already exists. Nothing to change."
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_snmp_api_instance,
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

# Suppress the InsecureRequestWarning
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
    """Check if a transport with given protocol and port already exists."""
    if not transports:
        return False
    for t in transports:
        t_dict = t if isinstance(t, dict) else t.to_dict()
        if t_dict.get("protocol") == protocol and t_dict.get("port") == port:
            return True
    return False


def _build_transport_spec(protocol, port):
    """Build an SnmpTransport spec from protocol and port."""
    spec = clustermgmt_sdk.SnmpTransport()
    spec.protocol = getattr(clustermgmt_sdk.SnmpProtocol, protocol)
    spec.port = port
    return spec


def create_snmp_transport(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    protocol = module.params.get("protocol")
    port = module.params.get("port")
    result["ext_id"] = cluster_ext_id

    if module.check_mode:
        spec = _build_transport_spec(protocol, port)
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_config = get_snmp_config(module, api_instance, cluster_ext_id)
    if current_config and _transport_exists(
        getattr(current_config, "transports", None), protocol, port
    ):
        result["skipped"] = True
        result["msg"] = "SNMP transport already exists. Nothing to change."
        module.exit_json(**result)

    spec = _build_transport_spec(protocol, port)

    try:
        resp = api_instance.add_snmp_transport(clusterExtId=cluster_ext_id, body=spec)
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
        resp = get_snmp_config(module, api_instance, cluster_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_snmp_transport(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    protocol = module.params.get("protocol")
    port = module.params.get("port")
    result["ext_id"] = cluster_ext_id

    if module.check_mode:
        result["msg"] = (
            "SNMP transport with protocol:{0} and port:{1} "
            "will be removed from cluster:{2}.".format(protocol, port, cluster_ext_id)
        )
        return

    current_config = get_snmp_config(module, api_instance, cluster_ext_id)
    if current_config and not _transport_exists(
        getattr(current_config, "transports", None), protocol, port
    ):
        result["skipped"] = True
        result["msg"] = "SNMP transport does not exist. Nothing to change."
        module.exit_json(**result)

    spec = _build_transport_spec(protocol, port)

    try:
        resp = api_instance.remove_snmp_transport(
            clusterExtId=cluster_ext_id, body=spec
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
        resp = get_snmp_config(module, api_instance, cluster_ext_id)
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
    api_instance = get_snmp_api_instance(module)
    if state == "present":
        create_snmp_transport(module, api_instance, result)
    elif state == "absent":
        delete_snmp_transport(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
