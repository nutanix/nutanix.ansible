#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_transport_v2
short_description: Manage SNMP transports in Nutanix Prism Central
description:
    - This module allows you to add, update, and remove SNMP transport ports and protocol details on a Nutanix cluster.
    - This module uses PC v4 APIs based SDKs
version_added: 2.6.0
notes:
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
        - Specify state
        - If C(state) is set to C(present) then module will add SNMP transport.
        - >-
          If C(state) is set to C(present) and C(old_port) or C(old_protocol) is given,
          then module will update SNMP transport by removing old and adding new.
        - If C(state) is set to C(absent), then module will remove SNMP transport.
    choices:
        - present
        - absent
    type: str
    default: present
  cluster_ext_id:
    description:
        - The external ID of the cluster.
    type: str
    required: true
  port:
    description:
        - The port number for SNMP transport.
    type: int
    required: true
  protocol:
    description:
        - The protocol for SNMP transport.
    type: str
    required: true
    choices: ['UDP', 'UDP6', 'TCP', 'TCP6']
  old_port:
    description:
        - The old port number to be replaced during update operation.
        - Required when updating an existing SNMP transport.
    type: int
    required: false
  old_protocol:
    description:
        - The old protocol to be replaced during update operation.
        - Required when updating an existing SNMP transport.
    type: str
    required: false
    choices: ['UDP', 'UDP6', 'TCP', 'TCP6']
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
    port: 162
    protocol: "UDP"

- name: Update SNMP transport on a cluster
  nutanix.ncp.ntnx_snmp_transport_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    port: 163
    protocol: "TCP"
    old_port: 162
    old_protocol: "UDP"

- name: Remove SNMP transport from a cluster
  nutanix.ncp.ntnx_snmp_transport_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    port: 162
    protocol: "UDP"
    state: absent
"""

RETURN = r"""
response:
    description:
        - Response for the SNMP transport operation.
        - Task details if operation triggers a task.
    type: dict
    returned: always
    sample:
      {
        "ext_id": "ZXJnb24=:d0fe946a-83b7-464d-bafb-4826282a75b1"
      }
task_ext_id:
    description:
        - Task external ID.
    type: str
    returned: when applicable
    sample: ZXJnb24=:d0fe946a-83b7-464d-bafb-4826282a75b1
ext_id:
    description:
        - Cluster external ID.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode
    type: str
    sample: "SNMP transport already exists on cluster"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
skipped:
    description: This field indicates whether the task was skipped. For example during idempotency checks.
    returned: always
    type: bool
    sample: true
failed:
    description: This field indicates whether the task failed.
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
    get_etag,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_snmp_config  # noqa: E402
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
        port=dict(type="int", required=True),
        protocol=dict(
            type="str", required=True, choices=["UDP", "UDP6", "TCP", "TCP6"]
        ),
        old_port=dict(type="int", required=False),
        old_protocol=dict(
            type="str", required=False, choices=["UDP", "UDP6", "TCP", "TCP6"]
        ),
    )
    return module_args


def _transport_exists(transports, port, protocol):
    """Check if a transport with given port and protocol exists in the list."""
    if not transports:
        return False
    for t in transports:
        if t.port == port and t.protocol == protocol:
            return True
    return False


def create_snmp_transport(module, clusters_api, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    port = module.params.get("port")
    protocol = module.params.get("protocol")
    result["ext_id"] = cluster_ext_id

    snmp_config = get_snmp_config(module, clusters_api, cluster_ext_id)
    if _transport_exists(snmp_config.transports, port, protocol):
        result["skipped"] = True
        result["msg"] = "SNMP transport already exists on cluster."
        module.exit_json(**result)

    transport = clustermgmt_sdk.SnmpTransport()
    transport.port = port
    transport.protocol = protocol

    if module.check_mode:
        result["response"] = strip_internal_attributes(transport.to_dict())
        return

    try:
        resp = clusters_api.add_snmp_transport(
            clusterExtId=cluster_ext_id, body=transport
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while adding SNMP transport",
        )

    task_ext_id = None
    if hasattr(resp, "data") and resp.data and hasattr(resp.data, "ext_id"):
        task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def update_snmp_transport(module, clusters_api, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    port = module.params.get("port")
    protocol = module.params.get("protocol")
    old_port = module.params.get("old_port")
    old_protocol = module.params.get("old_protocol")
    result["ext_id"] = cluster_ext_id

    if old_port == port and old_protocol == protocol:
        result["skipped"] = True
        result["msg"] = "Nothing to change."
        module.exit_json(**result)

    snmp_config = get_snmp_config(module, clusters_api, cluster_ext_id)
    etag = get_etag(data=snmp_config)

    if not _transport_exists(snmp_config.transports, old_port, old_protocol):
        result["msg"] = (
            "SNMP transport with port {0} and protocol {1} not found on cluster.".format(
                old_port, old_protocol
            )
        )
        module.fail_json(**result)

    if _transport_exists(snmp_config.transports, port, protocol):
        result["skipped"] = True
        result["msg"] = (
            "SNMP transport with port {0} and protocol {1} already exists.".format(
                port, protocol
            )
        )
        module.exit_json(**result)

    if module.check_mode:
        new_transport = clustermgmt_sdk.SnmpTransport()
        new_transport.port = port
        new_transport.protocol = protocol
        result["response"] = strip_internal_attributes(new_transport.to_dict())
        return

    old_transport = clustermgmt_sdk.SnmpTransport()
    old_transport.port = old_port
    old_transport.protocol = old_protocol

    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    try:
        clusters_api.remove_snmp_transport(
            clusterExtId=cluster_ext_id, body=old_transport, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while removing old SNMP transport during update",
        )

    new_transport = clustermgmt_sdk.SnmpTransport()
    new_transport.port = port
    new_transport.protocol = protocol

    try:
        resp = clusters_api.add_snmp_transport(
            clusterExtId=cluster_ext_id, body=new_transport
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while adding new SNMP transport during update",
        )

    task_ext_id = None
    if hasattr(resp, "data") and resp.data and hasattr(resp.data, "ext_id"):
        task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def delete_snmp_transport(module, clusters_api, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    port = module.params.get("port")
    protocol = module.params.get("protocol")
    result["ext_id"] = cluster_ext_id

    snmp_config = get_snmp_config(module, clusters_api, cluster_ext_id)

    if not _transport_exists(snmp_config.transports, port, protocol):
        result["skipped"] = True
        result["msg"] = (
            "SNMP transport with port {0} and protocol {1} not found. Nothing to delete.".format(
                port, protocol
            )
        )
        module.exit_json(**result)

    if module.check_mode:
        result["msg"] = (
            "SNMP transport with port {0} and protocol {1} will be removed.".format(
                port, protocol
            )
        )
        return

    transport = clustermgmt_sdk.SnmpTransport()
    transport.port = port
    transport.protocol = protocol

    etag = get_etag(data=snmp_config)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    try:
        resp = clusters_api.remove_snmp_transport(
            clusterExtId=cluster_ext_id, body=transport, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while removing SNMP transport",
        )

    task_ext_id = None
    if hasattr(resp, "data") and resp.data and hasattr(resp.data, "ext_id"):
        task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("cluster_ext_id", "port", "protocol")),
            ("state", "present", ("cluster_ext_id", "port", "protocol")),
        ],
        required_together=[
            ("old_port", "old_protocol"),
        ],
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
        if module.params.get("old_port") or module.params.get("old_protocol"):
            update_snmp_transport(module, clusters_api, result)
        else:
            create_snmp_transport(module, clusters_api, result)
    elif state == "absent":
        delete_snmp_transport(module, clusters_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
