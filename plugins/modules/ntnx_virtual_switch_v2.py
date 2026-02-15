#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_virtual_switch_v2
short_description: Create, Update, Delete virtual switches in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update, and delete virtual switches in Nutanix Prism Central.
  - It also supports creating a virtual switch from an existing bridge using the migrate operation.
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - if C(state) is present, it will create or update the virtual switch.
      - If C(state) is set to C(present) and ext_id is not provided then the operation will be create virtual switch.
      - If C(state) is set to C(present) and ext_id is provided then the operation will be update virtual switch.
      - If C(state) is set to C(absent) and ext_id is provided then the operation will be delete virtual switch.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the virtual switch. Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - User-visible Virtual Switch name.
      - Required for create operation.
      - Maximum 128 characters.
    type: str
    required: false
  description:
    description:
      - Description of the virtual switch.
      - Maximum 1000 characters.
    type: str
    required: false
  existing_bridge_name:
    description:
      - Name of an existing bridge to migrate/convert to a Virtual Switch.
      - When provided, the module will use the migrate API instead of creating a new virtual switch.
      - Maximum 128 characters.
    type: str
    required: false
  cluster_reference:
    description:
      - Prism Element cluster reference UUID for migrate operation.
      - Used only when existing_bridge_name is provided.
    type: str
    required: false
  bond_mode:
    description:
      - Bond mode type for the virtual switch.
      - Required for create operation (when not using existing_bridge_name).
    type: str
    choices:
      - NONE
      - ACTIVE_BACKUP
      - BALANCE_SLB
      - BALANCE_TCP
    required: false
  mtu:
    description:
      - MTU value for the virtual switch.
    type: int
    required: false
    default: 1500
  is_default:
    description:
      - Indicates whether it is a default Virtual Switch which cannot be deleted.
    type: bool
    required: false
    default: false
  is_quick_mode:
    description:
      - When true, the node is not put in maintenance mode during the Virtual Switch update operation.
      - This may briefly interrupt cluster workloads.
    type: bool
    required: false
    default: false
  clusters:
    description:
      - List of cluster configurations for the virtual switch.
      - Required for create operation (when not using existing_bridge_name).
    type: list
    elements: dict
    suboptions:
      ext_id:
        description:
          - Reference ExtId for the cluster.
        type: str
        required: true
      hosts:
        description:
          - Host configuration array.
        type: list
        elements: dict
        required: true
        suboptions:
          ext_id:
            description:
              - Reference ExtId for the host.
            type: str
            required: true
          host_nics:
            description:
              - List of host NIC names to use for the virtual switch.
            type: list
            elements: str
            required: false
          ip_address:
            description:
              - IP address configuration for the host.
            type: dict
            required: false
            suboptions:
              ip:
                description:
                  - IPv4 address specification.
                type: dict
                required: true
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
                    default: 32
              prefix_length:
                description:
                  - Prefix length of the IPv4 subnet.
                type: int
                required: true
          active_uplink:
            description:
              - Host active uplink interface.
            type: str
            required: false
      gateway_ip_address:
        description:
          - Gateway IP address for the cluster.
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
              - Prefix length of the network (0-32).
            type: int
            required: false
            default: 32
      vlan_identifier:
        description:
          - VLAN Identifier for this virtual switch cluster.
          - Set to 0 to remove VLAN tagging.
        type: int
    required: false
  igmp_spec:
    description:
      - IGMP specification for the virtual switch.
    type: dict
    required: false
    suboptions:
      is_snooping_enabled:
        description:
          - Enable IGMP snooping on this Virtual Switch.
        type: bool
        required: false
        default: false
      querier_spec:
        description:
          - Querier configuration for the virtual switch.
        type: dict
        required: false
        suboptions:
          is_querier_enabled:
            description:
              - Enable IGMP querier on this Virtual Switch.
            type: bool
            required: false
            default: false
          vlan_id_list:
            description:
              - VLAN Id list on which IGMP queries must be sent.
            type: list
            elements: int
            required: false
      snooping_timeout:
        description:
          - IGMP Snooping timeout value in seconds.
        type: int
        required: false
        default: 300
  metadata:
    description:
      - Metadata associated with the virtual switch resource.
    type: dict
    required: false
    suboptions:
      owner_reference_id:
        description:
          - A globally unique identifier that represents the owner of this resource.
        type: str
        required: false
      owner_user_name:
        description:
          - The userName of the owner of this resource.
          - Maximum 128 characters.
        type: str
        required: false
      project_reference_id:
        description:
          - A globally unique identifier that represents the project this resource belongs to.
        type: str
        required: false
      project_name:
        description:
          - The name of the project this resource belongs to.
          - Maximum 128 characters.
        type: str
        required: false
      category_ids:
        description:
          - A list of globally unique identifiers that represent all the categories the resource is associated with.
        type: list
        elements: str
        required: false
  wait:
    description: Wait for the operation to complete.
    type: bool
    required: false
    default: true

extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create virtual switch
  nutanix.ncp.ntnx_virtual_switch_v2:
    state: present
    name: "virtual_switch_ansible"
    description: "Virtual switch created by Ansible"
    bond_mode: "NONE"
    mtu: 1500
    is_default: false
    clusters:
      - ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
        hosts:
          - ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
        vlan_identifier: 0
    igmp_spec:
      is_snooping_enabled: false
  register: result
  ignore_errors: true

- name: Create a virtual switch from an existing bridge
  nutanix.ncp.ntnx_virtual_switch_v2:
    name: "virtual_switch_ansible_existing"
    description: "Virtual switch created from existing bridge"
    existing_bridge_name: "br2"
    cluster_reference: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: Update virtual switch
  nutanix.ncp.ntnx_virtual_switch_v2:
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "virtual_switch_ansible_updated"
    description: "Updated virtual switch description"
    bond_mode: "NONE"
    mtu: 1500
    is_default: false
    clusters:
      - ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
        hosts:
          - ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
        vlan_identifier: 0
    igmp_spec:
      is_snooping_enabled: true
      snooping_timeout: 600
      querier_spec:
        is_querier_enabled: true
  register: result
  ignore_errors: true

- name: Delete virtual switch
  nutanix.ncp.ntnx_virtual_switch_v2:
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting virtual switch
    - If the operation is create or update and C(wait) is true, it will return the virtual switch details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
      "bond_mode": "NONE",
      "clusters": [
          {
              "ext_id": "000647b8-ddb3-6bbb-0000-000000028f57",
              "gateway_ip_address": null,
              "hosts": [
                  {
                      "active_uplink": null,
                      "ext_id": "f28e7475-f835-42ef-ac35-ecbc48d5421e",
                      "host_nics": null,
                      "internal_bridge_name": "br1",
                      "ip_address": null,
                      "route_table": 1001
                  }
              ],
              "vlan_identifier": 0
          }
      ],
      "description": "Virtual switch created by Ansible",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "has_delete_in_progress": null,
      "has_deployment_error": null,
      "has_update_in_progress": null,
      "igmp_spec": {
          "is_snooping_enabled": false,
          "querier_spec": null,
          "snooping_timeout": 300
      },
      "is_default": false,
      "is_quick_mode": null,
      "links": null,
      "metadata": null,
      "mtu": 1500,
      "name": "virtual_switch_ansible",
      "owner_type": "PE",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external id of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external id of the virtual switch.
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

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_bridges_api_instance,
    get_etag,
    get_virtual_switches_api_instance,
)
from ..module_utils.v4.network.helpers import get_virtual_switch  # noqa: E402
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

    ipv4_subnet_spec = dict(
        ip=dict(
            type="dict",
            options=ipv4_address_spec,
            required=True,
            obj=networking_sdk.IPv4Address,
        ),
        prefix_length=dict(type="int", required=True),
    )

    host_spec = dict(
        ext_id=dict(type="str", required=True),
        host_nics=dict(type="list", elements="str", required=False),
        ip_address=dict(
            type="dict",
            options=ipv4_subnet_spec,
            required=False,
            obj=networking_sdk.IPv4Subnet,
        ),
        active_uplink=dict(type="str", required=False),
    )

    cluster_spec = dict(
        ext_id=dict(type="str", required=True),
        hosts=dict(
            type="list",
            elements="dict",
            options=host_spec,
            required=True,
            obj=networking_sdk.Host,
        ),
        gateway_ip_address=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=networking_sdk.IPv4Address,
        ),
        vlan_identifier=dict(type="int", required=False),
    )

    querier_spec = dict(
        is_querier_enabled=dict(type="bool", required=False, default=False),
        vlan_id_list=dict(type="list", elements="int", required=False),
    )

    igmp_spec = dict(
        is_snooping_enabled=dict(type="bool", required=False, default=False),
        querier_spec=dict(
            type="dict",
            options=querier_spec,
            required=False,
            obj=networking_sdk.QuerierSpec,
        ),
        snooping_timeout=dict(type="int", required=False, default=300),
    )

    metadata_spec = dict(
        owner_reference_id=dict(type="str", required=False),
        owner_user_name=dict(type="str", required=False),
        project_reference_id=dict(type="str", required=False),
        project_name=dict(type="str", required=False),
        category_ids=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        existing_bridge_name=dict(type="str"),
        cluster_reference=dict(type="str"),
        bond_mode=dict(
            type="str",
            choices=["NONE", "ACTIVE_BACKUP", "BALANCE_SLB", "BALANCE_TCP"],
            obj=networking_sdk.BondModeType,
        ),
        mtu=dict(type="int", default=1500),
        is_default=dict(type="bool", default=False),
        is_quick_mode=dict(type="bool", default=False),
        clusters=dict(
            type="list",
            elements="dict",
            options=cluster_spec,
            obj=networking_sdk.Cluster,
        ),
        igmp_spec=dict(
            type="dict",
            options=igmp_spec,
            obj=networking_sdk.IgmpSpec,
        ),
        metadata=dict(
            type="dict",
            options=metadata_spec,
            obj=networking_sdk.Metadata,
        ),
    )
    return module_args


def create_virtual_switch_from_bridge(module, bridges_api, result):
    sg = SpecGenerator(module)
    default_spec = networking_sdk.Bridge()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create virtual switch from bridge Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = bridges_api.migrate_bridge(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating virtual switch from bridge",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.VIRTUAL_SWITCH
        )
        if ext_id:
            result["ext_id"] = ext_id
            virtual_switches_api = get_virtual_switches_api_instance(module)
            resp = get_virtual_switch(module, virtual_switches_api, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def create_virtual_switch(module, virtual_switches, result):
    validate_required_params(module, ["bond_mode", "clusters"])
    sg = SpecGenerator(module)
    default_spec = networking_sdk.VirtualSwitch()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create virtual switch Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = virtual_switches.create_virtual_switch(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating virtual switch",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.VIRTUAL_SWITCH
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_virtual_switch(module, virtual_switches, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    clusters_old = old_spec_dict.get("clusters", [])
    clusters_update = update_spec_dict.get("clusters", [])
    if len(clusters_old) != len(clusters_update):
        return False
    for cluster_old, cluster_update in zip(clusters_old, clusters_update):
        hosts_old = cluster_old.get("hosts", [])
        hosts_update = cluster_update.get("hosts", [])
        if len(hosts_old) != len(hosts_update):
            return False
        for host_old, host_update in zip(hosts_old, hosts_update):
            host_old.pop("internal_bridge_name")
            host_update.pop("internal_bridge_name")
            host_old.pop("route_table")
            host_update.pop("route_table")
    old_spec_dict.pop("is_quick_mode")
    update_spec_dict.pop("is_quick_mode")
    old_spec_dict.pop("owner_type")
    update_spec_dict.pop("owner_type")
    return old_spec_dict == update_spec_dict


def update_virtual_switch(module, virtual_switches, result):
    ext_id = module.params.get("ext_id")

    result["ext_id"] = ext_id
    old_spec = get_virtual_switch(module, virtual_switches, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating virtual switch", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update virtual switch Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    # Remove read-only attributes before update API call
    update_spec.owner_type = None
    if update_spec.clusters:
        for cluster in update_spec.clusters:
            if cluster.hosts:
                for host in cluster.hosts:
                    host.internal_bridge_name = None
                    host.route_table = None

    resp = None

    try:
        resp = virtual_switches.update_virtual_switch_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating virtual switch",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_virtual_switch(module, virtual_switches, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_virtual_switch(module, virtual_switches, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Virtual switch with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = virtual_switches.delete_virtual_switch_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting virtual switch",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name",)),
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
        "error": None,
        "response": None,
        "ext_id": None,
    }
    virtual_switches = get_virtual_switches_api_instance(module)
    bridges_api = get_bridges_api_instance(module)
    state = module.params.get("state")

    if state == "absent":
        delete_virtual_switch(module, virtual_switches, result)
        module.exit_json(**result)

    if module.params.get("existing_bridge_name"):
        create_virtual_switch_from_bridge(module, bridges_api, result)
        module.exit_json(**result)

    if module.params.get("ext_id"):
        update_virtual_switch(module, virtual_switches, result)
        module.exit_json(**result)

    create_virtual_switch(module, virtual_switches, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
