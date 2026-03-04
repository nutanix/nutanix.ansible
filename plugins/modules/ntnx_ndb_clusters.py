#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_clusters
short_description: "Create, Update and Delete NDB clusters"
version_added: 1.8.0
description: "Create, Update and Delete NDB clusters"
options:
    name:
        type: str
        description:
         - Name of the cluster.
         - Update allowed.
    uuid:
        type: str
        description:
            - UUID of the cluster.
            - will be used to update if C(state) is C(present) and to delete if C(state) is C(absent)
    desc:
        type: str
        description:
            - Description of the cluster.
            - Update allowed.
    name_prefix:
        type: str
        description: Name prefix of the cluster.
    cluster_ip:
        type: str
        description:
         - IP address of cluster.
         - Update allowed.
    cluster_credentials:
        type: dict
        description:
         - Credentials of the cluster.
         - Update allowed.
        suboptions:
            username:
                type: str
                description: Cluster username
            password:
                type: str
                description: Cluster password
    agent_network:
        type: dict
        description: configure dns and ntp details.
        suboptions:
            dns_servers:
                type: list
                description: dns servers for clusters
                elements: str
            ntp_servers:
                type: list
                elements: str
                description: ntp servers for clusters
    vlan_access:
        type: dict
        description: VLAN access info for which you want to configure network segmentation
        suboptions:
            prism_vlan:
                type: dict
                description:
                    - VLAN access info to configure a VLAN that the NDB agent VM can use to communicate with Prism
                suboptions:
                    vlan_name:
                        type: str
                        description: Name of subnet
                    vlan_type:
                        type: str
                        description: type of subnet
                        choices: ["DHCP", "Static"]
                    static_ip:
                        type: str
                        description: ip address of subnet
                    gateway:
                        type: str
                        description: The gateway ip address
                    subnet_mask:
                        type: str
                        description: Subnet network address
            dsip_vlan:
                type: dict
                description: VLAN access info to configure a VLAN that the agent VM can use to make connection requests to the iSCSI data services IP.
                suboptions:
                    vlan_name:
                        type: str
                        description: Name of subnet
                    vlan_type:
                        type: str
                        description: Type of subnet
                        choices: ["DHCP", "Static"]
                    static_ip:
                        type: str
                        description: ip address of subnet
                    gateway:
                        type: str
                        description: The gateway ip address
                    subnet_mask:
                        type: str
                        description: Subnet network address
            dbserver_vlan:
                type: dict
                description:
                    - VLAN access info to configure a VLAN that is used for communications between
                      the NDB agent VM and the database server VM on the newly registered NDB server cluster.
                suboptions:
                    vlan_name:
                        type: str
                        description: Name of subnet
                    vlan_type:
                        type: str
                        description: Type of subnet
                        choices: ["DHCP", "Static"]
                    static_ip:
                        type: str
                        description: ip address of subnet
                    gateway:
                        type: str
                        description: The gateway ip address
                    subnet_mask:
                        type: str
                        description: Subnet network address
    storage_container:
        type: str
        description: Name of storage container.
extends_documentation_fragment:
      - nutanix.ncp.ntnx_operations
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_logger
author:
    - Prem Karat (@premkarat)
    - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
    - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Register Cluster with prism_vlan
  ntnx_ndb_clusters:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    name: "cluster_name"
    desc: "cluster_desc"
    name_prefix: "cluster_name_prefix"
    cluster_ip: "cluster_ip"
    cluster_credentials:
      username: "{{cluster_info.cluster_credentials.username}}"
      password: "{{cluster_info.cluster_credentials.password}}"
    agent_network:
      dns_servers:
        - "{{cluster_info.agent_network.dns_servers[0]}}"
        - "{{cluster_info.agent_network.dns_servers[1]}}"
      ntp_servers:
        - "{{cluster_info.agent_network.ntp_servers[0]}}"
        - "{{cluster_info.agent_network.ntp_servers[1]}}"
    vlan_access:
      prism_vlan:
        vlan_name: "{{cluster_info.vlan_access.prism_vlan.vlan_name}}"
        vlan_type: "{{cluster_info.vlan_access.prism_vlan.vlan_type}}"
        static_ip: "{{cluster_info.vlan_access.prism_vlan.static_ip}}"
        gateway: "{{cluster_info.vlan_access.prism_vlan.gateway}}"
        subnet_mask: "{{cluster_info.vlan_access.prism_vlan.subnet_mask}}"
    storage_container: "{{cluster_info.storage_container}}"

- name: update cluster name , desc
  ntnx_ndb_clusters:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "cluster_uuid"
    name: newname
    desc: newdesc

- name: delete cluster
  ntnx_ndb_clusters:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "cluster_uuid"
    state: absent
"""

RETURN = r"""
response:
  description: An intentful representation of a cluster status
  returned: always
  type: dict
  sample:
            {
                        "cloudInfo": null,
                        "cloudType": "NTNX",
                        "dateCreated": "2023-01-22 08:59:42.12768",
                        "dateModified": "2023-01-22 09:12:07.842244",
                        "description": "newdesc",
                        "entityCounts": null,
                        "fqdns": null,
                        "healthy": true,
                        "hypervisorType": "AHV",
                        "hypervisorVersion": "6.1",
                        "id": "0000-0000-000-00000-0000",
                        "ipAddresses": [
                            "10.46.33.223"
                        ],
                        "managementServerInfo": null,
                        "name": "newname",
                        "nxClusterUUID": "0000-0000-000-00000-0000",
                        "ownerId": "0000-0000-000-00000-0000",
                        "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                        "properties": [
                            {
                                "description": null,
                                "name": "CLUSTER_ID",
                                "ref_id": "0000-0000-000-00000-0000",
                                "secure": false,
                                "value": "0000-0000-000-00000-0000",
                            },
                            {
                                "description": null,
                                "name": "CLUSTER_INCARNATION_ID",
                                "ref_id": "0000-0000-000-00000-0000",
                                "secure": false,
                                "value": "1670238836188065"
                            },
                            {
                                "description": null,
                                "name": "ERA_STORAGE_CONTAINER",
                                "ref_id": "0000-0000-000-00000-0000",
                                "secure": false,
                                "value": "default-container-95673204421578"
                            },
                            {
                                "description": null,
                                "name": "MODEL_NAME",
                                "ref_id": "0000-0000-000-00000-0000",
                                "secure": false,
                                "value": "NX-1065-G5"
                            },
                            {
                                "description": null,
                                "name": "ONDEMAND_REPLICATION_SUPPORTED",
                                "ref_id": "0000-0000-000-00000-0000",
                                "secure": false,
                                "value": "true"
                            },
                            {
                                "description": null,
                                "name": "PRISM_VM_LIST_PAGINATION_LIMIT",
                                "ref_id": "0000-0000-000-00000-0000",
                                "secure": false,
                                "value": "500"
                            },
                            {
                                "description": null,
                                "name": "PRISM_VM_LIST_PAGINATION_SIZE",
                                "ref_id": "0000-0000-000-00000-0000",
                                "secure": false,
                                "value": "50"
                            },
                            {
                                "description": null,
                                "name": "RESOURCE_CONFIG",
                                "ref_id": "0000-0000-000-00000-0000",
                                "secure": false,
                                "value": "{\"storageThresholdPercentage\":95.0,\"memoryThresholdPercentage\":95.0}"
                            },
                            {
                                "description": null,
                                "name": "TIMEZONE",
                                "ref_id": "0000-0000-000-00000-0000",
                                "secure": false,
                                "value": "UTC"
                            }
                        ],
                        "referenceCount": 0,
                        "resourceConfig": {
                            "memoryThresholdPercentage": 95.0,
                            "storageThresholdPercentage": 95.0
                        },
                        "status": "UP",
                        "uniqueName": "NEWNAME",
                        "username": "admin",
                        "version": "v2",
            }
cluster_uuid:
  description: The created cluster uuid
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""

import time  # noqa: E402

from ..module_utils import utils  # noqa: E402
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.clusters import Cluster  # noqa: E402
from ..module_utils.v3.ndb.operations import Operation  # noqa: E402


def get_module_spec():

    credentials_spec = dict(
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )

    agent_network_spec = dict(
        dns_servers=dict(type="list", elements="str"),
        ntp_servers=dict(type="list", elements="str"),
    )

    vlan_access_spec = dict(
        vlan_name=dict(type="str"),
        vlan_type=dict(type="str", choices=["DHCP", "Static"]),
        static_ip=dict(type="str"),
        gateway=dict(type="str"),
        subnet_mask=dict(type="str"),
    )

    vlan_access_type_spec = dict(
        prism_vlan=dict(type="dict", options=vlan_access_spec),
        dsip_vlan=dict(type="dict", options=vlan_access_spec),
        dbserver_vlan=dict(type="dict", options=vlan_access_spec),
    )

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        desc=dict(type="str"),
        name_prefix=dict(type="str"),
        cluster_ip=dict(type="str"),
        cluster_credentials=dict(
            type="dict",
            required_together=[("username", "password")],
            options=credentials_spec,
        ),
        agent_network=dict(type="dict", options=agent_network_spec),
        vlan_access=dict(type="dict", options=vlan_access_type_spec),
        storage_container=dict(type="str"),
    )

    return module_args


def create_cluster(module, result):
    cluster = Cluster(module)
    cluster_ip = module.params.get("cluster_ip")

    spec, err = cluster.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create cluster spec", **result)

    if cluster.get_cluster_by_ip(cluster_ip):
        module.fail_json(
            msg="The provided cluster IP is already registered with NDB.", **result
        )

    if module.check_mode:
        result["response"] = spec
        return

    resp = cluster.create(spec)
    ops_uuid = resp["operationId"]

    cluster_name = module.params.get("name")
    cluster_uuid = cluster.get_uuid(key="name", value=cluster_name)

    if not cluster_uuid:
        result["error"] = err
        module.fail_json(msg="Failed getting cluster uuid", **result)

    result["cluster_uuid"] = cluster_uuid
    result["changed"] = True

    if module.params.get("wait"):
        operations = Operation(module)
        time.sleep(5)  # wait for ops to starts
        operations.wait_for_completion(ops_uuid)
        resp = cluster.read(cluster_uuid)

    result["response"] = resp


def update_cluster(module, result):
    cluster_uuid = module.params["uuid"]

    cluster = Cluster(module)

    resp = cluster.read(cluster_uuid)
    old_spec = cluster.get_default_update_spec(override_spec=resp)

    update_spec, err = cluster.get_spec(old_spec=old_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update cluster spec", **result)

    result["cluster_uuid"] = cluster_uuid

    if module.check_mode:
        result["response"] = update_spec
        return

    if check_for_idempotency(old_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = cluster.update(data=update_spec, uuid=cluster_uuid)
    result["changed"] = True

    result["response"] = resp


def delete_cluster(module, result):
    cluster_uuid = module.params["uuid"]

    cluster = Cluster(module)
    result["cluster_uuid"] = cluster_uuid

    if module.check_mode:
        result["msg"] = "Cluster with uuid:{0} will be deleted.".format(cluster_uuid)
        return

    resp, err = cluster.delete(cluster_uuid)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed removing cluster", **result)
    result["response"] = resp

    ops_uuid = resp["operationId"]

    if module.params.get("wait"):
        operations = Operation(module)
        time.sleep(2)  # to get operation ID functional
        resp = operations.wait_for_completion(ops_uuid, delay=5)
        result["response"] = resp
    result["changed"] = True
    result["cluster_uuid"] = cluster_uuid


def check_for_idempotency(old_spec, update_spec):
    if old_spec == update_spec:
        return True
    return False


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "uuid"), True),
            ("state", "present", ("cluster_ip", "uuid"), True),
            ("state", "present", ("cluster_credentials", "uuid"), True),
            ("state", "absent", ("uuid",)),
        ],
        mutually_exclusive=[
            ("uuid", "name_prefix"),
            ("uuid", "agent_network"),
            ("uuid", "vlan_access"),
            ("uuid", "storage_container"),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"response": {}, "error": None, "changed": False}
    state = module.params["state"]
    if state == "present":
        if module.params.get("uuid"):
            update_cluster(module, result)
        else:
            create_cluster(module, result)
    else:
        delete_cluster(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
