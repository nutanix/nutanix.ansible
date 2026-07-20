#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_check_hypervisor_requirement_v2
short_description: Check whether a hypervisor ISO upload is required before expanding a Nutanix cluster
version_added: 2.7.0
description:
    - Trigger the Nutanix Prism Central v4 cluster management action
      B(check-hypervisor-requirements) against a target cluster.
    - Given the list of nodes that are being considered for cluster expansion, the API
      evaluates whether the target cluster needs a hypervisor bundle (ISO / tar.gz)
      to be uploaded prior to imaging and adding those nodes.
    - The API is asynchronous. A C(TaskReference) is returned immediately and the
      module (when C(wait=true)) polls the task and fetches the hypervisor upload
      information via C(fetchTaskResponse) with response type C(HYPERVISOR_UPLOAD_INFO).
    - This module wraps the C(POST /api/clustermgmt/v4.2/config/clusters/{clusterExtId}/$actions/check-hypervisor-requirements)
      endpoint of the C(ntnx_clustermgmt_py_client) SDK.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Get hypervisor ISO upload information) -
      Required Roles: Cluster Admin, Super Admin, Prism Admin, Internal Super Admin,
      Self-Service Admin (deprecated), Project Manager.
    - This API is not supported for the C(XEN) hypervisor type.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported for this action module. Setting any other
              value causes the module to fail.
        type: str
        choices:
            - present
        default: present
    cluster_ext_id:
        description:
            - External ID (UUID) of the target cluster on which the
              C(check-hypervisor-requirements) action is invoked.
        type: str
        required: true
    node_list:
        description:
            - List of node details for which the hypervisor upload requirement should
              be evaluated. Each item describes a single incoming node being
              considered for expansion.
        type: list
        elements: dict
        required: true
        suboptions:
            node_uuid:
                description:
                    - UUID of the host / node.
                type: str
            hypervisor_version:
                description:
                    - Host / hypervisor version currently reported by the node.
                type: str
            nos_version:
                description:
                    - NOS (AOS) software version of the node.
                type: str
            model:
                description:
                    - Rackable unit model type of the node.
                type: str
            block_id:
                description:
                    - Rackable unit ID (block) that the node belongs to.
                type: str
            is_light_compute:
                description:
                    - Indicates whether the node is a light compute node or not.
                type: bool
            hypervisor_type:
                description:
                    - Hypervisor type reported by the node. The API is not supported
                      for the C(XEN) hypervisor.
                type: str
                choices:
                    - AHV
                    - ESX
                    - HYPERV
                    - XEN
                    - NATIVEHOST
            is_robo_mixed_hypervisor:
                description:
                    - Indicates whether the node is part of a ROBO deployment with a
                      mixed hypervisor.
                type: bool
            is_minimum_compute_node:
                description:
                    - Indicates whether the node is a minimum-compute node.
                type: bool
            luks_status:
                description:
                    - LUKS encryption status reported by the node.
                type: str
                choices:
                    - NON_LUKS
                    - LUKS
                    - PARTIAL_LUKS
                    - UNKNOWN_LUKS
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
- name: Check hypervisor requirements for an incoming AHV node
  nutanix.ncp.ntnx_check_hypervisor_requirement_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "000628e4-4c8f-1239-5575-0cc47a9a3e6d"
    node_list:
      - node_uuid: "54b7581b-2e35-413e-8608-0531b065a5d8"
        hypervisor_version: "10.0-793"
        nos_version: "7.0"
        model: "NX-3060-G5"
        block_id: "18SM8B010159"
        is_light_compute: false
        hypervisor_type: "AHV"
        is_robo_mixed_hypervisor: false
        is_minimum_compute_node: false
        luks_status: "NON_LUKS"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for the C(check-hypervisor-requirements) action.
        - When C(wait) is C(true), this contains the resolved task response
          (from C(fetchTaskResponse) with C(taskResponseType=HYPERVISOR_UPLOAD_INFO))
          describing, for each node, whether a hypervisor bundle upload is required.
        - When C(wait) is C(false), this contains the initial task reference.
        - When C(check_mode) is set, this contains the generated request spec.
    returned: always
    type: dict
    sample:
        {
            "ext_id": "adaf1a22-b003-4361-4b00-450648fc3be5",
            "links": null,
            "response": {
                "error_message": "The nodes you have selected are running hypervisor
                                  version(s) which are different than existing
                                  versions: kvm: 11.2 on cluster or a nos version
                                  which is higher than that of the cluster version.
                                  Please choose or upload installer tar.gz(s) to
                                  reimage new nodes",
                "upload_info_node_list": [
                    {
                        "available_hypervisor_iso_error": "null",
                        "bundle_name": null,
                        "is_hypervisor_upload_required": true,
                        "is_imaging_mandatory": true,
                        "is_node_compatible": false,
                        "md5_sum": null,
                        "node_uuid": "54b7581b-2e35-413e-8608-0531b065a5d8",
                        "required_hypervisor_type": "AHV"
                    }
                ]
            },
            "task_response_type": "HYPERVISOR_UPLOAD_INFO",
            "tenant_id": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while checking hypervisor requirements"

error:
    description:
        - This field typically holds information about if the task have errors that
          occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Failed generating spec for checking hypervisor requirements"

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task returned by the API.
    returned: always
    type: str
    sample: "ZXJnb24=:adaf1a22-b003-4361-4b00-450648fc3be5"

ext_id:
    description: The external ID of the cluster on which the action was invoked.
    returned: always
    type: str
    sample: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    node_list_spec = dict(
        node_uuid=dict(type="str"),
        hypervisor_version=dict(type="str"),
        nos_version=dict(type="str"),
        model=dict(type="str"),
        block_id=dict(type="str"),
        is_light_compute=dict(type="bool"),
        hypervisor_type=dict(
            type="str",
            choices=["AHV", "ESX", "HYPERV", "XEN", "NATIVEHOST"],
            obj=cluster_management_sdk.HypervisorType,
        ),
        is_robo_mixed_hypervisor=dict(type="bool"),
        is_minimum_compute_node=dict(type="bool"),
        luks_status=dict(
            type="str",
            choices=["NON_LUKS", "LUKS", "PARTIAL_LUKS", "UNKNOWN_LUKS"],
            obj=cluster_management_sdk.NodeLuksStatus,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        node_list=dict(
            type="list",
            elements="dict",
            required=True,
            options=node_list_spec,
            obj=cluster_management_sdk.HypervisorUploadNodeListItem,
        ),
    )

    return module_args


def check_hypervisor_requirements(module, api_instance, result):
    """
    Invoke the CheckHypervisorRequirements action on the target cluster and,
    when running with wait=True, poll the resulting task and fetch the hypervisor
    upload information via fetch_task_response(HYPERVISOR_UPLOAD_INFO).
    """
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.HypervisorUploadParam()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for checking hypervisor requirements",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.check_hypervisor_requirements(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while checking hypervisor requirements",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        fetch_task_ext_id = task_ext_id
        # The fetch_task_response endpoint expects the task ext_id WITHOUT the
        # base64-encoded service prefix (`ergon:...`); strip it if present.
        if ":" in fetch_task_ext_id:
            fetch_task_ext_id = fetch_task_ext_id.split(":")[1]
        try:
            task_response = api_instance.fetch_task_response(
                extId=fetch_task_ext_id,
                taskResponseType="HYPERVISOR_UPLOAD_INFO",
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while fetching hypervisor upload information",
            )
        result["response"] = strip_internal_attributes(task_response.data.to_dict())


def run_module():
    module = BaseModuleV4(
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
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_clusters_api_instance(module)
    check_hypervisor_requirements(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
