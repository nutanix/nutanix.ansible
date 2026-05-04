#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_transport_v2
short_description: Manage SNMP transport configuration for Nutanix clusters
description:
  - This module allows you to add, update, and remove SNMP transport ports and protocol details for a Nutanix cluster.
  - Add (create) an SNMP transport by specifying the cluster, protocol, and port.
  - Update an SNMP transport by providing existing transport details alongside new transport details.
  - Remove (delete) an SNMP transport by specifying the cluster, protocol, and port to remove.
  - This module uses PC v4 APIs based SDKs
version_added: "2.6.0"
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
      - If C(state) is set to C(present) then the SNMP transport will be added to the cluster.
      - >-
        If C(state) is set to C(present) and C(old_transport) is given, the old transport
        will be removed and the new transport will be added (update operation).
      - If C(state) is set to C(absent) then the SNMP transport will be removed from the cluster.
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
  protocol:
    description:
      - SNMP protocol type for the transport.
    type: str
    required: true
    choices:
      - UDP
      - UDP6
      - TCP
      - TCP6
  port:
    description:
      - SNMP port number for the transport.
    type: int
    required: true
  old_transport:
    description:
      - The existing SNMP transport details to remove during an update operation.
      - Required only for update operations where both old and new transport details differ.
    type: dict
    suboptions:
      protocol:
        description:
          - SNMP protocol type of the existing transport to remove.
        type: str
        required: true
        choices:
          - UDP
          - UDP6
          - TCP
          - TCP6
      port:
        description:
          - SNMP port number of the existing transport to remove.
        type: int
        required: true
  wait:
    description:
      - Whether to wait for the operation to complete.
    type: bool
    default: true
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
    protocol: "UDP"
    port: 162
    state: present

- name: Update SNMP transport (remove old and add new)
  nutanix.ncp.ntnx_snmp_transport_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    protocol: "TCP"
    port: 163
    old_transport:
      protocol: "UDP"
      port: 162
    state: present

- name: Remove SNMP transport from a cluster
  nutanix.ncp.ntnx_snmp_transport_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    protocol: "UDP"
    port: 162
    state: absent
"""

RETURN = r"""
response:
    description:
        - Response for the SNMP transport operation.
        - Task details of the operation.
    type: dict
    returned: always
    sample:
        {
            "ext_id": "ZXJnb24=:100a5778-9824-49c7-9444-222aa97f5874"
        }
ext_id:
    description:
        - The external ID of the cluster.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
task_ext_id:
    description:
        - The task external ID.
    type: str
    returned: always
    sample: "ZXJnb24=:100a5778-9824-49c7-9444-222aa97f5874"
changed:
    description:
        - Indicates if any changes were made during the operation.
    type: bool
    returned: always
    sample: true
skipped:
    description:
        - Indicates if the operation was skipped due to idempotency.
    type: bool
    returned: when the operation was skipped
    sample: true
msg:
    description:
        - A message describing the result of the operation.
    type: str
    returned: always
error:
    description:
        - The error message if an error occurs.
    type: str
    returned: when an error occurs
failed:
    description:
        - Whether the operation failed.
    type: bool
    returned: when an error occurs
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

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
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    old_transport_spec = dict(
        protocol=dict(
            type="str",
            required=True,
            choices=["UDP", "UDP6", "TCP", "TCP6"],
        ),
        port=dict(type="int", required=True),
    )

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        protocol=dict(
            type="str",
            required=True,
            choices=["UDP", "UDP6", "TCP", "TCP6"],
        ),
        port=dict(type="int", required=True),
        old_transport=dict(
            type="dict",
            options=old_transport_spec,
        ),
    )
    return module_args


def _build_snmp_transport_spec(protocol, port):
    """Build an SnmpTransport SDK object from protocol and port values."""
    snmp_protocol = getattr(clusters_sdk.SnmpProtocol, protocol)
    return clusters_sdk.SnmpTransport(protocol=snmp_protocol, port=port)


def _transport_exists(transports, protocol, port):
    """Check if a given transport already exists in the list of transports."""
    if not transports:
        return False
    for t in transports:
        if t.protocol == protocol and t.port == port:
            return True
    return False


def create_snmp_transport(module, api_instance, result):
    """Add an SNMP transport to the cluster."""
    cluster_ext_id = module.params["cluster_ext_id"]
    protocol = module.params["protocol"]
    port = module.params["port"]

    result["ext_id"] = cluster_ext_id

    snmp_config = get_snmp_config(module, api_instance, cluster_ext_id)
    existing_transports = snmp_config.transports if snmp_config else []

    if _transport_exists(existing_transports, protocol, port):
        result["skipped"] = True
        module.exit_json(
            msg="SNMP transport with protocol '{0}' and port '{1}' already exists.".format(
                protocol, port
            ),
            **result,
        )

    spec = _build_snmp_transport_spec(protocol, port)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.add_snmp_transport(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while adding SNMP transport",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def update_snmp_transport(module, api_instance, result):
    """Update an SNMP transport by removing the old one and adding the new one."""
    cluster_ext_id = module.params["cluster_ext_id"]
    protocol = module.params["protocol"]
    port = module.params["port"]
    old_transport = module.params["old_transport"]
    old_protocol = old_transport["protocol"]
    old_port = old_transport["port"]

    result["ext_id"] = cluster_ext_id

    snmp_config = get_snmp_config(module, api_instance, cluster_ext_id)
    existing_transports = snmp_config.transports if snmp_config else []

    if (
        old_protocol == protocol
        and old_port == port
        and _transport_exists(existing_transports, protocol, port)
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if _transport_exists(existing_transports, protocol, port) and not _transport_exists(
        existing_transports, old_protocol, old_port
    ):
        result["skipped"] = True
        module.exit_json(
            msg="New transport already exists and old transport not found. Nothing to change.",
            **result,
        )

    new_spec = _build_snmp_transport_spec(protocol, port)

    if module.check_mode:
        result["response"] = strip_internal_attributes(new_spec.to_dict())
        return

    if _transport_exists(existing_transports, old_protocol, old_port):
        old_spec = _build_snmp_transport_spec(old_protocol, old_port)
        try:
            resp = api_instance.remove_snmp_transport(
                clusterExtId=cluster_ext_id, body=old_spec
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while removing old SNMP transport during update",
            )
        task_ext_id = resp.data.ext_id
        if task_ext_id and module.params.get("wait"):
            wait_for_completion(module, task_ext_id)

    resp = None
    try:
        resp = api_instance.add_snmp_transport(
            clusterExtId=cluster_ext_id, body=new_spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while adding new SNMP transport during update",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_snmp_transport(module, api_instance, result):
    """Remove an SNMP transport from the cluster."""
    cluster_ext_id = module.params["cluster_ext_id"]
    protocol = module.params["protocol"]
    port = module.params["port"]

    result["ext_id"] = cluster_ext_id

    snmp_config = get_snmp_config(module, api_instance, cluster_ext_id)
    existing_transports = snmp_config.transports if snmp_config else []

    if not _transport_exists(existing_transports, protocol, port):
        result["skipped"] = True
        module.exit_json(
            msg="SNMP transport with protocol '{0}' and port '{1}' not found.".format(
                protocol, port
            ),
            **result,
        )

    spec = _build_snmp_transport_spec(protocol, port)

    if module.check_mode:
        result["msg"] = (
            "SNMP transport with protocol '{0}' and port '{1}' will be removed.".format(
                protocol, port
            )
        )
        return

    resp = None
    try:
        resp = api_instance.remove_snmp_transport(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while removing SNMP transport",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
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
    }

    api_instance = get_clusters_api_instance(module)
    state = module.params["state"]

    if state == "present":
        if module.params.get("old_transport"):
            update_snmp_transport(module, api_instance, result)
        else:
            create_snmp_transport(module, api_instance, result)
    else:
        delete_snmp_transport(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
