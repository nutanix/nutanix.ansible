#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_karbon_registrys_info
short_description: registry  info module
version_added: 1.5.0
description: 'Get registry info'
options:
      registry_name:
        description:
            - registry name
        type: str
      fetch_ssh_credentials:
        type: bool
        description: write
      fetch_kubeconfig:
        type: bool
        description: write
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List registrys
    ntnx_karbon_registrys_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
    register: result

  - name: Get registrys using name
    ntnx_registrys_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      registry_name: "registry-name"
    register: result

  - name:  Get registrys with ssh credential
    ntnx_karbon_registrys_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      registry_name: "registry-name"
      fetch_ssh_credentials: true
    register: result

  - name:  Get registrys with kubeconfig
    ntnx_karbon_registrys_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      registry_name: "registry-name"
      fetch_kubeconfig: true
    register: result
"""
RETURN = r"""
cni_config:
  description: Container networking interface (CNI) information.
  returned: always
  type: dict
  sample:
    {
                "flannel_config": null,
                "node_cidr_mask_size": 24,
                "pod_ipv4_cidr": "172.20.0.0/16",
                "service_ipv4_cidr": "172.19.0.0/16"
            }
etcd_config:
  description: Etcd configuration information.
  returned: always
  type: dict
  sample: {
                "node_pools": [
                    "test-module21_etcd_pool"
                ]
            }
kubeapi_server_ipv4_address:
    description: IPV4 address of the API server.
    returned: always
    type: str
    sample: "10.44.78.171"
master_config:
    description: Configuration of master nodes.
    returned: always
    type: dict
    sample: {
                "deployment_type": "single-master",
                "node_pools": [
                    "test-module21_master_pool"
                ]
            }
name:
    description: K8s registry name.
    returned: always
    type: str
    sample: "test-module21"
status:
    description: K8s registry status.
    returned: always
    type: str
    sample: "kActive"
uuid:
    description: The universally unique identifier (UUID) of the k8s registry.
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
version:
    description: K8s version of the registry.
    returned: always
    type: str
    sample: "1.19.8-0"
worker_config:
    description: Worker configuration information.
    returned: always
    type: dict
    sample: {
                "node_pools": [
                    "test-module21_worker_pool"
                ]
            }
kube_config:
    description: write
    returned: if fetch_kubeconfig is true
    type: str
certificate:
    description: ssh certifcate
    returned: if fetch_ssh_credentials is true
    type: str
expiry_time:
    description: expire time for certificate
    returned: if fetch_ssh_credentials is true
    type: str
    sample: "2022-08-16T06:33:18.000Z"
private_key:
    description: user private key
    returned: if fetch_ssh_credentials is true
    type: str
username:
    description: name
    returned: if fetch_ssh_credentials is true
    type: str
    sample: admin
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.karbon.registries import Registry  # noqa: E402


def get_module_spec():

    module_args = dict(
        registry_name=dict(type="str"),
    )

    return module_args


def get_registry(module, result):
    registry = Registry(module)
    registry_name = module.params.get("registry_name")

    resp = registry.read(registry_name)

    result["response"] = resp


def get_registries(module, result):
    registry = Registry(module)

    resp = registry.read()

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
        mutually_exclusive=[("fetch_ssh_credentials", "fetch_kubeconfig")],
        required_if=[
            ("fetch_ssh_credentials", True, ("registry_name",)),
            ("fetch_kubeconfig", True, ("registry_name",)),
        ],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("registry_name"):
        get_registry(module, result)
    else:
        get_registries(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
