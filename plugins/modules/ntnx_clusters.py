#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters
short_description: cluster module which supports updating the configuration on an existing cluster
version_added: 1.0.0
description:
    - cluster module which supports updating the configuration on an existing cluster
options:
    cluster:
        description:
        - either cluster name or uuid in which the config will apply to
        type: dict
        suboptions:
            name:
                type: str
                description:
                - Cluster name
                - Mutually exclusive with C(uuid)
            uuid:
                type: str
                description:
                - Cluster uuid
                - Mutually exclusive with C(name)
    authorized_public_key_list:
        type: list
        description:
        - list of public key entries
        elements: dict
        suboptions:
            name:
                type: str
                description:
                - name of public key
            key:
                type: str
                description:
                - public key
    timezone:
        type: str
        description:
        - timezone of the cluster
    supported_information_verbosity:
        type: str
        description:
        - verbosity level of the cluster support logging
    redundancy_factor:
        type: int
        description:
        - redundancy factor of the cluster
    network:
        description:
        - all configuration in the cluster that's network related
        type: dict
        suboptions:
            external_ip:
                type: str
                description:
                - the local IP of the cluster visible externally
            fully_qualified_domain_name:
                type: str
                description:
                - fully qualified domain name of the cluster visible externally
            external_data_services_ip:
                type: str
                description:
                - The cluster IP address that provides external entities access to various cluster data services
            external_subnet:
                type: str
                description:
                - external subnet for cross server communication.  format is IP/netmask
            internal_subnet:
                type: str
                description:
                - The internal subnet is local to every server
                    its not visible outside.iSCSI requests generated internally within
                    the appliance (by user VMs or VMFS) are sent to the internal subnet.
                    The format is IP/netmask
            masquerading_ip:
                type: str
                description:
                - The cluster NAT'd or proxy IP which maps to the cluster local IP
            masquerading_port:
                type: str
                description:
                - Port used together with masquerading_ip to connect to the cluster
            domain_server:
                description:
                - Cluster domain server.  Only applied to the cluster with all Hyper-V hosts.
                type: dict
                suboptions:
                    name:
                        type: str
                        description:
                        - joined domain name. Empty name will unjoin the cluster from current domain
                    nameserver:
                        type: str
                        description:
                        - ip of the nameserver that can resolve the domain name.
                    domain_credentials:
                        description:
                        - domain creds for the domain server authentication
                        type: dict
                        suboptions:
                            username:
                                type: str
                                description:
                                - username
                            password:
                                type: str
                                description:
                                - password
            nfs_subnet_whitelist:
                type: list
                description:
                - Comma separated list of subnets (of the form 'a.b.c.d/l.m.n.o') that
                    are allowed to send NFS requests to this container. If not specified, the global
                    NFS whitelist will be looked up for access permission. The internal subnet is always
                    automatically considered part of the whitelist, even if the field below does not
                    explicitly specify it. Similarly, all the hypervisor IPs are considered part of the
                    whitelist. Finally, to permit debugging, all of the SVMs local IPs are considered to be
                    implicitly part of the whitelist.
            name_server_ip_list:
                type: list
                description:
                - list of IP addresses of the name servers.
            ntp_server_ip_list:
                type: list
                description:
                - list of the IP addresses or the FQDNs of the NTP servers.
            http_proxy_list:
                description:
                - list of http proxy entries
                type: list
                suboptions:
                    name:
                        type: str
                        description:
                        - name of the network entity (optional)
                    address:
                        type: dict
                        description:
                        - address details for http proxy
                        suboptions:
                            ip:
                                type: str
                                description:
                                - ipv4 address
                            ivp6:
                                type: str
                                description:
                                - ipv6 address
                            fqdn:
                                type: str
                                description:
                                - fully qualified domain name
                            port:
                                type: int
                                description:
                                - port number
                            is_backup:
                                type: bool
                                description:
                                - whether this address is a backup or not
                    credentials:
                        type: dict
                        description:
                        - creds for the proxy
                        suboptions:
                            username:
                                type: str
                                description:
                                - username
                            password:
                                type: str
                                description:
                                - password
                    proxy_type_list:
                        type: list
                        description:
                        - none provided in API spec
            smtp_server:
                description:
                - smtp server definition
                type: dict
                suboptions:
                    email_address:
                        type: str
                        description:
                        - email address
                    server:
                        description:
                        - server details for the smtp server
                        type: dict
                        suboptions:
                            name:
                                type: str
                                description:
                                - name of the network entity (optional)
                            address:
                                type: dict
                                description:
                                - address details for the network entity
                                suboptions:
                                    ip:
                                        type: str
                                        description:
                                        - ipv4 address
                                    ipv6:
                                        type: str
                                        description:
                                        - ipv6 address
                                    fqdn:
                                        type: str
                                        description:
                                        - fully qualified domain name
                                    port:
                                        type: int
                                        description:
                                        - port number
                                    is_backup:
                                        type: bool
                                        description:
                                        - whether this address is a backup or not
                            credentials:
                                description:
                                - credential details for smtp server
                                type: dict
                                suboptions:
                                    username:
                                        type: str
                                        description:
                                        - username
                                    password:
                                        type: str
                                        description:
                                        - password
                            proxy_type_list:
                                type: list
                                description:
                                - none provided in API spec
                    type:
                        type: str
                        description:
                        - type of smtp server, defaults to PLAIN.
            http_proxy_whitelist:
                description:
                - http proxy whitelist configuration
                type: list
                elements: dict
                suboptions:
                    target:
                        type: str
                        description:
                        - The target's identifier (as specified by the target_type). For eg  10.1.1.1
                    target_type:
                        type: str
                        description:
                        - either "IPv4_ADDRESS" or "HOST_NAME"
            default_vswitch_config:
                description:
                - default vswitch configuration
                type: dict
                suboptions:
                    nic_teaming_policy:
                        type: str
                        description:
                        - nice teaming policy
                    uplink_grouping:
                        type: str
                        description:
                        - determines how the ethernet uplinks are selected for this vswitch

extends_documentation_fragment:
- nutanix.ncp.ntnx_credentials
- nutanix.ncp.ntnx_operations
author:
- Thomas Tomlinson (@thomas-tomlinson)
"""

EXAMPLES = r"""

- name: ensure public ssh keys are present
  nutanix.ncp.ntnx_clusters:
    validate_certs: False
    state: present
    nutanix_host: nutanix_host
    nutanix_username: nutanix_user
    nutanix_password: nutanix_password
    cluster:
        name: cluster_name
    authorized_public_key_list:
        - name: user_1
          key: ssh-rsa REALLY_LONG_KEY_TEXT
        - name: user_2
          key: ssh-rsa REALLY_LONG_KEY_TEXT

"""

RETURN = r"""
response:
    description:
    - The full API response from the cluster PUT call.
    returned: always
    type: dict
    sample:  {
        "api_version": "3.1",
            "metadata": {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "2022-05-27T15:31:23Z",
                "kind": "cluster",
                "last_update_time": "2022-06-02T19:15:48Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_version": 51,
                "uuid": "0005dec1-a7d4-a09e-3740-2cea7f9c9e08"
            },
            "spec": {
                "name": "cluster_name",
                "resources": {
                    "config": {
                        "authorized_public_key_list": []
                    }
                }
            }
        }
"""


from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.clusters import Cluster  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    domain_server_spec = dict(
        name=dict(type="str"),
        nameserver=dict(type="str"),
        domain_credentials=dict(username=dict(type="str", password=dict(type="str"))),
    )

    http_proxy_list_spec = dict(
        name=dict(type="str"),
        address=dict(
            ip=dict(type="str"),
            ipv6=dict(type="str"),
            fqdn=dict(type="str"),
            port=dict(type="int"),
            is_backup=dict(type="bool"),
        )
    )

    smtp_server_spec = dict(
        email_address=dict(type="str"),
        server=dict(
            name=dict(type="str"),
            address=dict(
                ip=dict(type="str"),
                ipv6=dict(type="str"),
                fqdn=dict(type="str"),
                port=dict(type="int"),
                is_backup=dict(type="bool"),
            ),
            credentials=dict(
                username=dict(type="str"),
                password=dict(type="str"),
            ),
            type=dict(type="str"),
        )
    )

    http_proxy_whitelist_spec = dict(
        target=dict(type="str"),
        target_type=dict(type="str"),
    )

    default_vswitch_config_spec = dict(
        nic_teaming_policy=dict(type="str"),
        uplink_grouping=dict(type="str"),
    )

    network_spec = dict(
        external_ip=dict(type="str"),
        fully_qualified_domain_name=dict(type="str"),
        external_data_services_ip=dict(type="str"),
        external_subnet=dict(type="str"),
        internal_subnet=dict(type="str"),
        masquerading_ip=dict(type="str"),
        masquerading_port=dict(type="str"),
        domain_server=dict(type="dict", options=domain_server_spec),
        nfs_subnet_whitelist=dict(type="list"),
        name_server_ip_list=dict(type="list"),
        ntp_server_ip_list=dict(type="list"),
        http_proxy_list=dict(type="list", options=http_proxy_list_spec),
        smtp_server=dict(type="dict", options=smtp_server_spec),
        http_proxy_whitelist=dict(type="list", options=http_proxy_whitelist_spec),
        default_vswitch_config=dict(type="dict", options=default_vswitch_config_spec),
    )
    authorized_public_key_list_spec = dict(
        name=dict(type="str"),
        key=dict(type="str"),
    )

    module_args = dict(
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive, required=True,
        ),
        authorized_public_key_list=dict(type="list", options=authorized_public_key_list_spec),
        timezone=dict(type="str"),
        supported_information_verbosity=dict(type="str"),
        redundancy_factor=dict(type="int"),
        network=dict(type="dict", options=network_spec),
    )

    return module_args


def update_cluster_config(module, result):
    cluster = Cluster(module)
    old_spec = cluster.get_current_spec()
    spec, error = cluster.get_spec(old_spec)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating cluster Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return
    uuid = spec["metadata"]["uuid"]
    resp = cluster.update(spec, uuid)
    # compare the specs before and after.  currently only way to determine if something changed
    if old_spec['spec'] != resp['spec']:
        result["changed"] = True
    else:
        result["changed"] = False

    result["response"] = resp
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = cluster.read(uuid)
        result["response"] = resp


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        update_cluster_config(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
