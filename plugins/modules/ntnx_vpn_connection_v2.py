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
  - A VPN connection provides secure IKEv2/IPsec point-to-point connectivity between a Nutanix overlay
    network (VPC) and an external network reachable through a remote VPN gateway.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a VPN Connection) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - >-
      B(Update a VPN Connection) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - >-
      B(Delete a VPN Connection) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create the VPN connection.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the VPN connection.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the VPN connection.
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
      - External ID of the local (Nutanix side) VPN gateway used for this VPN connection.
      - Required for create operation.
    type: str
    required: false
  remote_gateway_reference:
    description:
      - External ID of the remote peer VPN gateway used for this VPN connection.
      - Required for create operation.
    type: str
    required: false
  local_gateway_role:
    description:
      - Role of the local gateway during IKE negotiation.
      - Required for create operation.
    type: str
    required: false
    choices:
      - INITIATOR
      - ACCEPTOR
  dynamic_route_priority:
    description:
      - Priority used to select routes learned dynamically over this VPN connection.
    type: int
    required: false
  ipsec_config:
    description:
      - IPSec configuration used by the VPN connection.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      pre_shared_key:
        description:
          - Shared secret for authentication between the two gateway peers.
          - This value is never logged.
        type: str
        required: false
      local_vti_ip:
        description:
          - IP address of the local Virtual Tunnel Interface (VTI).
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address value for the local VTI.
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
                  - Prefix length of the IPv4 address.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address value for the local VTI.
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
                  - Prefix length of the IPv6 address.
                type: int
                required: false
                default: 128
      remote_vti_ip:
        description:
          - IP address of the remote Virtual Tunnel Interface (VTI).
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address value for the remote VTI.
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
                  - Prefix length of the IPv4 address.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address value for the remote VTI.
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
                  - Prefix length of the IPv6 address.
                type: int
                required: false
                default: 128
      local_authentication_id:
        description:
          - IKE authentication identifier used by the local peer.
        type: str
        required: false
      remote_authentication_id:
        description:
          - IKE authentication identifier used by the remote peer.
        type: str
        required: false
      ike_lifetime_secs:
        description:
          - Lifetime, in seconds, for the IKE (phase 1) security association.
        type: int
        required: false
      ipsec_lifetime_secs:
        description:
          - Lifetime, in seconds, for the IPSec (phase 2) security association.
        type: int
        required: false
      esp_pfs_dh_group_number:
        description:
          - Diffie-Hellman group number used for Perfect Forward Secrecy for ESP.
        type: int
        required: false
      ike_encryption_algorithm:
        description:
          - Encryption algorithm used during IKE (phase 1) negotiation.
        type: str
        required: false
        choices:
          - AES128
          - AES256
          - AES256GCM128
          - TRIPLE_DES
      ike_authentication_algorithm:
        description:
          - Authentication algorithm used during IKE (phase 1) negotiation.
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
          - Encryption algorithm used for IPSec (phase 2).
        type: str
        required: false
        choices:
          - AES128
          - AES256
          - AES256GCM128
          - TRIPLE_DES
      ipsec_authentication_algorithm:
        description:
          - Authentication algorithm used for IPSec (phase 2).
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
      - Dead Peer Detection (DPD) configuration used to detect stalled tunnels.
    type: dict
    required: false
    suboptions:
      operation:
        description:
          - DPD action to take when a peer is found unreachable.
        type: str
        required: false
        choices:
          - CLEAR
          - HOLD
          - RESTART
      interval_secs:
        description:
          - Interval (in seconds) between DPD probes.
        type: int
        required: false
      timeout_secs:
        description:
          - Timeout (in seconds) after which the peer is declared dead.
        type: int
        required: false
  qos_config:
    description:
      - Quality of Service configuration to shape traffic through the VPN tunnel.
    type: dict
    required: false
    suboptions:
      ingress_limit_mbps:
        description:
          - Ingress traffic limit in Mbps.
        type: int
        required: false
      egress_limit_mbps:
        description:
          - Egress traffic limit in Mbps.
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
- name: Create VPN connection with minimum attributes
  nutanix.ncp.ntnx_vpn_connection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "vpn_connection_ansible"
    local_gateway_reference: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    remote_gateway_reference: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

- name: Create VPN connection with all attributes
  nutanix.ncp.ntnx_vpn_connection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "vpn_connection_ansible_full"
    description: "VPN connection created by Ansible with all attributes"
    local_gateway_reference: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    remote_gateway_reference: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    local_gateway_role: "INITIATOR"
    dynamic_route_priority: 100
    ipsec_config:
      pre_shared_key: "Nutanix.Ipsec.Psk.123"
      local_vti_ip:
        ipv4:
          value: "169.254.1.1"
          prefix_length: 30
      remote_vti_ip:
        ipv4:
          value: "169.254.1.2"
          prefix_length: 30
      local_authentication_id: "10.0.0.1"
      remote_authentication_id: "10.0.0.2"
      ike_lifetime_secs: 86400
      ipsec_lifetime_secs: 43200
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

- name: Update VPN connection
  nutanix.ncp.ntnx_vpn_connection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "6b0d70b5-6ce8-4116-b46a-4b1c9e8f83fd"
    name: "vpn_connection_ansible_updated"
    description: "Updated VPN connection description"
    local_gateway_reference: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    remote_gateway_reference: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    dynamic_route_priority: 200

- name: Delete VPN connection
  nutanix.ncp.ntnx_vpn_connection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "6b0d70b5-6ce8-4116-b46a-4b1c9e8f83fd"
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
        "description": "VPN connection created by Ansible with all attributes",
        "dpd_config": {
            "interval_secs": 30,
            "operation": "RESTART",
            "timeout_secs": 120
        },
        "dynamic_route_priority": 100,
        "ebgp_status": null,
        "ext_id": "6b0d70b5-6ce8-4116-b46a-4b1c9e8f83fd",
        "ipsec_config": {
            "esp_pfs_dh_group_number": 14,
            "ike_authentication_algorithm": "SHA256",
            "ike_encryption_algorithm": "AES256",
            "ike_lifetime_secs": 86400,
            "ipsec_authentication_algorithm": "SHA256",
            "ipsec_encryption_algorithm": "AES256",
            "ipsec_lifetime_secs": 43200,
            "local_authentication_id": "10.0.0.1",
            "local_vti_ip": {
                "ipv4": {
                    "prefix_length": 30,
                    "value": "169.254.1.1"
                },
                "ipv6": null
            },
            "pre_shared_key": null,
            "remote_authentication_id": "10.0.0.2",
            "remote_vti_ip": {
                "ipv4": {
                    "prefix_length": 30,
                    "value": "169.254.1.2"
                },
                "ipv6": null
            }
        },
        "ipsec_tunnel_status": null,
        "learned_prefixes": null,
        "links": null,
        "local_gateway_reference": "2e40ff57-20aa-4d2b-b179-298db969c20d",
        "local_gateway_role": "INITIATOR",
        "metadata": null,
        "name": "vpn_connection_ansible_full",
        "qos_config": {
            "egress_limit_mbps": 100,
            "ingress_limit_mbps": 100
        },
        "remote_gateway_reference": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
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
  sample: "6b0d70b5-6ce8-4116-b46a-4b1c9e8f83fd"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the operation was skipped due to idempotency.
  returned: always
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
  description: This indicates the message describing the outcome of the operation.
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
    strip_read_only_fields,
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


def create_vpn_connection(module, api_instance, result):
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
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.VPN_CONNECTION
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_vpn_connection(module, api_instance, ext_id)
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
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    return old_spec_dict == update_spec_dict


def update_vpn_connection(module, api_instance, result):
    ext_id = module.params.get("ext_id")

    result["ext_id"] = ext_id
    old_spec = get_vpn_connection(module, api_instance, ext_id)
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
        module.exit_json(msg="Nothing to change.")

    strip_read_only_fields(
        update_spec,
        fields=[
            "ipsec_tunnel_status",
            "ebgp_status",
            "learned_prefixes",
        ],
    )

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


def delete_vpn_connection(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "VPN connection with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_vpn_connection(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

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
    api_instance = get_vpn_connections_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_vpn_connection(module, api_instance, result)
        else:
            create_vpn_connection(module, api_instance, result)
    else:
        delete_vpn_connection(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
