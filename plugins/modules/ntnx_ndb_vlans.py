#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_vlans
short_description: Module for create, update and delete of ndb vlan.
version_added: 1.8.0
description:
  - Module for create, update and delete of ndb vlans
  - Module for management ip pools in vlans
options:
  vlan_uuid:
    description:
      - uuid for update or delete of vlan
      - will be used to update if C(state) is C(present) and to delete if C(state) is C(absent)
    type: str
  name:
    description:
      - name of vlan
      - update allowed
    type: str
  vlan_type:
    description:
      - whether the vlan is managed or not
      - update allowed
    type: str
    choices: ["DHCP", "Static"]
  cluster:
        description:
          - Name or UUID of the cluster on which the vlan will be placed
        type: dict
        suboptions:
          name:
            description:
              - Cluster Name
              - Mutually exclusive with C(uuid)
            type: str
          uuid:
            description:
              - Cluster UUID
              - Mutually exclusive with C(name)
            type: str
  gateway:
    description:
      - The gateway ip address
      - update allowed
    type: str
  subnet_mask:
    description:
      - subnet mask
      - update allowed
    type: str
  primary_dns:
    description:
      - DNS servers IP
      - update allowed
    type: str
  secondary_dns:
    description:
      - DNS servers IP
      - update allowed
    type: str
  dns_domain:
    description:
      - The domain name
      - update allowed
    type: str
  ip_pools:
        description:
          - Range of IPs
          - update allowed
        type: list
        elements: dict
        suboptions:
            start_ip:
                description:
                - The start address of the IPs pool range
                type: str
            end_ip:
                description:
                - The end address of the IPs pool range
                type: str
  remove_ip_pools:
        description:
          - Range of IPs to remove
        type: list
        elements: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_ndb_base_module
  - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: create Dhcp ndb vlan
  ntnx_ndb_vlans:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    name: test-vlan-name
    vlan_type: DHCP
    cluster:
      uuid: "<cluster-uuid>"
  register: result

- name: create static ndb vlan
  ntnx_ndb_vlans:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    name: test-vlan-name
    vlan_type: Static
    cluster:
      uuid: "<cluster-uuid>"
    gateway: "<gateway>"
    subnet_mask: "<subnet_mask>"
    ip_pools:
      -
        start_ip: "<vlan_start_ip>"
        end_ip: "<vlan_end_ip>"
      -
        start_ip: "<vlan_start_ip>"
        end_ip: "<vlan_end_ip>"
    primary_dns: "<vlan_primary_dns>"
    secondary_dns: "<vlan_secondary_dns>"
    dns_domain: "<dns_domain_ip>"
  register: result

- name: update ndb vlan type
  ntnx_ndb_vlans:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    vlan_uuid: "<vlan-uuid>"
    vlan_type: DHCP
  register: result

- name: Delete vlan
  ntnx_ndb_vlans:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: absent
    vlan_uuid: "<vlan-uuid>"
  register: result
"""

RETURN = r"""
response:
  description: vlan creation response after provisioning
  returned: always
  type: dict
  sample: {}
vlan_uuid:
  description: created vlan UUID
  returned: always
  type: str
  sample: "00000-0000-000-0000-000000"
clusterId:
  description: Cluster ID
  returned: always
  type: str
  sample: "00000-0000-000-0000-000000"
name:
  description: vlan name
  returned: always
  type: str
  sample: "test-name"
type:
  description: vlan type Static or Dhcp
  returned: always
  type: str
  sample: "Static"
managed:
  description: mannaged or unmannged vlan
  returned: always
  type: bool

propertiesMap:
  description: confiuration of static vlan
  type: dict
  returned: always
  sample:
    {
                    "VLAN_DNS_DOMAIN": "0.0.0.0",
                    "VLAN_GATEWAY": "0.0.0.0",
                    "VLAN_PRIMARY_DNS": "0.0.0.0",
                    "VLAN_SECONDARY_DNS": "0.0.0.0",
                    "VLAN_SUBNET_MASK": "0.0.0.0",
                }
ipPools:
  description: Range of ip's
  type: list
  returned: always
  sample:
    [
                {
                    "endIP": "0.0.0.0",
                    "id": "000000-00000-000000-0000",
                    "ipAddresses": [
                        {
                            "ip": "0.0.0.0",
                            "status": "Available"
                        },
                        {
                            "ip": "0.0.0.0",
                            "status": "Available"
                        },
                        {
                            "ip": "0.0.0.0",
                            "status": "Available"
                        },
                    ],
                    "modifiedBy": "000000-00000-000000-0000",
                    "startIP": "0.0.0.0"
                }
                ]

properties:
  description: list of confiuration of static vlan
  type: list
  returned: always
  sample:
    [
                {
                    "name": "VLAN_DNS_DOMAIN",
                    "secure": false,
                    "value": "0.0.0.0"
                },
                {
                    "name": "VLAN_GATEWAY",
                    "secure": false,
                    "value": "0.0.0.0"
                },
                {
                    "name": "VLAN_PRIMARY_DNS",
                    "secure": false,
                    "value": "0.0.0.0"
                },
                {
                    "name": "VLAN_SECONDARY_DNS",
                    "secure": false,
                    "value": "0.0.0.0"
                },
                {
                    "name": "VLAN_SUBNET_MASK",
                    "secure": false,
                    "value": "0.0.0.0"
                }
            ]
"""
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.vlans import VLAN  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    ip_pool_spec = dict(start_ip=dict(type="str"), end_ip=dict(type="str"))

    module_args = dict(
        name=dict(type="str"),
        vlan_type=dict(type="str", choices=["DHCP", "Static"]),
        vlan_uuid=dict(type="str"),
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        ip_pools=dict(
            type="list",
            elements="dict",
            options=ip_pool_spec,
            required_by={"end_ip": "start_ip"},
        ),
        remove_ip_pools=dict(type="list", elements="str"),
        gateway=dict(type="str"),
        subnet_mask=dict(type="str"),
        primary_dns=dict(type="str"),
        secondary_dns=dict(type="str"),
        dns_domain=dict(type="str"),
    )
    return module_args


def create_vlan(module, result):
    vlan = VLAN(module)

    name = module.params.get("name")
    uuid, err = vlan.get_uuid(name)
    if uuid:
        module.fail_json(msg="vlan with given name already exists", **result)

    spec, err = vlan.get_spec(validate_module_params=True)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create vlan spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = vlan.create(data=spec)

    result["response"] = resp
    vlan_uuid = resp["id"]
    result["vlan_uuid"] = vlan_uuid
    result["changed"] = True


def update_vlan(module, result):
    vlan = VLAN(module)

    uuid = module.params.get("vlan_uuid")
    ip_pools = module.params.pop("ip_pools", None)
    remove_ip_pools = module.params.pop("remove_ip_pools", None)
    if not uuid:
        module.fail_json(msg="vlan_uuid is required field for update", **result)

    resp, err = vlan.get_vlan(uuid=uuid, detailed=False)

    old_spec = vlan.get_default_update_spec(override_spec=resp)

    update_spec, err = vlan.get_spec(old_spec=old_spec, validate_module_params=True)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update vlan spec", **result)

    if module.check_mode:
        result["response"] = update_spec
        return

    if check_for_idempotency(old_spec, update_spec):
        if not remove_ip_pools and not ip_pools:
            result["skipped"] = True
            module.exit_json(msg="Nothing to change.")
    else:
        vlan.update(data=update_spec, uuid=uuid)

    if remove_ip_pools:
        vlan.remove_ip_pools(vlan_uuid=uuid, ip_pools=remove_ip_pools)
    if ip_pools:
        resp, err = vlan.add_ip_pools(
            vlan_uuid=uuid, ip_pools=ip_pools, old_spec=old_spec
        )
        if err:
            result["warning"] = "IP pool is not added. Error: {0}".format(err)

    resp, err = vlan.get_vlan(uuid=uuid, detailed=True)

    result["response"] = resp
    result["vlan_uuid"] = uuid
    result["changed"] = True


def delete_vlan(module, result):
    vlan = VLAN(module)

    uuid = module.params.get("vlan_uuid")
    if not uuid:
        module.fail_json(msg="vlan_uuid is required field for delete", **result)

    resp = vlan.delete(uuid)

    result["response"] = resp
    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):

    for key, value in update_spec.items():
        if old_spec.get(key) != value:
            return False

    return True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        mutually_exclusive=[("vlan_uuid", "name")],
        required_if=[
            ("state", "present", ("name", "vlan_uuid"), True),
            ("state", "absent", ("vlan_uuid",)),
        ],
        required_by={"remove_ip_pools": "vlan_uuid"},
        required_one_of=[("vlan_uuid", "vlan_type")],
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "vlan_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("vlan_uuid"):
            update_vlan(module, result)
        else:
            create_vlan(module, result)
    else:
        delete_vlan(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
