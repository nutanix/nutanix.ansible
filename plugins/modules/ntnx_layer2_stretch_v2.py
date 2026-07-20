#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_layer2_stretch_v2
short_description: Create, Update, Delete Layer2Stretch configurations in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Layer2Stretch configurations in Nutanix Prism Central.
  - A Layer2Stretch stretches a layer-2 subnet across two sites (local and remote) so that VMs in both sites can share the same broadcast domain.
  - Both C(VPN) (site to site tunnels) and C(VXLAN) (VTEP based) connection types are supported.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Layer2Stretch) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - >-
      B(Update a Layer2Stretch) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - >-
      B(Delete a Layer2Stretch) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create Layer2Stretch.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update Layer2Stretch.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete Layer2Stretch.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Layer2Stretch configuration.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Layer2Stretch configuration name.
      - Required for create operation.
      - Maximum 128 characters.
    type: str
    required: false
  description:
    description:
      - Free-form description for the Layer2Stretch configuration.
    type: str
    required: false
  connection_type:
    description:
      - Type of connection used to build the layer-2 stretch between the two sites.
      - C(VPN) uses a site to site VPN tunnel between local and remote gateway.
      - C(VXLAN) uses VTEP encapsulation between local and remote VTEP gateways.
      - Required for create operation.
    type: str
    required: false
    choices:
      - VPN
      - VXLAN
  mtu:
    description:
      - MTU (in bytes) of the stretched layer-2 segment.
    type: int
    required: false
  vni:
    description:
      - VXLAN Network Identifier used to identify the stretched segment on the wire.
      - Applicable primarily when C(connection_type) is C(VXLAN).
    type: int
    required: false
  local_site_params:
    description:
      - Layer2Stretch parameters for the LOCAL site (the site the API call is issued against).
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      pc_cluster_reference:
        description:
          - Reference to the Prism Central cluster hosting the local site.
        type: str
        required: false
      stretch_subnet_reference:
        description:
          - Reference to the subnet on the local site that is being stretched.
        type: str
        required: false
      connection_reference:
        description:
          - Reference to the local gateway/connection used to build the stretch.
          - For C(VPN) this points to the local VPN connection.
          - For C(VXLAN) this points to the local VTEP gateway.
        type: str
        required: false
      stretch_interface_ip_address:
        description:
          - IP address of the interface used to terminate the stretch on the local site.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 128
      vpn_interface_ip_address:
        description:
          - IP address of the VPN interface for the local site (only applicable to C(VPN) stretches).
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 128
      default_gateway_ip_address:
        description:
          - Default gateway IP address to reach the remote site from the local site.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 128
      high_availability_group:
        description:
          - High-availability group configuration for the local site.
        type: dict
        required: false
        suboptions:
          is_ha_enabled:
            description:
              - Indicates whether high availability is enabled for this site.
            type: bool
            required: false
          algorithm:
            description:
              - High-availability algorithm used inside the group.
            type: str
            required: false
            choices:
              - ACTIVE_BACKUP
          peered_gateways:
            description:
              - List of peered gateways participating in this high-availability group.
            type: list
            elements: dict
            required: false
            suboptions:
              ext_id:
                description:
                  - External ID of the peered gateway.
                type: str
                required: false
  remote_site_params:
    description:
      - Layer2Stretch parameters for the REMOTE site.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      pc_cluster_reference:
        description:
          - Reference to the Prism Central cluster hosting the remote site.
        type: str
        required: false
      stretch_subnet_reference:
        description:
          - Reference to the subnet on the remote site that is being stretched.
        type: str
        required: false
      connection_reference:
        description:
          - Reference to the remote gateway/connection used to build the stretch.
        type: str
        required: false
      stretch_interface_ip_address:
        description:
          - IP address of the interface used to terminate the stretch on the remote site.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 128
      vpn_interface_ip_address:
        description:
          - IP address of the VPN interface for the remote site (only applicable to C(VPN) stretches).
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 128
      default_gateway_ip_address:
        description:
          - Default gateway IP address to reach the local site from the remote site.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address.
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
                  - Prefix length of the network.
                type: int
                required: false
                default: 128
      high_availability_group:
        description:
          - High-availability group configuration for the remote site.
        type: dict
        required: false
        suboptions:
          is_ha_enabled:
            description:
              - Indicates whether high availability is enabled for this site.
            type: bool
            required: false
          algorithm:
            description:
              - High-availability algorithm used inside the group.
            type: str
            required: false
            choices:
              - ACTIVE_BACKUP
          peered_gateways:
            description:
              - List of peered gateways participating in this high-availability group.
            type: list
            elements: dict
            required: false
            suboptions:
              ext_id:
                description:
                  - External ID of the peered gateway.
                type: str
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
- name: Create VPN based Layer2Stretch
  nutanix.ncp.ntnx_layer2_stretch_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "layer2_stretch_ansible"
    description: "Layer2Stretch created by Ansible"
    connection_type: "VPN"
    mtu: 1500
    local_site_params:
      pc_cluster_reference: "18553f0f-7ce0-4c33-a697-0eecfb27fc10"
      stretch_subnet_reference: "b0cce620-3654-8522-9876-a91e2c037862"
      connection_reference: "a4f3f04f-1222-8544-7896-28b62bcc3e3e"
    remote_site_params:
      pc_cluster_reference: "78e0d3ac-9e08-4d0c-8f1c-3d90ac2a55f0"
      stretch_subnet_reference: "b7c94b93-2222-3333-4444-91e2c0378621"
      connection_reference: "e7f3f04f-2222-3333-4444-28b62bcc3e3f"
  register: result
  ignore_errors: true

- name: Update Layer2Stretch description and MTU
  nutanix.ncp.ntnx_layer2_stretch_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "layer2_stretch_ansible_updated"
    description: "Updated Layer2Stretch description"
    mtu: 9000
  register: result
  ignore_errors: true

- name: Delete Layer2Stretch
  nutanix.ncp.ntnx_layer2_stretch_v2:
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
    - Response for creating, updating, or deleting a Layer2Stretch configuration.
    - If the operation is create or update and C(wait) is true, it will return the Layer2Stretch details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "connection_type": "VPN",
      "description": "Layer2Stretch created by Ansible",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "high_availability_status": null,
      "links": null,
      "local_site_params": {
        "connection_reference": "a4f3f04f-1222-8544-7896-28b62bcc3e3e",
        "default_gateway_ip_address": null,
        "high_availability_group": null,
        "pc_cluster_reference": "18553f0f-7ce0-4c33-a697-0eecfb27fc10",
        "stretch_interface_ip_address": null,
        "stretch_subnet_reference": "b0cce620-3654-8522-9876-a91e2c037862",
        "vpn_interface_ip_address": null
      },
      "metadata": null,
      "mtu": 1500,
      "name": "layer2_stretch_ansible",
      "remote_site_params": {
        "connection_reference": "e7f3f04f-2222-3333-4444-28b62bcc3e3f",
        "default_gateway_ip_address": null,
        "high_availability_group": null,
        "pc_cluster_reference": "78e0d3ac-9e08-4d0c-8f1c-3d90ac2a55f0",
        "stretch_interface_ip_address": null,
        "stretch_subnet_reference": "b7c94b93-2222-3333-4444-91e2c0378621",
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
    - The external ID of the Layer2Stretch configuration.
  returned: always
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

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
  sample: "Api Exception raised while creating Layer2Stretch"
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
from ..module_utils.v4.network.helpers import (  # noqa: E402
    get_layer2_stretch,
    get_layer2_stretch_by_name,
)
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

    peered_gateway_spec = dict(
        ext_id=dict(type="str", required=False),
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


def check_layer2_stretch_idempotency(module, api_instance):
    """
    Idempotency helper for create: if a Layer2Stretch with the same name
    already exists, return its ext_id so the caller can skip creation.
    """
    name = module.params.get("name")
    if not name:
        return None
    existing = get_layer2_stretch_by_name(module, api_instance, name)
    if existing is None:
        return None
    return getattr(existing, "ext_id", None)


def create_Layer2Stretch(module, result, api_instance):
    validate_required_params(
        module,
        ["name", "connection_type", "local_site_params", "remote_site_params"],
    )

    existing_ext_id = check_layer2_stretch_idempotency(module, api_instance)
    if existing_ext_id:
        result["ext_id"] = existing_ext_id
        result["skipped"] = True
        result["changed"] = False
        result["msg"] = (
            "Layer2Stretch with name '{0}' already exists. "
            "Skipping creation.".format(module.params.get("name"))
        )
        return

    sg = SpecGenerator(module)
    default_spec = networking_sdk.Layer2Stretch()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create Layer2Stretch spec", **result)

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
            msg="Api Exception raised while creating Layer2Stretch",
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
                    "Failed to get entity ext_id from task for Layer2Stretch"
                ),
                msg="Failed to get entity ext_id from task for Layer2Stretch",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """
    Compare stripped old vs update specs to decide whether the update is a no-op.
    Read-only runtime fields (status, high-availability status, links) are
    dropped from both sides so they cannot spuriously trigger a change.
    """
    read_only_keys = [
        "stretch_status",
        "remote_stretch_status",
        "high_availability_status",
        "links",
        "metadata",
        "tenant_id",
    ]
    old_copy = strip_internal_attributes(deepcopy(old_spec_dict))
    new_copy = strip_internal_attributes(deepcopy(update_spec_dict))
    for key in read_only_keys:
        old_copy.pop(key, None)
        new_copy.pop(key, None)
    return old_copy == new_copy


def _remove_read_only_attributes(spec):
    """Remove server populated read-only fields before update API call."""
    for field in (
        "stretch_status",
        "remote_stretch_status",
        "high_availability_status",
        "links",
        "tenant_id",
    ):
        if hasattr(spec, field):
            setattr(spec, field, None)


def update_Layer2Stretch(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_layer2_stretch(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating Layer2Stretch", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update Layer2Stretch spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    _remove_read_only_attributes(update_spec)

    resp = None
    try:
        resp = api_instance.update_layer2_stretch_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Layer2Stretch",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_layer2_stretch(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_Layer2Stretch(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Layer2Stretch with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_layer2_stretch_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Layer2Stretch",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
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
    api_instance = get_layer2_stretches_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_Layer2Stretch(module, result, api_instance)
        else:
            create_Layer2Stretch(module, result, api_instance)
    else:
        delete_Layer2Stretch(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
