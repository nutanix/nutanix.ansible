#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_config_by_cluster_id_v2
short_description: Manage SNMP configuration of a Nutanix cluster in Prism Central
version_added: 2.7.0
description:
  - This module allows you to manage the SNMP configuration of a Nutanix cluster via Prism Central.
  - Depending on C(resource_type), this module can update SNMP status, add or remove
    SNMP transport ports, create, update, or delete SNMP users, and create, update,
    or delete SNMP traps.
  - The SNMP configuration is scoped to a cluster and identified by C(cluster_ext_id).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Update SNMP status, add/remove SNMP transports, manage SNMP users and traps) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) it will create/update the selected SNMP resource on the cluster.
      - If C(state) is set to C(absent) it will delete or remove the selected SNMP resource from the cluster.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster whose SNMP configuration is being managed.
    type: str
    required: true
  resource_type:
    description:
      - Selects which SNMP sub-resource this task operates on.
      - C(status) toggles SNMP on the cluster (uses C(is_enabled)).
      - C(transport) adds or removes SNMP transports (uses C(transports)).
      - C(user) creates, updates, or deletes a SNMP user (uses C(username), C(auth_type), C(auth_key), C(priv_type), C(priv_key)).
      - C(trap) creates, updates, or deletes a SNMP trap (uses C(address), C(username), C(protocol), C(port), C(should_inform), C(engine_id), C(version), C(reciever_name), C(community_string)).
    type: str
    required: true
    choices:
      - status
      - transport
      - user
      - trap
  ext_id:
    description:
      - The external ID (UUID) of a specific SNMP user or SNMP trap.
      - Required for update and delete operations on C(user) and C(trap) resource types.
    type: str
    required: false
  is_enabled:
    description:
      - Desired SNMP status.
      - Required when C(resource_type=status).
    type: bool
    required: false
  transports:
    description:
      - List of SNMP transports to add or remove.
      - Required when C(resource_type=transport).
    type: list
    elements: dict
    required: false
    suboptions:
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
          - SNMP transport port number.
        type: int
        required: false
  username:
    description:
      - SNMP user name for C(resource_type=user).
      - For SNMP trap C(V3), the SNMP username on the trap.
      - Required when creating an SNMP user (C(resource_type=user), C(state=present), no C(ext_id)).
    type: str
    required: false
  auth_type:
    description:
      - SNMP user authentication type.
      - Used when C(resource_type=user).
    type: str
    required: false
    choices:
      - MD5
      - SHA
  auth_key:
    description:
      - SNMP user authentication key.
      - Used when C(resource_type=user).
    type: str
    required: false
  priv_type:
    description:
      - SNMP user encryption (privacy) type.
      - Used when C(resource_type=user).
    type: str
    required: false
    choices:
      - DES
      - AES
  priv_key:
    description:
      - SNMP user privacy (encryption) key.
      - Used when C(resource_type=user).
    type: str
    required: false
  address:
    description:
      - IP address of the SNMP trap receiver.
      - Required when creating an SNMP trap (C(resource_type=trap), C(state=present), no C(ext_id)).
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the SNMP trap receiver.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The IPv4 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the network.
            type: int
            required: false
      ipv6:
        description:
          - IPv6 address of the SNMP trap receiver.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the network.
            type: int
            required: false
  protocol:
    description:
      - SNMP transport protocol used by the SNMP trap receiver.
      - Used when C(resource_type=trap).
    type: str
    required: false
    choices:
      - UDP
      - UDP6
      - TCP
      - TCP6
  port:
    description:
      - SNMP port used by the SNMP trap receiver.
      - Used when C(resource_type=trap).
    type: int
    required: false
  should_inform:
    description:
      - Whether the SNMP trap should send C(INFORM) instead of a plain trap.
      - Used when C(resource_type=trap).
    type: bool
    required: false
  engine_id:
    description:
      - Engine ID of the SNMP trap receiver.
      - Used when C(resource_type=trap).
    type: str
    required: false
  version:
    description:
      - SNMP trap protocol version.
      - Used when C(resource_type=trap).
    type: str
    required: false
    choices:
      - V2
      - V3
  reciever_name:
    description:
      - Name of the SNMP trap receiver.
      - Used when C(resource_type=trap).
    type: str
    required: false
  community_string:
    description:
      - SNMP community string used with SNMP C(V2) traps.
      - Used when C(resource_type=trap).
    type: str
    required: false
    no_log: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Enable SNMP on a cluster
  nutanix.ncp.ntnx_snmp_config_by_cluster_id_v2:
    state: present
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: status
    is_enabled: true
  register: result
  ignore_errors: true

- name: Add SNMP transports on the cluster
  nutanix.ncp.ntnx_snmp_config_by_cluster_id_v2:
    state: present
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: transport
    transports:
      - protocol: UDP
        port: 161
  register: result
  ignore_errors: true

- name: Remove SNMP transports from the cluster
  nutanix.ncp.ntnx_snmp_config_by_cluster_id_v2:
    state: absent
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: transport
    transports:
      - protocol: UDP
        port: 161
  register: result
  ignore_errors: true

- name: Create an SNMP V3 user
  nutanix.ncp.ntnx_snmp_config_by_cluster_id_v2:
    state: present
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: user
    username: "ansible_snmp_user"
    auth_type: SHA
    auth_key: "ansible-auth-key-123"
    priv_type: AES
    priv_key: "ansible-priv-key-123"
  register: result
  ignore_errors: true

- name: Update an existing SNMP user
  nutanix.ncp.ntnx_snmp_config_by_cluster_id_v2:
    state: present
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: user
    ext_id: "aaaaaaaa-1111-2222-3333-444444444444"
    username: "ansible_snmp_user"
    auth_type: MD5
    auth_key: "updated-auth-key-456"
    priv_type: DES
    priv_key: "updated-priv-key-456"
  register: result
  ignore_errors: true

- name: Delete an SNMP user
  nutanix.ncp.ntnx_snmp_config_by_cluster_id_v2:
    state: absent
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: user
    ext_id: "aaaaaaaa-1111-2222-3333-444444444444"
  register: result
  ignore_errors: true

- name: Create an SNMP trap
  nutanix.ncp.ntnx_snmp_config_by_cluster_id_v2:
    state: present
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: trap
    address:
      ipv4:
        value: "10.44.76.100"
    protocol: UDP
    port: 162
    should_inform: false
    version: V3
    username: "ansible_snmp_user"
    reciever_name: "ansible_trap_receiver"
    engine_id: "800000090300abcdef012345"
  register: result
  ignore_errors: true

- name: Update an SNMP trap
  nutanix.ncp.ntnx_snmp_config_by_cluster_id_v2:
    state: present
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: trap
    ext_id: "bbbbbbbb-1111-2222-3333-444444444444"
    address:
      ipv4:
        value: "10.44.76.101"
    protocol: UDP
    port: 162
    should_inform: true
    version: V3
    username: "ansible_snmp_user"
    reciever_name: "ansible_trap_receiver_updated"
    engine_id: "800000090300abcdef012345"
  register: result
  ignore_errors: true

- name: Delete an SNMP trap
  nutanix.ncp.ntnx_snmp_config_by_cluster_id_v2:
    state: absent
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: trap
    ext_id: "bbbbbbbb-1111-2222-3333-444444444444"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the SNMP configuration operation.
    - If the operation is create or update and C(wait) is true, it will return the
      created/updated SNMP user/trap or a task snapshot for status/transport actions.
    - If C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "aaaaaaaa-1111-2222-3333-444444444444",
      "username": "ansible_snmp_user",
      "auth_type": "SHA",
      "priv_type": "AES",
      "auth_key": null,
      "priv_key": null,
      "links": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task created for the SNMP operation.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the created or affected SNMP user / SNMP trap.
    - For C(status) and C(transport) operations, this may remain the same as the
      cluster ext_id.
  returned: always
  type: str
  sample: "aaaaaaaa-1111-2222-3333-444444444444"

cluster_ext_id:
  description:
    - The external ID of the cluster on which the SNMP configuration was managed.
  returned: always
  type: str
  sample: "0006361b-6855-3644-7458-2268f8ffb2bd"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (idempotency)
  returned: When the operation was skipped
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating SNMP user"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
    get_etag,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_snmp_config,
    get_snmp_trap,
    get_snmp_user,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )

    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            obj=cluster_management_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            obj=cluster_management_sdk.IPv6Address,
        ),
    )

    transport_spec = dict(
        protocol=dict(
            type="str",
            required=True,
            choices=["UDP", "UDP6", "TCP", "TCP6"],
            obj=cluster_management_sdk.SnmpProtocol,
        ),
        port=dict(type="int", required=False),
    )

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        resource_type=dict(
            type="str", required=True, choices=["status", "transport", "user", "trap"]
        ),
        ext_id=dict(type="str", required=False),
        is_enabled=dict(type="bool", required=False),
        transports=dict(
            type="list",
            elements="dict",
            options=transport_spec,
            required=False,
            obj=cluster_management_sdk.SnmpTransport,
        ),
        username=dict(type="str", required=False),
        auth_type=dict(
            type="str",
            required=False,
            choices=["MD5", "SHA"],
            obj=cluster_management_sdk.SnmpAuthType,
        ),
        auth_key=dict(type="str", required=False, no_log=True),
        priv_type=dict(
            type="str",
            required=False,
            choices=["DES", "AES"],
            obj=cluster_management_sdk.SnmpPrivType,
        ),
        priv_key=dict(type="str", required=False, no_log=True),
        address=dict(
            type="dict",
            options=ip_address_spec,
            obj=cluster_management_sdk.IPAddress,
            required=False,
        ),
        protocol=dict(
            type="str",
            required=False,
            choices=["UDP", "UDP6", "TCP", "TCP6"],
            obj=cluster_management_sdk.SnmpProtocol,
        ),
        port=dict(type="int", required=False),
        should_inform=dict(type="bool", required=False),
        engine_id=dict(type="str", required=False),
        version=dict(
            type="str",
            required=False,
            choices=["V2", "V3"],
            obj=cluster_management_sdk.SnmpTrapVersion,
        ),
        reciever_name=dict(type="str", required=False),
        community_string=dict(type="str", required=False, no_log=True),
    )
    return module_args


# ---------------------------------------------------------------------------
# SNMP status
# ---------------------------------------------------------------------------


def update_snmp_status(module, result, clusters):
    validate_required_params(module, ["is_enabled"])
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.SnmpStatusParam()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating SNMP status update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = clusters.update_snmp_status(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating SNMP status of a cluster",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


# ---------------------------------------------------------------------------
# SNMP transports
# ---------------------------------------------------------------------------


def _build_transports_spec(module, result):
    validate_required_params(module, ["transports"])
    transports_input = module.params.get("transports") or []
    transports = []
    for item in transports_input:
        transport = cluster_management_sdk.SnmpTransport()
        if item.get("protocol") is not None:
            transport.protocol = item.get("protocol")
        if item.get("port") is not None:
            transport.port = item.get("port")
        transports.append(transport)
    if not transports:
        result["error"] = "No SNMP transports provided"
        module.fail_json(msg="Failed generating SNMP transports spec", **result)
    return transports


def add_snmp_transport(module, result, clusters):
    """Add SNMP transports one by one — the SDK accepts a single ``SnmpTransport``."""
    cluster_ext_id = module.params.get("cluster_ext_id")
    transports_spec = _build_transports_spec(module, result)

    if module.check_mode:
        result["response"] = [
            strip_internal_attributes(t.to_dict()) for t in transports_spec
        ]
        return

    task_ext_ids = []
    task_responses = []
    for transport in transports_spec:
        try:
            resp = clusters.add_snmp_transport(
                clusterExtId=cluster_ext_id, body=transport
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while adding SNMP transports",
            )
        task_ext_id = resp.data.ext_id
        task_ext_ids.append(task_ext_id)
        if task_ext_id and module.params.get("wait"):
            task = wait_for_completion(module, task_ext_id)
            task_responses.append(strip_internal_attributes(task.to_dict()))
        else:
            task_responses.append(strip_internal_attributes(resp.data.to_dict()))

    # Preserve historical single-string task_ext_id when only one transport is
    # supplied; fall back to a list otherwise.
    result["task_ext_id"] = task_ext_ids[0] if len(task_ext_ids) == 1 else task_ext_ids
    result["response"] = (
        task_responses[0] if len(task_responses) == 1 else task_responses
    )
    result["changed"] = True


def remove_snmp_transport(module, result, clusters):
    """Remove SNMP transports one by one — the SDK accepts a single ``SnmpTransport``."""
    cluster_ext_id = module.params.get("cluster_ext_id")
    transports_spec = _build_transports_spec(module, result)

    if module.check_mode:
        result["response"] = [
            strip_internal_attributes(t.to_dict()) for t in transports_spec
        ]
        result["msg"] = (
            "SNMP transports will be removed from cluster with ext_id: {0}".format(
                cluster_ext_id
            )
        )
        return

    task_ext_ids = []
    task_responses = []
    for transport in transports_spec:
        try:
            resp = clusters.remove_snmp_transport(
                clusterExtId=cluster_ext_id, body=transport
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while removing SNMP transports",
            )
        task_ext_id = resp.data.ext_id
        task_ext_ids.append(task_ext_id)
        if task_ext_id and module.params.get("wait"):
            task = wait_for_completion(module, task_ext_id)
            task_responses.append(strip_internal_attributes(task.to_dict()))
        else:
            task_responses.append(strip_internal_attributes(resp.data.to_dict()))

    result["task_ext_id"] = task_ext_ids[0] if len(task_ext_ids) == 1 else task_ext_ids
    result["response"] = (
        task_responses[0] if len(task_responses) == 1 else task_responses
    )
    result["changed"] = True


# ---------------------------------------------------------------------------
# SNMP users
# ---------------------------------------------------------------------------


def _find_user_ext_id_by_username(module, clusters, cluster_ext_id, username):
    """Look up an SNMP user's ext_id by username in the cluster's SNMP config."""
    if not username:
        return None
    config = get_snmp_config(module, clusters, cluster_ext_id)
    for user in getattr(config, "users", None) or []:
        if getattr(user, "username", None) == username:
            return getattr(user, "ext_id", None)
    return None


def _find_trap_ext_id_by_attributes(
    module, clusters, cluster_ext_id, reciever_name, address_value
):
    """Look up an SNMP trap's ext_id by reciever_name (preferred) or IP address."""
    config = get_snmp_config(module, clusters, cluster_ext_id)
    for trap in getattr(config, "traps", None) or []:
        trap_name = getattr(trap, "reciever_name", None)
        if reciever_name and trap_name == reciever_name:
            return getattr(trap, "ext_id", None)
        if not reciever_name and address_value:
            addr = getattr(trap, "address", None)
            if addr is not None:
                ipv4 = getattr(addr, "ipv4", None)
                ipv6 = getattr(addr, "ipv6", None)
                if (ipv4 and getattr(ipv4, "value", None) == address_value) or (
                    ipv6 and getattr(ipv6, "value", None) == address_value
                ):
                    return getattr(trap, "ext_id", None)
    return None


def create_snmp_user(module, result, clusters):
    validate_required_params(module, ["username"])
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.SnmpUser()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating SNMP user create spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = clusters.create_snmp_user(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating SNMP user",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        # The task's entities_affected only carries the cluster; look up the
        # newly-created user by username from the cluster's SNMP config.
        ext_id = _find_user_ext_id_by_username(
            module, clusters, cluster_ext_id, module.params.get("username")
        )
        if ext_id:
            result["ext_id"] = ext_id
            user_resp = get_snmp_user(module, clusters, cluster_ext_id, ext_id)
            result["response"] = strip_internal_attributes(user_resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to resolve ext_id for newly created SNMP user"
                ),
                msg="Failed to resolve ext_id for newly created SNMP user",
            )
    result["changed"] = True


def update_snmp_user(module, result, clusters):
    validate_required_params(module, ["ext_id", "username"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.SnmpUser()
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating SNMP user update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    current_user = get_snmp_user(module, clusters, cluster_ext_id, ext_id)
    etag = get_etag(data=current_user)
    if not etag:
        module.fail_json(msg="Unable to fetch etag for updating SNMP user", **result)

    resp = None
    try:
        resp = clusters.update_snmp_user_by_id(
            clusterExtId=cluster_ext_id,
            extId=ext_id,
            body=update_spec,
            if_match=etag,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating SNMP user",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        user_resp = get_snmp_user(module, clusters, cluster_ext_id, ext_id)
        result["response"] = strip_internal_attributes(user_resp.to_dict())
    result["changed"] = True


def delete_snmp_user(module, result, clusters):
    validate_required_params(module, ["ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "SNMP user with ext_id:{0} will be deleted from cluster:{1}.".format(
                ext_id, cluster_ext_id
            )
        )
        return

    resp = None
    try:
        resp = clusters.delete_snmp_user_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting SNMP user",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id, raise_error=False)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


# ---------------------------------------------------------------------------
# SNMP traps
# ---------------------------------------------------------------------------


def create_snmp_trap(module, result, clusters):
    validate_required_params(module, ["address"])
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.SnmpTrap()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating SNMP trap create spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = clusters.create_snmp_trap(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating SNMP trap",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        # Task entities_affected only carries the cluster reference; look up the
        # newly-created trap by reciever_name or address from the SNMP config.
        address_value = None
        addr_param = module.params.get("address") or {}
        ipv4 = addr_param.get("ipv4") if isinstance(addr_param, dict) else None
        ipv6 = addr_param.get("ipv6") if isinstance(addr_param, dict) else None
        if ipv4 and ipv4.get("value"):
            address_value = ipv4.get("value")
        elif ipv6 and ipv6.get("value"):
            address_value = ipv6.get("value")
        ext_id = _find_trap_ext_id_by_attributes(
            module,
            clusters,
            cluster_ext_id,
            module.params.get("reciever_name"),
            address_value,
        )
        if ext_id:
            result["ext_id"] = ext_id
            trap_resp = get_snmp_trap(module, clusters, cluster_ext_id, ext_id)
            result["response"] = strip_internal_attributes(trap_resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to resolve ext_id for newly created SNMP trap"
                ),
                msg="Failed to resolve ext_id for newly created SNMP trap",
            )
    result["changed"] = True


def update_snmp_trap(module, result, clusters):
    validate_required_params(module, ["ext_id", "address"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.SnmpTrap()
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating SNMP trap update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    current_trap = get_snmp_trap(module, clusters, cluster_ext_id, ext_id)
    etag = get_etag(data=current_trap)
    if not etag:
        module.fail_json(msg="Unable to fetch etag for updating SNMP trap", **result)

    resp = None
    try:
        resp = clusters.update_snmp_trap_by_id(
            clusterExtId=cluster_ext_id,
            extId=ext_id,
            body=update_spec,
            if_match=etag,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating SNMP trap",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        trap_resp = get_snmp_trap(module, clusters, cluster_ext_id, ext_id)
        result["response"] = strip_internal_attributes(trap_resp.to_dict())
    result["changed"] = True


def delete_snmp_trap(module, result, clusters):
    validate_required_params(module, ["ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "SNMP trap with ext_id:{0} will be deleted from cluster:{1}.".format(
                ext_id, cluster_ext_id
            )
        )
        return

    resp = None
    try:
        resp = clusters.delete_snmp_trap_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting SNMP trap",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id, raise_error=False)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------


def create_SnmpConfigByClusterId(module, result, clusters):
    """Dispatch a create-type operation based on ``resource_type``."""
    resource_type = module.params.get("resource_type")
    if resource_type == "status":
        update_snmp_status(module, result, clusters)
    elif resource_type == "transport":
        add_snmp_transport(module, result, clusters)
    elif resource_type == "user":
        create_snmp_user(module, result, clusters)
    elif resource_type == "trap":
        create_snmp_trap(module, result, clusters)
    else:
        module.fail_json(
            msg="Unsupported resource_type '{0}' for state=present".format(
                resource_type
            ),
            **result,
        )


def update_SnmpConfigByClusterId(module, result, clusters):
    """Dispatch an update-type operation based on ``resource_type`` and ``ext_id``."""
    resource_type = module.params.get("resource_type")
    if resource_type == "user":
        update_snmp_user(module, result, clusters)
    elif resource_type == "trap":
        update_snmp_trap(module, result, clusters)
    else:
        module.fail_json(
            msg="Update operation is not supported for resource_type '{0}'. "
            "ext_id is only accepted for user and trap resource types.".format(
                resource_type
            ),
            **result,
        )


def delete_SnmpConfigByClusterId(module, result, clusters):
    """Dispatch a delete/remove-type operation based on ``resource_type``."""
    resource_type = module.params.get("resource_type")
    if resource_type == "transport":
        remove_snmp_transport(module, result, clusters)
    elif resource_type == "user":
        delete_snmp_user(module, result, clusters)
    elif resource_type == "trap":
        delete_snmp_trap(module, result, clusters)
    else:
        module.fail_json(
            msg="Delete operation is not supported for resource_type '{0}'.".format(
                resource_type
            ),
            **result,
        )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("resource_type", "status", ("is_enabled",)),
            ("resource_type", "transport", ("transports",)),
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
        "cluster_ext_id": module.params.get("cluster_ext_id"),
        "task_ext_id": None,
    }
    clusters = get_clusters_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_SnmpConfigByClusterId(module, result, clusters)
        else:
            create_SnmpConfigByClusterId(module, result, clusters)
    else:
        delete_SnmpConfigByClusterId(module, result, clusters)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
