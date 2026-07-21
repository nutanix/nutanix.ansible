#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpn_connection_v2
short_description: Create, Update, Delete VPN connections in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete VPN connections in Nutanix Prism Central.
  - A VPN connection interconnects a local network gateway (in a VPC or VLAN)
    with a remote gateway using IPSec/IKEv2 tunnels, and optionally advertises
    routes over BGP.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation. The required roles depend on the
      operation being performed.
    - >-
      B(Create/Update/Delete a VPN connection) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
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
      - Name of the VPN connection.
      - Required for create operation.
    type: str
    required: false
  description:
    description:
      - Free-form description for the VPN connection.
    type: str
    required: false
  local_gateway_reference:
    description:
      - External ID of the local network gateway to use as one end of the tunnel.
      - Required for create operation.
    type: str
    required: false
  remote_gateway_reference:
    description:
      - External ID of the remote network gateway to use as the other end of the tunnel.
      - Required for create operation.
    type: str
    required: false
  local_gateway_role:
    description:
      - Role played by the local gateway during IKE negotiation.
      - C(INITIATOR) actively opens the tunnel, C(ACCEPTOR) waits for the peer.
      - Required for create operation.
    type: str
    required: false
    choices:
      - INITIATOR
      - ACCEPTOR
  dynamic_route_priority:
    description:
      - Priority applied to routes learned dynamically through this VPN connection.
      - Lower values are preferred. Recommended range 100-1000.
    type: int
    required: false
  ipsec_config:
    description:
      - IPSec / IKE parameters used to establish the tunnel between the peer
        gateways.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      pre_shared_key:
        description:
          - Shared secret used to authenticate the two gateway peers.
          - This value is treated as sensitive and is not logged.
        type: str
        required: false
      local_vti_ip:
        description:
          - IP address of the local virtual tunnel interface (VTI).
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 form of the VTI address.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the IPv4 address (0-32).
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 form of the VTI address.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the IPv6 address (0-128).
                type: int
                required: false
                default: 128
      remote_vti_ip:
        description:
          - IP address of the remote virtual tunnel interface (VTI).
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 form of the VTI address.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the IPv4 address (0-32).
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 form of the VTI address.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the IPv6 address (0-128).
                type: int
                required: false
                default: 128
      local_authentication_id:
        description:
          - Identifier used by the local endpoint during IKE authentication.
        type: str
        required: false
      remote_authentication_id:
        description:
          - Identifier expected from the remote endpoint during IKE authentication.
        type: str
        required: false
      ike_lifetime_secs:
        description:
          - Lifetime, in seconds, of the IKE (Phase 1) security association
            before it is renegotiated.
        type: int
        required: false
      ipsec_lifetime_secs:
        description:
          - Lifetime, in seconds, of the IPSec (Phase 2) security association
            before it is renegotiated.
        type: int
        required: false
      esp_pfs_dh_group_number:
        description:
          - Diffie-Hellman group number to use for Perfect Forward Secrecy
            during ESP negotiation (0 disables PFS).
        type: int
        required: false
      ike_encryption_algorithm:
        description:
          - Encryption algorithm used during IKE (Phase 1) negotiation.
        type: str
        required: false
        choices:
          - AES128
          - AES256
          - AES256GCM128
          - TRIPLE_DES
      ike_authentication_algorithm:
        description:
          - Authentication algorithm used during IKE (Phase 1) negotiation.
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
          - Encryption algorithm used for the IPSec (Phase 2) SA.
        type: str
        required: false
        choices:
          - AES128
          - AES256
          - AES256GCM128
          - TRIPLE_DES
      ipsec_authentication_algorithm:
        description:
          - Authentication algorithm used for the IPSec (Phase 2) SA.
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
      - Dead-peer-detection configuration for the tunnel.
    type: dict
    required: false
    suboptions:
      operation:
        description:
          - Action taken by the local end when the remote peer is considered dead.
        type: str
        required: false
        choices:
          - CLEAR
          - HOLD
          - RESTART
      interval_secs:
        description:
          - Interval, in seconds, between DPD probes.
        type: int
        required: false
      timeout_secs:
        description:
          - Timeout, in seconds, after which a non-responsive peer is
            declared dead.
        type: int
        required: false
  qos_config:
    description:
      - Quality-of-Service limits applied to traffic on the tunnel.
    type: dict
    required: false
    suboptions:
      ingress_limit_mbps:
        description:
          - Ingress traffic limit in Mbps (0 or absent means unlimited).
        type: int
        required: false
      egress_limit_mbps:
        description:
          - Egress traffic limit in Mbps (0 or absent means unlimited).
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
- name: Create VPN connection
  nutanix.ncp.ntnx_vpn_connection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "vpn_connection_ansible"
    description: "VPN connection created by Ansible"
    local_gateway_reference: "1e04b1ef-6e2d-4cf1-8a67-8a5a70bb0a12"
    remote_gateway_reference: "b8c2ce0a-3a51-4c66-8f42-5ea1a3f9c6c4"
    local_gateway_role: "INITIATOR"
    dynamic_route_priority: 500
    ipsec_config:
      pre_shared_key: "MyStrongSharedKey!"
      local_vti_ip:
        ipv4:
          value: "169.254.10.1"
          prefix_length: 30
      remote_vti_ip:
        ipv4:
          value: "169.254.10.2"
          prefix_length: 30
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
      interval_secs: 30
      timeout_secs: 120
    qos_config:
      ingress_limit_mbps: 100
      egress_limit_mbps: 100
  register: result
  ignore_errors: true

- name: Update VPN connection
  nutanix.ncp.ntnx_vpn_connection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    name: "vpn_connection_ansible_updated"
    description: "Updated VPN connection description"
    local_gateway_reference: "1e04b1ef-6e2d-4cf1-8a67-8a5a70bb0a12"
    remote_gateway_reference: "b8c2ce0a-3a51-4c66-8f42-5ea1a3f9c6c4"
    local_gateway_role: "INITIATOR"
    dynamic_route_priority: 450
    ipsec_config:
      pre_shared_key: "MyStrongSharedKey!"
      ike_encryption_algorithm: "AES128"
      ike_authentication_algorithm: "SHA512"
      ipsec_encryption_algorithm: "AES128"
      ipsec_authentication_algorithm: "SHA512"
    dpd_config:
      operation: "HOLD"
      interval_secs: 60
      timeout_secs: 240
    qos_config:
      ingress_limit_mbps: 200
      egress_limit_mbps: 200
  register: result
  ignore_errors: true

- name: Delete VPN connection
  nutanix.ncp.ntnx_vpn_connection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting VPN connection.
    - If the operation is create or update and C(wait) is true, it will return the VPN connection details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "advertised_prefixes": null,
      "description": "VPN connection created by Ansible",
      "dpd_config": {
          "interval_secs": 30,
          "operation": "RESTART",
          "timeout_secs": 120
      },
      "dynamic_route_priority": 500,
      "ebgp_status": null,
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "ipsec_config": {
          "esp_pfs_dh_group_number": 14,
          "ike_authentication_algorithm": "SHA256",
          "ike_encryption_algorithm": "AES256",
          "ike_lifetime_secs": 28800,
          "ipsec_authentication_algorithm": "SHA256",
          "ipsec_encryption_algorithm": "AES256",
          "ipsec_lifetime_secs": 3600,
          "local_authentication_id": "local-id",
          "local_vti_ip": {
              "ipv4": {
                  "prefix_length": 30,
                  "value": "169.254.10.1"
              },
              "ipv6": null
          },
          "pre_shared_key": null,
          "remote_authentication_id": "remote-id",
          "remote_vti_ip": {
              "ipv4": {
                  "prefix_length": 30,
                  "value": "169.254.10.2"
              },
              "ipv6": null
          }
      },
      "ipsec_tunnel_status": null,
      "learned_prefixes": null,
      "links": null,
      "local_gateway_reference": "1e04b1ef-6e2d-4cf1-8a67-8a5a70bb0a12",
      "local_gateway_role": "INITIATOR",
      "metadata": null,
      "name": "vpn_connection_ansible",
      "qos_config": {
          "egress_limit_mbps": 100,
          "ingress_limit_mbps": 100
      },
      "remote_gateway_reference": "b8c2ce0a-3a51-4c66-8f42-5ea1a3f9c6c4",
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
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: always
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
  sample: "Api Exception raised while creating VPN connection"
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
        local_gateway_role=dict(
            type="str",
            choices=["INITIATOR", "ACCEPTOR"],
            obj=networking_sdk.GatewayRole,
        ),
        dynamic_route_priority=dict(type="int"),
        ipsec_config=dict(
            type="dict",
            options=ipsec_config_spec,
            obj=networking_sdk.IpsecConfig,
        ),
        dpd_config=dict(
            type="dict",
            options=dpd_config_spec,
            obj=networking_sdk.DpdConfig,
        ),
        qos_config=dict(
            type="dict",
            options=qos_config_spec,
            obj=networking_sdk.QosConfig,
        ),
    )
    return module_args


def create_vpn_connection(module, vpn_connections, result):
    validate_required_params(
        module,
        [
            "name",
            "local_gateway_reference",
            "remote_gateway_reference",
            "local_gateway_role",
            "ipsec_config",
        ],
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
        resp = vpn_connections.create_vpn_connection(body=spec)
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
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.VPN_CONNECTION
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_vpn_connection(module, vpn_connections, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for VPN Connection"
                ),
                msg="Failed to get entity ext_id from task for VPN Connection",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old = strip_internal_attributes(deepcopy(old_spec_dict))
    new = strip_internal_attributes(deepcopy(update_spec_dict))
    # Server-populated read-only fields must be ignored in diff.
    for field in [
        "advertised_prefixes",
        "learned_prefixes",
        "ipsec_tunnel_status",
        "ebgp_status",
    ]:
        old.pop(field, None)
        new.pop(field, None)
    return old == new


def update_vpn_connection(module, vpn_connections, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_vpn_connection(module, vpn_connections, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating VPN connection", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update VPN connection spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = vpn_connections.update_vpn_connection_by_id(
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
        resp = get_vpn_connection(module, vpn_connections, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_vpn_connection(module, vpn_connections, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "VPN connection with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = vpn_connections.delete_vpn_connection_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting VPN connection",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
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
    vpn_connections = get_vpn_connections_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_vpn_connection(module, vpn_connections, result)
        else:
            create_vpn_connection(module, vpn_connections, result)
    else:
        delete_vpn_connection(module, vpn_connections, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
