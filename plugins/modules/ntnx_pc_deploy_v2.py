#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_pc_deploy_v2
short_description: Deploys a Prism Central using the provided details
version_added: 2.1.0
description:
    - Deploys a Prism Central using the provided details
    - Prism Central Size, Network Config are mandatory fields to deploy Prism Central
    - If wait is set to true, the module will wait for the task to complete
    - Please provide Prism Element IP address here in C(nutanix_host)
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will deploy a Prism Central.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    wait:
        description: Wait for the operation to complete.
        type: bool
        required: false
        default: True
    config:
        description: Domain manager (Prism Central) cluster configuration details.
        type: dict
        required: true
        suboptions:
            should_enable_lockdown_mode:
                description: A boolean value indicating whether to enable lockdown mode for a cluster.
                type: bool
                required: false
            build_info:
                description: Currently representing the build information to be used for the cluster creation.
                type: dict
                required: true
                suboptions:
                    version:
                        description: Software version.
                        type: str
                        required: false
            name:
                description: Name of the domain manager (Prism Central).
                type: str
                required: true
            size:
                description: Domain manager (Prism Central) size is an enumeration of starter, small, large, or extra large starter values.
                type: str
                required: true
                choices:
                    - SMALL
                    - LARGE
                    - EXTRALARGE
                    - STARTER
            resource_config:
                description:
                    - This configuration is used to provide the resource-related details like container external identifiers, number of VCPUs, memory size,
                        data disk size of the domain manager (Prism Central).
                    - In the case of a multi-node setup, the sum of resources like number of VCPUs, memory size and data disk size are provided.
                type: dict
                required: false
                suboptions:
                    container_ext_ids:
                        description: The external identifier of the container that will be used to create the domain manager (Prism Central) cluster.
                        type: list
                        required: false
                        elements: str
                    data_disk_size_bytes:
                        description: The size of the data disk in bytes.
                        type: int
                        required: false
                    memory_size_bytes:
                        description: The size of the memory in bytes.
                        type: int
                        required: false
                    num_vcpus:
                        description: The number of virtual CPUs.
                        type: int
                        required: false
    network:
        description: Domain manager (Prism Central) network configuration details.
        type: dict
        required: true
        suboptions:
            external_address:
                description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                type: dict
                required: false
                suboptions:
                    ipv4:
                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description: The IPv4 address of the host.
                                type: str
                                required: true
                            prefix_length:
                                description: The prefix length of the network to which this host IPv4 address belongs.
                                type: int
                                required: false
                                default: 32
                    ipv6:
                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description: The IPv6 address of the host.
                                type: str
                                required: true
                            prefix_length:
                                description: The prefix length of the network to which this host IPv6 address belongs.
                                type: int
                                required: false
                                default: 128
            name_servers:
                description:
                    - List of name servers on a cluster.
                    - For create operation, only ipv4 address / fqdn values are supported currently.
                type: list
                required: true
                elements: dict
                suboptions:
                    ipv4:
                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description: The IPv4 address of the host.
                                type: str
                                required: true
                            prefix_length:
                                description: The prefix length of the network to which this host IPv4 address belongs.
                                type: int
                                required: false
                                default: 32
                    ipv6:
                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description: The IPv6 address of the host.
                                type: str
                                required: true
                            prefix_length:
                                description: The prefix length of the network to which this host IPv6 address belongs.
                                type: int
                                required: false
                                default: 128
                    fqdn:
                        description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description: Fully Qualified Domain Name of the Host.
                                type: str
                                required: false
            ntp_servers:
                description:
                    - List of NTP servers on a cluster
                    - For create operation, only ipv4 address / fqdn values are supported currently.
                type: list
                required: true
                elements: dict
                suboptions:
                    ipv4:
                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description: The IPv4 address of the host.
                                type: str
                                required: true
                            prefix_length:
                                description: The prefix length of the network to which this host IPv4 address belongs.
                                type: int
                                required: false
                                default: 32
                    ipv6:
                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description: The IPv6 address of the host.
                                type: str
                                required: true
                            prefix_length:
                                description: The prefix length of the network to which this host IPv6 address belongs.
                                type: int
                                required: false
                                default: 128
                    fqdn:
                        description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description: Fully Qualified Domain Name of the Host.
                                type: str
                                required: false
            internal_networks:
                description: This configuration is used to internally manage Prism Central network.
                type: list
                elements: dict
                required: false
                suboptions:
                    default_gateway:
                        description:
                            - The default gateway of the network.
                            - An unique address that identifies a device on the internet or a local network in
                                IPv4/IPv6 format or a Fully Qualified Domain Name.
                        type: dict
                        required: true
                        suboptions:
                            ipv4:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv4 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                            ipv6:
                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv6 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                            fqdn:
                                description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: Fully Qualified Domain Name of the Host.
                                        type: str
                                        required: false
                    subnet_mask:
                        description:
                            - The subnet mask of the network.
                            - An unique address that identifies a device on the internet or a local network in
                                IPv4/IPv6 format or a Fully Qualified Domain Name.
                        type: dict
                        required: true
                        suboptions:
                            ipv4:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv4 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                            ipv6:
                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv6 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                            fqdn:
                                description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: Fully Qualified Domain Name of the Host.
                                        type: str
                                        required: false
                    ip_ranges:
                        description: Range of IPs used for Prism Central network setup.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                            begin:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    ipv4:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv4 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv4 address belongs.
                                                type: int
                                                required: false
                                                default: 32
                                    ipv6:
                                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv6 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv6 address belongs.
                                                type: int
                                                required: false
                                                default: 128
                            end:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    ipv4:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv4 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv4 address belongs.
                                                type: int
                                                required: false
                                                default: 32
                                    ipv6:
                                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv6 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv6 address belongs.
                                                type: int
                                                required: false
                                                default: 128
            external_networks:
                description: This configuration is used to manage Prism Central.
                type: list
                elements: dict
                required: true
                suboptions:
                    default_gateway:
                        description:
                            - The default gateway of the network.
                            - An unique address that identifies a device on the internet or a local network in
                                IPv4/IPv6 format or a Fully Qualified Domain Name.
                        type: dict
                        required: true
                        suboptions:
                            ipv4:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv4 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                            ipv6:
                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv6 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                            fqdn:
                                description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: Fully Qualified Domain Name of the Host.
                                        type: str
                                        required: false
                    subnet_mask:
                        description:
                            - The subnet mask of the network.
                            - An unique address that identifies a device on the internet or a local network in
                                IPv4/IPv6 format or a Fully Qualified Domain Name.
                        type: dict
                        required: true
                        suboptions:
                            ipv4:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv4 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                            ipv6:
                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv6 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                            fqdn:
                                description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: Fully Qualified Domain Name of the Host.
                                        type: str
                                        required: false
                    ip_ranges:
                        description: Range of IPs used for Prism Central network setup.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                            begin:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    ipv4:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv4 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv4 address belongs.
                                                type: int
                                                required: false
                                                default: 32
                                    ipv6:
                                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv6 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv6 address belongs.
                                                type: int
                                                required: false
                                                default: 128
                            end:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    ipv4:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv4 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv4 address belongs.
                                                type: int
                                                required: false
                                                default: 32
                                    ipv6:
                                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv6 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv6 address belongs.
                                                type: int
                                                required: false
                                                default: 128
                    network_ext_id:
                        description: The network external identifier to which Domain Manager (Prism Central) is to be deployed or is already configured.
                        type: str
                        required: true
    should_enable_high_availability:
        description: This configuration enables Prism Central to be deployed in scale-out mode.
        type: bool
        required: false
        default: false
    nutanix_host:
        description: Nutanix Prism Element IP address.
        type: str
        required: true
    nutanix_username:
        description: The username to authenticate with the Nutanix Prism Element.
        type: str
        required: true
    nutanix_password:
        description: The password to authenticate with the Nutanix Prism Element.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Deploy PC
  nutanix.ncp.ntnx_pc_deploy_v2:
    nutanix_host: <pe_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    config:
      name: "pc_name"
      size: "STARTER"
      build_info:
        version: "pc.2024.3"
    network:
      external_networks:
        - default_gateway:
            ipv4:
              value: "10.0.0.1"
          subnet_mask:
            ipv4:
              value: "255.255.240.0"
          ip_ranges:
            - begin:
                ipv4:
                  value: "10.0.0.2"
              end:
                ipv4:
                  value: "10.0.0.3"
          network_ext_id: "4854f740-1234-9655-7458-942e66b4189e"
      name_servers:
        - ipv4:
            value: "10.0.0.4"
        - ipv4:
            value: "10.0.0.5"
      ntp_servers:
        - fqdn:
            value: "2.example.org"
        - fqdn:
            value: "3.example.org"
  register: result
"""

RETURN = r"""
response:
    description: Task response for deploy PC operation.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00062db6-57d1-7642-0000-00000000b71a"
            ],
            "completed_time": "2025-02-09T15:34:15.092891+00:00",
            "completion_details": null,
            "created_time": "2025-02-09T14:44:52.593544+00:00",
            "entities_affected": [
                {
                    "ext_id": "00062db6-57d1-7642-0000-00000000b71a",
                    "name": null,
                    "rel": "clustermgmt:config:cluster"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2025-02-09T15:34:15.092888+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 2,
            "operation": "kPrismCentralDeploymentRequest",
            "operation_description": "Download and deploy Prism Central",
            "owned_by": null,
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2025-02-09T14:44:52.602785+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:f9856c8f-d619-42d6-65b3-5651e8825a6c",
                    "href": "https://10.0.0.1:9440/api/prism/v4.0/config/tasks/ZXJnb24=:f9856c8f-d619-42d6-65b3-5651e8825a6c",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:fdd37a31-ab57-48fd-56dd-47358b910010",
                    "href": "https://10.0.0.1:9440/api/prism/v4.0/config/tasks/ZXJnb24=:fdd37a31-ab57-48fd-56dd-47358b910010",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }

task_ext_id:
    description: Task external ID for deploy PC operation.
    returned: always
    type: str
    sample: "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
)
from ..module_utils.v4.prism.spec.pc import PrismSpecs as prism_specs  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
    )
    module_args.update(prism_specs.get_prism_spec())
    return module_args


def deploy_pc(module, result):
    """
    This method will deploy prism central.
    Args:
        module (object): Ansible module object
        result (dict): Result object
    """
    sg = SpecGenerator(module)
    default_spec = prism_sdk.DomainManager()
    spec, err = sg.generate_spec(obj=default_spec)
    domain_manager_api = get_domain_manager_api_instance(module)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating deploy prism central spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = domain_manager_api.create_domain_manager(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deploying prism central",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    deploy_pc(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
