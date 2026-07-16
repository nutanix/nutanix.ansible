#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_VpnConnection_v2
short_description: Create, Update, Delete VPN connections in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to create, update, and delete VPN connections in Nutanix Prism Central.
  - A VPN connection couples a local VPN gateway to a remote VPN gateway using an IPSec tunnel.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a VPN connection) -
      Required Roles: Account Owner, Administrator, Prism Admin, Super Admin, VPC Admin
    - >-
      B(Update a VPN connection) -
      Required Roles: Account Owner, Administrator, Prism Admin, Super Admin, VPC Admin
    - >-
      B(Delete a VPN connection) -
      Required Roles: Account Owner, Administrator, Prism Admin, Super Admin, VPC Admin
    - Requires the referenced local and remote VPN gateways to exist before creating the connection.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create VPN connection.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update VPN connection.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete VPN connection.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the VPN connection.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - VPN connection name.
      - Required for create operation.
    type: str
    required: false
  description:
    description:
      - Description of the VPN connection.
    type: str
    required: false
  local_gateway_reference:
    description:
      - External ID (UUID) of the local VPN gateway that is one end of the connection.
      - Required for create operation.
    type: str
    required: false
  remote_gateway_reference:
    description:
      - External ID (UUID) of the remote VPN gateway that is the other end of the connection.
      - Required for create operation.
    type: str
    required: false
  ipsec_config:
    description:
      - IPSec configuration for the VPN connection.
    type: dict
    required: false
    suboptions:
      pre_shared_key:
        description:
          - Shared secret used for authentication between the gateway peers.
          - Handled as a secret; not logged.
        type: str
        required: false
      local_vti_ip:
        description:
          - Local VTI (Virtual Tunnel Interface) IP address.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address of the local VTI.
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
                  - Prefix length of the IPv4 network.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address of the local VTI.
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
                  - Prefix length of the IPv6 network.
                type: int
                required: false
                default: 128
      remote_vti_ip:
        description:
          - Remote VTI (Virtual Tunnel Interface) IP address.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address of the remote VTI.
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
                  - Prefix length of the IPv4 network.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address of the remote VTI.
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
                  - Prefix length of the IPv6 network.
                type: int
                required: false
                default: 128
      local_authentication_id:
        description:
          - Local authentication ID for IPSec.
        type: str
        required: false
      remote_authentication_id:
        description:
          - Remote authentication ID for IPSec.
        type: str
        required: false
      ike_lifetime_secs:
        description:
          - Lifetime of the IKE Security Association (SA) in seconds.
        type: int
        required: false
      ipsec_lifetime_secs:
        description:
          - Lifetime of the IPSec Security Association (SA) in seconds.
        type: int
        required: false
      esp_pfs_dh_group_number:
        description:
          - Diffie-Hellman group number used for the IPSec Perfect Forward Secrecy (PFS).
        type: int
        required: false
      ike_encryption_algorithm:
        description:
          - Encryption algorithm used by the IKE protocol.
        type: str
        required: false
        choices:
          - AES128
          - AES256
          - AES256GCM128
          - TRIPLE_DES
      ike_authentication_algorithm:
        description:
          - Authentication algorithm used by the IKE protocol.
        type: str
        required: false
        choices:
          - MD5
          - SHA1
          - SHA256
          - SHA384
          - SHA512
      ipsec_encryption_algorithm:
        description:
          - Encryption algorithm used by the IPSec protocol.
        type: str
        required: false
        choices:
          - AES128
          - AES256
          - AES256GCM128
          - TRIPLE_DES
      ipsec_authentication_algorithm:
        description:
          - Authentication algorithm used by the IPSec protocol.
        type: str
        required: false
        choices:
          - MD5
          - SHA1
          - SHA256
          - SHA384
          - SHA512
  dpd_config:
    description:
      - Dead Peer Detection (DPD) configuration for the VPN connection.
    type: dict
    required: false
    suboptions:
      operation:
        description:
          - Action to take when the peer is detected as dead.
        type: str
        required: false
        choices:
          - CLEAR
          - HOLD
          - RESTART
      interval_secs:
        description:
          - Interval (in seconds) between DPD messages sent by the gateway.
        type: int
        required: false
      timeout_secs:
        description:
          - Amount of time (in seconds) to wait for a response before considering the peer dead.
        type: int
        required: false
  qos_config:
    description:
      - Quality of Service (QoS) configuration for the VPN IPSec tunnel.
    type: dict
    required: false
    suboptions:
      ingress_limit_mbps:
        description:
          - Ingress (inbound) traffic bandwidth limit in Mbps.
        type: int
        required: false
      egress_limit_mbps:
        description:
          - Egress (outbound) traffic bandwidth limit in Mbps.
        type: int
        required: false
  local_gateway_role:
    description:
      - Role of the local gateway in this VPN connection.
      - C(INITIATOR) actively opens the IKE negotiation.
      - C(ACCEPTOR) waits for the peer to open the IKE negotiation.
    type: str
    required: false
    choices:
      - INITIATOR
      - ACCEPTOR
  dynamic_route_priority:
    description:
      - Priority used to rank the dynamic routes learned over this VPN connection.
    type: int
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create VPN connection with minimum parameters
  nutanix.ncp.ntnx_VpnConnection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "vpn_connection_ansible"
    local_gateway_reference: "6b7c07d9-4c47-4a2b-84b9-4c1b8e0f30a4"
    remote_gateway_reference: "a2ffe73d-a1e3-4c7d-b8a0-3e8ba52a2d19"
  register: result
  ignore_errors: true

- name: Create VPN connection with all parameters
  nutanix.ncp.ntnx_VpnConnection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "vpn_connection_ansible_full"
    description: "VPN connection created by Ansible"
    local_gateway_reference: "6b7c07d9-4c47-4a2b-84b9-4c1b8e0f30a4"
    remote_gateway_reference: "a2ffe73d-a1e3-4c7d-b8a0-3e8ba52a2d19"
    local_gateway_role: "INITIATOR"
    dynamic_route_priority: 100
    ipsec_config:
      pre_shared_key: "s3cr3t-pre-shared-key"
      local_authentication_id: "local-id"
      remote_authentication_id: "remote-id"
      ike_lifetime_secs: 28800
      ipsec_lifetime_secs: 3600
      esp_pfs_dh_group_number: 14
      ike_encryption_algorithm: "AES256"
      ike_authentication_algorithm: "SHA256"
      ipsec_encryption_algorithm: "AES256"
      ipsec_authentication_algorithm: "SHA256"
    dpd_config:
      operation: "RESTART"
      interval_secs: 10
      timeout_secs: 30
    qos_config:
      ingress_limit_mbps: 100
      egress_limit_mbps: 100
  register: result
  ignore_errors: true

- name: Update VPN connection
  nutanix.ncp.ntnx_VpnConnection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "9b3d8c5c-7e2a-4a70-bad3-8f5d94a9b0b1"
    name: "vpn_connection_ansible_updated"
    description: "Updated VPN connection description"
    dynamic_route_priority: 200
    qos_config:
      ingress_limit_mbps: 200
      egress_limit_mbps: 200
  register: result
  ignore_errors: true

- name: Delete VPN connection
  nutanix.ncp.ntnx_VpnConnection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "9b3d8c5c-7e2a-4a70-bad3-8f5d94a9b0b1"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting VPN connection
    - If the operation is create or update and C(wait) is true, it will return the VPN connection details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
      "advertised_prefixes": null,
      "description": "VPN connection created by Ansible",
      "dpd_config": {
        "interval_secs": 10,
        "operation": "RESTART",
        "timeout_secs": 30
      },
      "dynamic_route_priority": 100,
      "ebgp_status": null,
      "ext_id": "9b3d8c5c-7e2a-4a70-bad3-8f5d94a9b0b1",
      "ipsec_config": {
        "esp_pfs_dh_group_number": 14,
        "ike_authentication_algorithm": "SHA256",
        "ike_encryption_algorithm": "AES256",
        "ike_lifetime_secs": 28800,
        "ipsec_authentication_algorithm": "SHA256",
        "ipsec_encryption_algorithm": "AES256",
        "ipsec_lifetime_secs": 3600,
        "local_authentication_id": "local-id",
        "local_vti_ip": null,
        "pre_shared_key": null,
        "remote_authentication_id": "remote-id",
        "remote_vti_ip": null
      },
      "ipsec_tunnel_status": null,
      "learned_prefixes": null,
      "links": null,
      "local_gateway_reference": "6b7c07d9-4c47-4a2b-84b9-4c1b8e0f30a4",
      "local_gateway_role": "INITIATOR",
      "metadata": null,
      "name": "vpn_connection_ansible_full",
      "qos_config": {
        "egress_limit_mbps": 100,
        "ingress_limit_mbps": 100
      },
      "remote_gateway_reference": "a2ffe73d-a1e3-4c7d-b8a0-3e8ba52a2d19",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the VPN connection.
  returned: always
  type: str
  sample: "9b3d8c5c-7e2a-4a70-bad3-8f5d94a9b0b1"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - Indicates the operation was skipped (nothing to change or already exists).
  returned: when applicable
  type: bool
  sample: true

msg:
  description:
    - Status or informational message.
    - Populated in idempotent, check mode, or error scenarios.
  returned: when there is an error, module is idempotent, or check mode (in delete operation)
  type: str
  sample: "VpnConnection with name 'vpn_connection_ansible' already exists. Skipping creation."

error:
  description: This indicates the error message if any error occurred
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_vpn_connections_api_instance,
)
from ..module_utils.v4.network.helpers import get_vpn_connection  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=networking_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=networking_sdk.IPv6Address,
        ),
    )

    ipsec_config_spec = dict(
        pre_shared_key=dict(type="str", required=False, no_log=True),
        local_vti_ip=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        remote_vti_ip=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        local_authentication_id=dict(type="str", required=False),
        remote_authentication_id=dict(type="str", required=False),
        ike_lifetime_secs=dict(type="int", required=False),
        ipsec_lifetime_secs=dict(type="int", required=False),
        esp_pfs_dh_group_number=dict(type="int", required=False),
        ike_encryption_algorithm=dict(
            type="str",
            required=False,
            choices=["AES128", "AES256", "AES256GCM128", "TRIPLE_DES"],
            obj=networking_sdk.EncryptionAlgorithm,
        ),
        ike_authentication_algorithm=dict(
            type="str",
            required=False,
            choices=["MD5", "SHA1", "SHA256", "SHA384", "SHA512"],
            obj=networking_sdk.AuthenticationAlgorithm,
        ),
        ipsec_encryption_algorithm=dict(
            type="str",
            required=False,
            choices=["AES128", "AES256", "AES256GCM128", "TRIPLE_DES"],
            obj=networking_sdk.EncryptionAlgorithm,
        ),
        ipsec_authentication_algorithm=dict(
            type="str",
            required=False,
            choices=["MD5", "SHA1", "SHA256", "SHA384", "SHA512"],
            obj=networking_sdk.AuthenticationAlgorithm,
        ),
    )

    dpd_config_spec = dict(
        operation=dict(
            type="str",
            required=False,
            choices=["CLEAR", "HOLD", "RESTART"],
            obj=networking_sdk.DpdOperation,
        ),
        interval_secs=dict(type="int", required=False),
        timeout_secs=dict(type="int", required=False),
    )

    qos_config_spec = dict(
        ingress_limit_mbps=dict(type="int", required=False),
        egress_limit_mbps=dict(type="int", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        local_gateway_reference=dict(type="str"),
        remote_gateway_reference=dict(type="str"),
        ipsec_config=dict(
            type="dict",
            options=ipsec_config_spec,
            required=False,
            obj=networking_sdk.IpsecConfig,
        ),
        dpd_config=dict(
            type="dict",
            options=dpd_config_spec,
            required=False,
            obj=networking_sdk.DpdConfig,
        ),
        qos_config=dict(
            type="dict",
            options=qos_config_spec,
            required=False,
            obj=networking_sdk.QosConfig,
        ),
        local_gateway_role=dict(
            type="str",
            required=False,
            choices=["INITIATOR", "ACCEPTOR"],
            obj=networking_sdk.GatewayRole,
        ),
        dynamic_route_priority=dict(type="int", required=False),
    )
    return module_args


def create_VpnConnection(module, result, api_instance):
    validate_required_params(
        module, ["name", "local_gateway_reference", "remote_gateway_reference"]
    )
    sg = SpecGenerator(module)
    default_spec = networking_sdk.VpnConnection()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create VPN connection spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_vpn_connection(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating VPN connection",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.VPN_CONNECTION
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_vpn_connection(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_vpn_connection_idempotency(old_spec, update_spec):
    """Return True when there are no differences between old and update specs."""
    old_spec = strip_internal_attributes(deepcopy(old_spec))
    update_spec = strip_internal_attributes(deepcopy(update_spec))
    return old_spec == update_spec


def update_VpnConnection(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_vpn_connection(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating VPN connection", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update VPN connection spec", **result)

    if check_vpn_connection_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.update_vpn_connection_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating VPN connection",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_vpn_connection(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_VpnConnection(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "VPN connection with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_vpn_connection(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.delete_vpn_connection_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting VPN connection",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, raise_error=True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_vpn_connections_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_VpnConnection(module, result, api_instance)
        else:
            create_VpnConnection(module, result, api_instance)
    else:
        delete_VpnConnection(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
