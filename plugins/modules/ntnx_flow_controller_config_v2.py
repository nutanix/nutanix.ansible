#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_flow_controller_config_v2
short_description: Update Flow Controller configuration
version_added: "2.7.0"
description:
    - Updates the Flow Controller configuration and recomputes required resources.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update Flow Controller configuration) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will update the Flow Controller configuration.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    vm_count:
        description:
            - Total number of VMs to be managed by the Flow Controller.
        type: int
        required: false
    subnet_count:
        description:
            - Total number of subnets to be managed by the Flow Controller.
        type: int
        required: false
    capabilities:
        description:
            - Capabilities and scale parameters configured for the Flow Controller.
        type: dict
        required: false
        suboptions:
            vlan_networking:
                description:
                    - VLAN networking capability for the Flow Controller.
                type: dict
                required: false
                suboptions:
                    is_enabled:
                        description:
                            - Indicates whether the VLAN networking capability is enabled for the Flow Controller.
                        type: bool
                        required: false
            virtual_networking:
                description:
                    - Virtual networking capability for the Flow Controller.
                type: dict
                required: false
                suboptions:
                    is_enabled:
                        description:
                            - Indicates whether the virtual networking capability is enabled for the Flow Controller.
                        type: bool
                        required: false
                    scale:
                        description:
                            - Scale parameters for the virtual networking capability.
                        type: dict
                        required: false
                        suboptions:
                            vpc_count:
                                description:
                                    - Number of VPCs supported by the Flow Controller.
                                type: int
                                required: false
                            load_balancer_count:
                                description:
                                    - Number of load balancers supported by the Flow Controller.
                                type: int
                                required: false
                            gateway_node_count:
                                description:
                                    - Number of gateway nodes supported by the Flow Controller.
                                type: int
                                required: false
            network_security_app_centric:
                description:
                    - App-centric network security capability for the Flow Controller.
                type: dict
                required: false
                suboptions:
                    is_enabled:
                        description:
                            - Indicates whether the app-centric network security capability is enabled for the Flow Controller.
                        type: bool
                        required: false
                    scale:
                        description:
                            - Scale parameters for the app-centric network security capability.
                        type: dict
                        required: false
                        suboptions:
                            security_policy_count:
                                description:
                                    - Number of app-centric security policies supported by the Flow Controller.
                                type: int
                                required: false
                            address_group_count:
                                description:
                                    - Number of address groups supported by the Flow Controller.
                                type: int
                                required: false
                            service_group_count:
                                description:
                                    - Number of service groups supported by the Flow Controller.
                                type: int
                                required: false
                            entity_group_count:
                                description:
                                    - Number of entity groups supported by the Flow Controller.
                                type: int
                                required: false
            security_analytics:
                description:
                    - Security analytics capability for the Flow Controller.
                type: dict
                required: false
                suboptions:
                    is_enabled:
                        description:
                            - Indicates whether the security analytics capability is enabled for the Flow Controller.
                        type: bool
                        required: false
                    scale:
                        description:
                            - Scale parameters for the security analytics capability.
                        type: dict
                        required: false
                        suboptions:
                            analytics_retention_days:
                                description:
                                    - Retention period for security analytics data in days.
                                type: int
                                required: false
                            analytics_storage_gib:
                                description:
                                    - Storage for security analytics data in GiB.
                                type: int
                                required: false
            containers:
                description:
                    - Containers capability for the Flow Controller.
                type: dict
                required: false
                suboptions:
                    is_enabled:
                        description:
                            - Indicates whether the containers capability is enabled for the Flow Controller.
                        type: bool
                        required: false
                    scale:
                        description:
                            - Scale parameters for the containers capability.
                        type: dict
                        required: false
                        suboptions:
                            kubernetes_cluster_count:
                                description:
                                    - Number of Kubernetes clusters supported by the Flow Controller.
                                type: int
                                required: false
            network_security_rule_centric:
                description:
                    - Rule-centric network security capability for the Flow Controller.
                type: dict
                required: false
                suboptions:
                    is_enabled:
                        description:
                            - Indicates whether the rule-centric network security capability is enabled for the Flow Controller.
                        type: bool
                        required: false
                    scale:
                        description:
                            - Scale parameters for the rule-centric network security capability.
                        type: dict
                        required: false
                        suboptions:
                            security_policy_count:
                                description:
                                    - Number of rule-centric security policies supported by the Flow Controller.
                                type: int
                                required: false
                            address_group_count:
                                description:
                                    - Number of address groups supported by the Flow Controller.
                                type: int
                                required: false
                            service_group_count:
                                description:
                                    - Number of service groups supported by the Flow Controller.
                                type: int
                                required: false
                            entity_group_count:
                                description:
                                    - Number of entity groups supported by the Flow Controller.
                                type: int
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
- name: Update Flow Controller configuration
  nutanix.ncp.ntnx_flow_controller_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_count: 1000
    subnet_count: 500
    capabilities:
      vlan_networking:
        is_enabled: true
      virtual_networking:
        is_enabled: true
        scale:
          vpc_count: 10
          load_balancer_count: 5
          gateway_node_count: 2
      network_security_app_centric:
        is_enabled: true
        scale:
          security_policy_count: 100
          address_group_count: 50
          service_group_count: 50
          entity_group_count: 20
      security_analytics:
        is_enabled: false
      containers:
        is_enabled: false
      network_security_rule_centric:
        is_enabled: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for updating Flow Controller configuration.
        - If C(wait) is true, it will contain the Flow Controller configuration details after completion.
        - If C(wait) is false, it will contain the task details.
    type: dict
    returned: always
    sample:
        {
            "capabilities": {
                "containers": {
                    "is_enabled": false,
                    "scale": null
                },
                "network_security_app_centric": {
                    "is_enabled": true,
                    "scale": {
                        "address_group_count": 50,
                        "entity_group_count": 20,
                        "security_policy_count": 100,
                        "service_group_count": 50
                    }
                },
                "network_security_rule_centric": {
                    "is_enabled": false,
                    "scale": null
                },
                "security_analytics": {
                    "is_enabled": false,
                    "scale": null
                },
                "virtual_networking": {
                    "is_enabled": true,
                    "scale": {
                        "gateway_node_count": 2,
                        "load_balancer_count": 5,
                        "vpc_count": 10
                    }
                },
                "vlan_networking": {
                    "is_enabled": true
                }
            },
            "required_resources": [
                {
                    "cpu": 4,
                    "deployment_mode": "SMALL",
                    "disk_mib": 102400,
                    "memory_mib": 8192
                }
            ],
            "subnet_count": 500,
            "vm_count": 1000
        }
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
skipped:
    description: This indicates whether the task was skipped
    type: bool
    returned: When the operation was skipped
    sample: true
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e"
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error or module is idempotent
    sample: "Nothing to change."
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
"""

import copy  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_flow_controller_config_api_instance,
)
from ..module_utils.v4.network.helpers import get_flow_controller_config  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    vlan_networking_spec = dict(
        is_enabled=dict(type="bool", required=False),
    )

    virtual_networking_scale_spec = dict(
        vpc_count=dict(type="int", required=False),
        load_balancer_count=dict(type="int", required=False),
        gateway_node_count=dict(type="int", required=False),
    )

    virtual_networking_spec = dict(
        is_enabled=dict(type="bool", required=False),
        scale=dict(
            type="dict",
            options=virtual_networking_scale_spec,
            required=False,
            obj=networking_sdk.VirtualNetworkingScale,
        ),
    )

    network_security_app_centric_scale_spec = dict(
        security_policy_count=dict(type="int", required=False),
        address_group_count=dict(type="int", required=False),
        service_group_count=dict(type="int", required=False),
        entity_group_count=dict(type="int", required=False),
    )

    network_security_app_centric_spec = dict(
        is_enabled=dict(type="bool", required=False),
        scale=dict(
            type="dict",
            options=network_security_app_centric_scale_spec,
            required=False,
            obj=networking_sdk.NetworkSecurityAppCentricScale,
        ),
    )

    security_analytics_scale_spec = dict(
        analytics_retention_days=dict(type="int", required=False),
        analytics_storage_gib=dict(type="int", required=False),
    )

    security_analytics_spec = dict(
        is_enabled=dict(type="bool", required=False),
        scale=dict(
            type="dict",
            options=security_analytics_scale_spec,
            required=False,
            obj=networking_sdk.SecurityAnalyticsScale,
        ),
    )

    containers_scale_spec = dict(
        kubernetes_cluster_count=dict(type="int", required=False),
    )

    containers_spec = dict(
        is_enabled=dict(type="bool", required=False),
        scale=dict(
            type="dict",
            options=containers_scale_spec,
            required=False,
            obj=networking_sdk.ContainersScale,
        ),
    )

    network_security_rule_centric_scale_spec = dict(
        security_policy_count=dict(type="int", required=False),
        address_group_count=dict(type="int", required=False),
        service_group_count=dict(type="int", required=False),
        entity_group_count=dict(type="int", required=False),
    )

    network_security_rule_centric_spec = dict(
        is_enabled=dict(type="bool", required=False),
        scale=dict(
            type="dict",
            options=network_security_rule_centric_scale_spec,
            required=False,
            obj=networking_sdk.NetworkSecurityRuleCentricScale,
        ),
    )

    capabilities_spec = dict(
        vlan_networking=dict(
            type="dict",
            options=vlan_networking_spec,
            required=False,
            obj=networking_sdk.VlanNetworkingCapability,
        ),
        virtual_networking=dict(
            type="dict",
            options=virtual_networking_spec,
            required=False,
            obj=networking_sdk.VirtualNetworkingCapability,
        ),
        network_security_app_centric=dict(
            type="dict",
            options=network_security_app_centric_spec,
            required=False,
            obj=networking_sdk.NetworkSecurityAppCentricCapability,
        ),
        security_analytics=dict(
            type="dict",
            options=security_analytics_spec,
            required=False,
            obj=networking_sdk.SecurityAnalyticsCapability,
        ),
        containers=dict(
            type="dict",
            options=containers_spec,
            required=False,
            obj=networking_sdk.ContainersCapability,
        ),
        network_security_rule_centric=dict(
            type="dict",
            options=network_security_rule_centric_spec,
            required=False,
            obj=networking_sdk.NetworkSecurityRuleCentricCapability,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        vm_count=dict(type="int"),
        subnet_count=dict(type="int"),
        capabilities=dict(
            type="dict",
            options=capabilities_spec,
            required=False,
            obj=networking_sdk.FlowControllerCapabilities,
        ),
    )
    return module_args


def check_flow_controller_config_idempotency(current_spec, update_spec):
    """
    Check if Flow Controller config update is idempotent.
    Compares writable fields between current and update specs.
    """
    current_dict = strip_internal_attributes(current_spec.to_dict())
    update_dict = strip_internal_attributes(update_spec.to_dict())

    # Remove read-only fields that are not part of writable spec
    read_only_fields = [
        "required_resources",
        "ext_id",
        "links",
        "tenant_id",
        "metadata",
    ]
    for field in read_only_fields:
        current_dict.pop(field, None)
        update_dict.pop(field, None)

    # Remove internal fields
    for d in (current_dict, update_dict):
        d.pop("_reserved", None)
        d.pop("_object_type", None)
        d.pop("_unknown_fields", None)

    return current_dict == update_dict


def update_flow_controller_config(module, result, api_instance):
    current_spec = get_flow_controller_config(module, api_instance)
    etag_value = get_etag(data=current_spec)

    sg = SpecGenerator(module)
    default_spec = copy.deepcopy(current_spec)
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for updating Flow Controller config",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_flow_controller_config_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = {}
    if etag_value:
        kwargs["if_match"] = etag_value

    resp = None
    try:
        resp = api_instance.update_flow_controller_config(body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Flow Controller config",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        updated_config = get_flow_controller_config(module, api_instance)
        result["response"] = strip_internal_attributes(updated_config.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
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
    }
    api_instance = get_flow_controller_config_api_instance(module)
    update_flow_controller_config(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
