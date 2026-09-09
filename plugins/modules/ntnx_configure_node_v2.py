#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_configure_node_v2
short_description: Configure a node in the hardware provider via Foundation Central
version_added: 2.7.0
description:
  - This module triggers a node configuration operation in the hardware provider through Foundation Central.
  - It applies node-specific configurations such as server settings, pre-cluster and post-cluster configuration,
    or unconfiguration of a server.
  - This is an action module and does not implement Create/Update/Delete state machines.
  - This module uses the Life Cycle Management v4 APIs based SDKs.
notes:
  - This module talks to B(Foundation Central) (FCVM/Foundation), NOT to Prism Central.
    Set C(nutanix_host) to the Foundation Central endpoint.
  - >-
    B(Configure a Node) - Requires the appropriate Foundation Central administrator role on the FCVM.
  - Exactly one of the C(configuration) suboptions must be provided.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module will configure the node.
    type: str
    choices:
      - present
    default: present
  configuration:
    description:
      - The configuration to apply to the node in the hardware provider.
      - Exactly one of the suboptions must be provided.
    type: dict
    required: true
    suboptions:
      configure_server_details:
        description:
          - Configuration details for setting up a server node in the hardware provider.
        type: dict
        required: false
        suboptions:
          node_ext_id:
            description:
              - External ID of the node to configure.
            type: str
            required: false
          group_id:
            description:
              - Group ID to associate the server node with.
            type: str
            required: false
          server_settings_config:
            description:
              - Server settings configuration.
            type: dict
            required: false
          physical_network_adapter_config:
            description:
              - Physical network adapter configuration.
            type: dict
            required: false
          bmc_ip_addressing_config:
            description:
              - BMC IP addressing configuration.
            type: dict
            required: false
      pre_cluster_config_details:
        description:
          - Pre-cluster configuration details applied before cluster creation.
        type: dict
        required: false
        suboptions:
          nodes:
            description:
              - List of nodes (by external ID) to include in the pre-cluster configuration.
            type: list
            elements: dict
            required: false
            suboptions:
              ext_id:
                description:
                  - External ID of the node.
                type: str
                required: false
      post_cluster_config_details:
        description:
          - Post-cluster configuration details applied after cluster creation.
        type: dict
        required: false
        suboptions:
          cluster_ext_id:
            description:
              - External ID of the cluster the nodes belong to.
            type: str
            required: false
          nodes:
            description:
              - List of nodes (by external ID) to include in the post-cluster configuration.
            type: list
            elements: dict
            required: false
            suboptions:
              ext_id:
                description:
                  - External ID of the node.
                type: str
                required: false
      un_configure_server_details:
        description:
          - Details required to unconfigure a server node in the hardware provider.
        type: dict
        required: false
        suboptions:
          node_ext_id:
            description:
              - External ID of the node to unconfigure.
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
- name: Configure a server node
  nutanix.ncp.ntnx_configure_node_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    configuration:
      configure_server_details:
        node_ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
        group_id: "group-1"
  register: result
  ignore_errors: true

- name: Apply pre-cluster configuration to nodes
  nutanix.ncp.ntnx_configure_node_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    configuration:
      pre_cluster_config_details:
        nodes:
          - ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
  register: result
  ignore_errors: true

- name: Unconfigure a server node
  nutanix.ncp.ntnx_configure_node_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    configuration:
      un_configure_server_details:
        node_ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for configuring a node.
    - Task details when C(wait) is true.
  returned: always
  type: dict
  sample:
    {
      "completed_time": "2026-09-09T06:26:51.524581+00:00",
      "created_time": "2026-09-09T06:26:47.167906+00:00",
      "entities_affected": [
        {"ext_id": "d1a1a1a1-1111-2222-3333-444455556666", "rel": "lifecycle:config:node"}
      ],
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "operation": "ConfigureNode",
      "operation_description": "Configure node",
      "status": "SUCCEEDED"
    }

changed:
  description: This indicates whether the action was executed.
  returned: always
  type: bool
  sample: true

task_ext_id:
  description: The external ID of the task.
  returned: when applicable
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the related entity if returned.
  returned: when applicable
  type: str
  sample: "d1a1a1a1-1111-2222-3333-444455556666"

skipped:
  description: This indicates whether the action was skipped (e.g. in check mode).
  returned: when applicable
  type: bool
  sample: false

msg:
  description: This indicates the status or error message.
  returned: contextual
  type: str
  sample: "Node configuration will be triggered."

error:
  description: This field holds the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_nodes_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    node_info_spec = dict(
        ext_id=dict(type="str", required=False),
    )

    configure_server_details_spec = dict(
        node_ext_id=dict(type="str", required=False),
        group_id=dict(type="str", required=False),
        server_settings_config=dict(type="dict", required=False),
        physical_network_adapter_config=dict(type="dict", required=False),
        bmc_ip_addressing_config=dict(type="dict", required=False),
    )

    pre_cluster_config_details_spec = dict(
        nodes=dict(
            type="list",
            elements="dict",
            options=node_info_spec,
            obj=lifecycle_sdk.NodeInfo,
            required=False,
        ),
    )

    post_cluster_config_details_spec = dict(
        cluster_ext_id=dict(type="str", required=False),
        nodes=dict(
            type="list",
            elements="dict",
            options=node_info_spec,
            obj=lifecycle_sdk.NodeInfo,
            required=False,
        ),
    )

    un_configure_server_details_spec = dict(
        node_ext_id=dict(type="str", required=False),
    )

    configuration_spec = dict(
        configure_server_details=dict(
            type="dict",
            options=configure_server_details_spec,
            obj=lifecycle_sdk.ConfigureServerDetails,
        ),
        pre_cluster_config_details=dict(
            type="dict",
            options=pre_cluster_config_details_spec,
            obj=lifecycle_sdk.PreClusterConfigDetails,
        ),
        post_cluster_config_details=dict(
            type="dict",
            options=post_cluster_config_details_spec,
            obj=lifecycle_sdk.PostClusterConfigDetails,
        ),
        un_configure_server_details=dict(
            type="dict",
            options=un_configure_server_details_spec,
            obj=lifecycle_sdk.UnConfigureServerDetails,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        configuration=dict(
            type="dict",
            required=True,
            options=configuration_spec,
            obj={
                "configure_server_details": lifecycle_sdk.ConfigureServerDetails,
                "pre_cluster_config_details": lifecycle_sdk.PreClusterConfigDetails,
                "post_cluster_config_details": lifecycle_sdk.PostClusterConfigDetails,
                "un_configure_server_details": lifecycle_sdk.UnConfigureServerDetails,
            },
            mutually_exclusive=[
                (
                    "configure_server_details",
                    "pre_cluster_config_details",
                    "post_cluster_config_details",
                    "un_configure_server_details",
                )
            ],
        ),
    )
    return module_args


def run_action(module, result, api_instance):
    validate_required_params(module, ["configuration"])

    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.ConfigureNodeSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for configuring node", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Node configuration will be triggered."
        return

    resp = None
    try:
        resp = api_instance.configure_node(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while configuring node",
        )
    if resp is not None and getattr(resp, "data", None) is not None:
        task_ext_id = getattr(resp.data, "ext_id", None)
        result["task_ext_id"] = task_ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        if task_ext_id and module.params.get("wait"):
            task = wait_for_completion(module, task_ext_id)
            result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_nodes_api_instance(module)
    run_action(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
