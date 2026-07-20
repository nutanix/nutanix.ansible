#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_layer2_stretche_v2
short_description: Create, Update, Delete Layer2 Stretch configurations in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Layer2 Stretch configurations in Nutanix Prism Central.
  - Layer2 Stretch (also known as L2 Network Extension) extends a Layer 2 domain across two Prism Central sites.
  - The stretch can be created over a VPN tunnel or a VXLAN tunnel between VTEP gateways.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Layer2 Stretch) -
      Required Roles: Prism Admin, Super Admin, VPC Admin, Network Infra Admin
    - >-
      B(Update a Layer2 Stretch) -
      Required Roles: Prism Admin, Super Admin, VPC Admin, Network Infra Admin
    - >-
      B(Delete a Layer2 Stretch) -
      Required Roles: Prism Admin, Super Admin, VPC Admin, Network Infra Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create Layer2 Stretch.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update Layer2 Stretch.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete Layer2 Stretch.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Layer2 Stretch configuration.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Layer2 Stretch configuration name.
      - Required for create operation.
      - Maximum 128 characters.
    type: str
    required: false
  description:
    description:
      - Layer2 stretch configuration details between subnets on two sites.
      - Maximum 1000 characters.
    type: str
    required: false
  connection_type:
    description:
      - Type of the connection used for stretching the subnet. The default is VPN.
    type: str
    required: false
    choices:
      - VPN
      - VXLAN
  mtu:
    description:
      - The MTU size setting for the VXLAN session.
      - Valid range is 500-8950.
    type: int
    required: false
  vni:
    description:
      - The VXLAN network identifier used to uniquely identify the VXLAN tunnel.
      - Valid range is 1-16777215.
    type: int
    required: false
  local_site_params:
    description:
      - Site-specific stretch configuration parameters for the local site.
    type: dict
    required: false
    suboptions:
      pc_cluster_reference:
        description:
          - Prism Central cluster reference for the local site.
        type: str
        required: false
      stretch_subnet_reference:
        description:
          - Reference to the local subnet that is being stretched.
        type: str
        required: false
      connection_reference:
        description:
          - The VPN connection or network gateway (with VTEP service) used for this Layer2 stretch on the local site.
        type: str
        required: false
      stretch_interface_ip_address:
        description:
          - IP address configuration for the local stretch interface.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address configuration.
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
          ipv6:
            description:
              - IPv6 address configuration.
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
      vpn_interface_ip_address:
        description:
          - IP address of the VPN interface used by the local site for the stretch.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address configuration.
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
          ipv6:
            description:
              - IPv6 address configuration.
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
      default_gateway_ip_address:
        description:
          - Default gateway IP address for the local stretched subnet.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address configuration.
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
          ipv6:
            description:
              - IPv6 address configuration.
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
      high_availability_group:
        description:
          - High availability group configuration for the local site.
        type: dict
        required: false
        suboptions:
          is_ha_enabled:
            description:
              - Indicates whether high availability is enabled.
            type: bool
            required: false
          algorithm:
            description:
              - High availability algorithm type used for the group.
            type: str
            required: false
            choices:
              - ACTIVE_BACKUP
          peered_gateways:
            description:
              - List of peered gateways in the high availability group.
            type: list
            elements: dict
            required: false
            suboptions:
              ext_id:
                description:
                  - External ID of the peered gateway.
                type: str
                required: true
  remote_site_params:
    description:
      - Site-specific stretch configuration parameters for the remote site.
    type: dict
    required: false
    suboptions:
      pc_cluster_reference:
        description:
          - Prism Central cluster reference for the remote site.
        type: str
        required: false
      stretch_subnet_reference:
        description:
          - Reference to the remote subnet that is being stretched.
        type: str
        required: false
      connection_reference:
        description:
          - The VPN connection or network gateway (with VTEP service) used for this Layer2 stretch on the remote site.
        type: str
        required: false
      stretch_interface_ip_address:
        description:
          - IP address configuration for the remote stretch interface.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address configuration.
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
          ipv6:
            description:
              - IPv6 address configuration.
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
      vpn_interface_ip_address:
        description:
          - IP address of the VPN interface used by the remote site for the stretch.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address configuration.
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
          ipv6:
            description:
              - IPv6 address configuration.
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
      default_gateway_ip_address:
        description:
          - Default gateway IP address for the remote stretched subnet.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address configuration.
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
          ipv6:
            description:
              - IPv6 address configuration.
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
      high_availability_group:
        description:
          - High availability group configuration for the remote site.
        type: dict
        required: false
        suboptions:
          is_ha_enabled:
            description:
              - Indicates whether high availability is enabled.
            type: bool
            required: false
          algorithm:
            description:
              - High availability algorithm type used for the group.
            type: str
            required: false
            choices:
              - ACTIVE_BACKUP
          peered_gateways:
            description:
              - List of peered gateways in the high availability group.
            type: list
            elements: dict
            required: false
            suboptions:
              ext_id:
                description:
                  - External ID of the peered gateway.
                type: str
                required: true
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
- name: Create Layer2 Stretch over VPN
  nutanix.ncp.ntnx_layer2_stretche_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "l2_stretch_vpn_ansible"
    description: "Layer2 Stretch over VPN created by Ansible"
    connection_type: "VPN"
    local_site_params:
      pc_cluster_reference: "5ab1b1a2-1111-4e00-9999-0000000000aa"
      stretch_subnet_reference: "8b5df6bc-1111-4e00-9999-0000000000bb"
      connection_reference: "3f9e5c2d-1111-4e00-9999-0000000000cc"
    remote_site_params:
      pc_cluster_reference: "6bc2b2b3-2222-4e00-9999-0000000000dd"
      stretch_subnet_reference: "9c6ef7cd-2222-4e00-9999-0000000000ee"
      connection_reference: "4a0f6d3e-2222-4e00-9999-0000000000ff"
  register: result
  ignore_errors: true

- name: Create Layer2 Stretch over VXLAN with HA
  nutanix.ncp.ntnx_layer2_stretche_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "l2_stretch_vxlan_ansible"
    description: "Layer2 Stretch over VXLAN created by Ansible"
    connection_type: "VXLAN"
    mtu: 1500
    vni: 100000
    local_site_params:
      pc_cluster_reference: "5ab1b1a2-1111-4e00-9999-0000000000aa"
      stretch_subnet_reference: "8b5df6bc-1111-4e00-9999-0000000000bb"
      connection_reference: "3f9e5c2d-1111-4e00-9999-0000000000cc"
      high_availability_group:
        is_ha_enabled: true
        algorithm: "ACTIVE_BACKUP"
        peered_gateways:
          - ext_id: "1a2b3c4d-1111-4e00-9999-000000000011"
    remote_site_params:
      pc_cluster_reference: "6bc2b2b3-2222-4e00-9999-0000000000dd"
      stretch_subnet_reference: "9c6ef7cd-2222-4e00-9999-0000000000ee"
      connection_reference: "4a0f6d3e-2222-4e00-9999-0000000000ff"
  register: result
  ignore_errors: true

- name: Update Layer2 Stretch description
  nutanix.ncp.ntnx_layer2_stretche_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "l2_stretch_vpn_ansible_updated"
    description: "Updated Layer2 Stretch description"
    connection_type: "VPN"
  register: result
  ignore_errors: true

- name: Delete Layer2 Stretch
  nutanix.ncp.ntnx_layer2_stretche_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting Layer2 Stretch
    - If the operation is create or update and C(wait) is true, it will return the Layer2 Stretch details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
      "connection_type": "VPN",
      "description": "Layer2 Stretch over VPN created by Ansible",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "high_availability_status": null,
      "links": null,
      "local_site_params": {
        "connection_reference": "3f9e5c2d-1111-4e00-9999-0000000000cc",
        "default_gateway_ip_address": null,
        "high_availability_group": null,
        "pc_cluster_reference": "5ab1b1a2-1111-4e00-9999-0000000000aa",
        "stretch_interface_ip_address": null,
        "stretch_subnet_reference": "8b5df6bc-1111-4e00-9999-0000000000bb",
        "vpn_interface_ip_address": null
      },
      "metadata": null,
      "mtu": null,
      "name": "l2_stretch_vpn_ansible",
      "remote_site_params": {
        "connection_reference": "4a0f6d3e-2222-4e00-9999-0000000000ff",
        "default_gateway_ip_address": null,
        "high_availability_group": null,
        "pc_cluster_reference": "6bc2b2b3-2222-4e00-9999-0000000000dd",
        "stretch_interface_ip_address": null,
        "stretch_subnet_reference": "9c6ef7cd-2222-4e00-9999-0000000000ee",
        "vpn_interface_ip_address": null
      },
      "remote_stretch_status": null,
      "stretch_status": null,
      "tenant_id": null,
      "vni": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the Layer2 Stretch.
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
  sample: "Api Exception raised while creating Layer2 Stretch"
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
    get_layer2_stretches_api_instance,
)
from ..module_utils.v4.network.helpers import get_layer2_stretch  # noqa: E402
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

# Read-only fields returned by the API that must never be sent back on update
READ_ONLY_FIELDS = (
    "stretch_status",
    "remote_stretch_status",
    "high_availability_status",
    "metadata",
    "links",
    "tenant_id",
)


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

    peered_gateway_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    high_availability_group_spec = dict(
        is_ha_enabled=dict(type="bool", required=False),
        algorithm=dict(
            type="str",
            required=False,
            choices=["ACTIVE_BACKUP"],
            obj=networking_sdk.HighAvailabilityAlgorithm,
        ),
        peered_gateways=dict(
            type="list",
            elements="dict",
            options=peered_gateway_spec,
            required=False,
            obj=networking_sdk.PeeredGateway,
        ),
    )

    site_params_spec = dict(
        pc_cluster_reference=dict(type="str", required=False),
        stretch_subnet_reference=dict(type="str", required=False),
        connection_reference=dict(type="str", required=False),
        stretch_interface_ip_address=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        vpn_interface_ip_address=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        default_gateway_ip_address=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        high_availability_group=dict(
            type="dict",
            options=high_availability_group_spec,
            required=False,
            obj=networking_sdk.HighAvailabilityGroup,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        connection_type=dict(
            type="str",
            choices=["VPN", "VXLAN"],
            obj=networking_sdk.StretchConnectionType,
        ),
        mtu=dict(type="int"),
        vni=dict(type="int"),
        local_site_params=dict(
            type="dict",
            options=site_params_spec,
            obj=networking_sdk.SiteParams,
        ),
        remote_site_params=dict(
            type="dict",
            options=site_params_spec,
            obj=networking_sdk.SiteParams,
        ),
    )
    return module_args


def create_layer2_stretche(module, result, api_instance):
    validate_required_params(module, ["name"])
    sg = SpecGenerator(module)
    default_spec = networking_sdk.Layer2Stretch()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create Layer2 Stretch spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_layer2_stretch(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Layer2 Stretch",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.LAYER2_STRETCH
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_layer2_stretch(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Layer2 Stretch"
                ),
                msg="Failed to get entity ext_id from task for Layer2 Stretch",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    for field in READ_ONLY_FIELDS:
        old_spec_dict.pop(field, None)
        update_spec_dict.pop(field, None)
    return old_spec_dict == update_spec_dict


def update_layer2_stretche(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_layer2_stretch(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating Layer2 Stretch", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update Layer2 Stretch spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Layer2 Stretch is already in the desired state.",
            **result,
        )

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_layer2_stretch_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Layer2 Stretch",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_layer2_stretch(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_layer2_stretche(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Layer2 Stretch with ext_id:{0} will be deleted.".format(ext_id)
        return

    old_spec = get_layer2_stretch(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.delete_layer2_stretch_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Layer2 Stretch",
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
    api_instance = get_layer2_stretches_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_layer2_stretche(module, result, api_instance)
        else:
            create_layer2_stretche(module, result, api_instance)
    else:
        delete_layer2_stretche(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
