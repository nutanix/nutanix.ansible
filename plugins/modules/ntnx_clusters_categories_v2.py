#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_categories_v2
short_description: Manage Nutanix clusters categories in Prism Central
description:
  - This module allows you to associate or disassociate categories with a Nutanix cluster using Prism Central.
  - This module uses PC v4 APIs based SDKs
version_added: "2.4.0"
options:
    state:
        description:
            - The state of the category association.
            - If C(present), the module will associate the provided categories with the cluster.
            - If C(absent), the module will disassociate the provided categories from the cluster.
        type: str
        choices: [present, absent]
        default: present
    cluster_ext_id:
        description:
            - The external ID of the cluster on which categories will be associated or disassociated.
        type: str
        required: true
    categories:
        description:
            - List of categories to associate or disassociate with the cluster on which categories will be associated or disassociated.
        type: list
        elements: str
        required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Associate categories with cluster
  nutanix.ncp.ntnx_clusters_categories_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    categories:
      - "12n8p-2779-4b30-9156-521b0b6b3293"
      - "98j8p-5779-4b30-9156-521b0b6b3293"
    state: present
  register: result
  ignore_errors: true

- name: Disassociate categories from cluster
  nutanix.ncp.ntnx_clusters_categories_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    categories:
      - "12n8p-2779-4b30-9156-521b0b6b3293"
      - "98j8p-5779-4b30-9156-521b0b6b3293"
    state: absent
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - The response from the clusters categories API.
        - If C(wait) is true, response will be cluster details
        - If C(wait) is false, response will be task details
    type: dict
    returned: always
    sample:
        {
            "backup_eligibility_score": 1,
            "categories": [
                "f7c8a907-b7ec-409d-b626-3b69ac3a0e4e"
            ],
            "cluster_profile_ext_id": null,
            "config": {
                "authorized_public_key_list": [
                    {
                        "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDQ6",
                        "name": "cb48351c-ed6d-4791-930a-0d61bd0060bf"
                    },
                    {
                        "key": "ssh-rsa AAAAB3NzaC1yc2EAA= root@phoenix",
                        "name": "10.46.136.28"
                    },
                    {
                        "key": "ssh-rsa AAAAB3NzaC1yc2EAAAAQ== nutanix@titan",
                        "name": "agave"
                    },
                    {
                        "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6oD",
                        "name": "nutest"
                    }
                ],
                "build_info": {
                    "build_type": "release",
                    "commit_id": "403c2537de51674979c3b35300abff1a7566ac8a",
                    "full_version": "el8.5-release-ganges-7.3-stable-403c2537de51674979c3b35300abff1a7566ac8a",
                    "short_commit_id": "403c25",
                    "version": "7.3"
                },
                "cluster_arch": "X86_64",
                "cluster_function": [
                    "AOS"
                ],
                "cluster_software_map": [
                    {
                        "software_type": "NCC",
                        "version": "ncc-5.2.0"
                    },
                    {
                        "software_type": "NOS",
                        "version": "el8.5-release-ganges-7.3-stable-403c2537de51674979c3b35300abff1a7566ac8a"
                    }
                ],
                "encryption_in_transit_status": null,
                "encryption_option": null,
                "encryption_scope": null,
                "fault_tolerance_state": {
                    "current_cluster_fault_tolerance": "CFT_0N_AND_0D",
                    "current_max_fault_tolerance": 0,
                    "desired_cluster_fault_tolerance": "CFT_0N_AND_0D",
                    "desired_max_fault_tolerance": 0,
                    "domain_awareness_level": "DISK",
                    "redundancy_status": null
                },
                "hypervisor_types": [
                    "AHV"
                ],
                "incarnation_id": 1758177781920286,
                "is_available": true,
                "is_lts": false,
                "is_password_remote_login_enabled": true,
                "is_remote_support_enabled": false,
                "operation_mode": "NORMAL",
                "pulse_status": {
                    "is_enabled": true,
                    "pii_scrubbing_level": "DEFAULT"
                },
                "redundancy_factor": 1,
                "timezone": "UTC"
            },
            "container_name": null,
            "ext_id": "00063f0d-aa24-b21e-185b-ac1f6b6f97e2",
            "inefficient_vm_count": null,
            "links": null,
            "name": "auto_cluster_prod_f6143afd4db4",
            "network": {
                "backplane": {
                    "is_segmentation_enabled": false,
                    "netmask": null,
                    "subnet": null,
                    "vlan_tag": null
                },
                "external_address": {
                    "ipv4": {
                        "prefix_length": 32,
                        "value": "10.46.136.38"
                    },
                    "ipv6": null
                },
                "external_data_service_ip": {
                    "ipv4": {
                        "prefix_length": 32,
                        "value": "10.46.136.42"
                    },
                    "ipv6": null
                },
                "external_subnet": "10.46.136.0/255.255.248.0",
                "fqdn": null,
                "http_proxy_list": null,
                "http_proxy_white_list": null,
                "internal_subnet": "192.168.5.0/255.255.255.128",
                "key_management_server_type": null,
                "management_server": null,
                "masquerading_ip": null,
                "masquerading_port": null,
                "name_server_ip_list": [
                    {
                        "fqdn": null,
                        "ipv4": {
                            "prefix_length": 32,
                            "value": "10.40.64.15"
                        },
                        "ipv6": null
                    },
                    {
                        "fqdn": null,
                        "ipv4": {
                            "prefix_length": 32,
                            "value": "10.40.64.16"
                        },
                        "ipv6": null
                    }
                ],
                "nfs_subnet_whitelist": null,
                "ntp_server_ip_list": [
                    {
                        "fqdn": {
                            "value": "0.centos.pool.ntp.org"
                        },
                        "ipv4": null,
                        "ipv6": null
                    },
                    {
                        "fqdn": {
                            "value": "1.centos.pool.ntp.org"
                        },
                        "ipv4": null,
                        "ipv6": null
                    },
                    {
                        "fqdn": {
                            "value": "2.centos.pool.ntp.org"
                        },
                        "ipv4": null,
                        "ipv6": null
                    },
                    {
                        "fqdn": {
                            "value": "3.centos.pool.ntp.org"
                        },
                        "ipv4": null,
                        "ipv6": null
                    }
                ],
                "smtp_server": null
            },
            "nodes": {
                "node_list": [
                    {
                        "controller_vm_ip": {
                            "ipv4": {
                                "prefix_length": 32,
                                "value": "10.46.136.32"
                            },
                            "ipv6": null
                        },
                        "host_ip": {
                            "ipv4": {
                                "prefix_length": 32,
                                "value": "10.46.136.28"
                            },
                            "ipv6": null
                        },
                        "node_uuid": "cb48351c-ed6d-4791-930a-0d61bd0060bf"
                    }
                ],
                "number_of_nodes": 1
            },
            "tenant_id": null,
            "upgrade_status": "SUCCEEDED",
            "vm_count": 3
        }
changed:
    description: Whether the module made any changes
    type: bool
    returned: always
    sample: false
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: When an error occurs
failed:
    description: Indicates if the operation failed.
    type: bool
    returned: always
    sample: false
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:15cb540e-df8d-41d7-807c-d39fdd253e81"
cluster_ext_id:
    description: The external ID of the cluster.
    type: str
    returned: always
    sample: "0006361b-6855-3644-7458-2268f8ffb2bd"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cluster  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        categories=dict(type="list", elements="str", required=True),
    )
    return module_args


def associate_categories(module, result):
    clusters = get_clusters_api_instance(module)
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    sg = SpecGenerator(module)
    default_spec = clusters_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating cluster associate category spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = clusters.associate_categories_to_cluster(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating categories",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        resp = get_cluster(module, clusters, ext_id=cluster_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def disassociate_categories(module, result):
    clusters = get_clusters_api_instance(module)
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    sg = SpecGenerator(module)
    default_spec = clusters_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating cluster disassociate category spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = clusters.disassociate_categories_from_cluster(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating categories",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        resp = get_cluster(module, clusters, ext_id=cluster_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "cluster_ext_id": None,
        "task_ext_id": None,
    }
    state = module.params["state"]
    if state == "present":
        associate_categories(module, result)
    else:
        disassociate_categories(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
