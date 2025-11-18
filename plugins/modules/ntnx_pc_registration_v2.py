#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_pc_registration_v2
short_description: Registers a domain manager (Prism Central) instance to other entities like PE and PC
version_added: 2.0.0
description:
    - Registers a domain manager (Prism Central) instance to other entities like PE and PC
    - Unregistration of a domain manager (Prism Central) instance is not supported
    - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - State of the module.
      - If state is present, the module will register a Prism Central.
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
  ext_id:
    description:
            - The external ID of the prism central cluster.
            - Required for registering prism central to a remote cluster.
    type: str
    required: true
  remote_cluster:
    description:
        - Description of the remote cluster.
    type: dict
    required: true
    suboptions:
        domain_manager_remote_cluster:
            description:
                - Domain manager (Prism Central) remote cluster details.
            type: dict
            suboptions:
                remote_cluster:
                    description:
                        - The remote cluster details.
                    type: dict
                    required: true
                    suboptions:
                        address:
                            description:
                                - The address of the remote cluster.
                            type: dict
                            required: true
                            suboptions:
                                ipv4:
                                    description:
                                        - The IPv4 address of the remote cluster.
                                    type: dict
                                    suboptions:
                                        value:
                                            description:
                                                - The IPv4 address value.
                                            type: str
                                            required: true
                                        prefix_length:
                                            description:
                                                - The IPv4 address prefix length.
                                            type: int
                                            required: false
                                            default: 32
                                ipv6:
                                    description:
                                        - The IPv6 address of the remote cluster.
                                    type: dict
                                    suboptions:
                                        value:
                                            description:
                                                - The IPv6 address value.
                                            type: str
                                            required: true
                                        prefix_length:
                                            description:
                                                - The IPv6 address prefix length.
                                            type: int
                                            required: false
                                            default: 128
                                fqdn:
                                    description:
                                        - The FQDN of the remote cluster.
                                    type: dict
                                    suboptions:
                                        value:
                                            description:
                                                - The FQDN value.
                                            type: str
                                            required: true
                        credentials:
                            description:
                                - The credentials of the remote cluster.
                            type: dict
                            required: true
                            suboptions:
                                authentication:
                                    description:
                                        - The authentication details.
                                    type: dict
                                    required: true
                                    suboptions:
                                        username:
                                            description:
                                                - The username of the remote cluster.
                                            type: str
                                            required: true
                                        password:
                                            description:
                                                - The password of the remote cluster.
                                            type: str
                                            required: true
                cloud_type:
                    description:
                        - The cloud type of the remote cluster.
                    type: str
                    choices:
                        - NUTANIX_HOSTED_CLOUD
                        - ONPREM_CLOUD
                    required: true
        aos_remote_cluster:
            description:
                - The AOS remote cluster details.
                - Register a Prism Element to current Prism Central
            type: dict
            suboptions:
                remote_cluster:
                    description:
                        - The remote cluster details.
                    type: dict
                    required: true
                    suboptions:
                        address:
                            description:
                                - The address of the remote cluster.
                            type: dict
                            required: true
                            suboptions:
                                ipv4:
                                    description:
                                        - The IPv4 address of the remote cluster.
                                    type: dict
                                    suboptions:
                                        value:
                                            description:
                                                - The IPv4 address value.
                                            type: str
                                            required: true
                                        prefix_length:
                                            description:
                                                - The IPv4 address prefix length.
                                            type: int
                                            required: false
                                            default: 32
                                ipv6:
                                    description:
                                        - The IPv6 address of the remote cluster.
                                    type: dict
                                    suboptions:
                                        value:
                                            description:
                                                - The IPv6 address value.
                                            type: str
                                            required: true
                                        prefix_length:
                                            description:
                                                - The IPv6 address prefix length.
                                            type: int
                                            required: false
                                            default: 128
                                fqdn:
                                    description:
                                        - The FQDN of the remote cluster.
                                    type: dict
                                    suboptions:
                                        value:
                                            description:
                                                - The FQDN value.
                                            type: str
                                            required: true
                        credentials:
                            description:
                                - The credentials of the remote cluster.
                            type: dict
                            required: true
                            suboptions:
                                authentication:
                                    description:
                                        - The authentication details.
                                    type: dict
                                    required: true
                                    suboptions:
                                        username:
                                            description:
                                                - The username of the remote cluster.
                                            type: str
                                            required: true
                                        password:
                                            description:
                                                - The password of the remote cluster.
                                            type: str
                                            required: true
        cluster_reference:
            description:
                - The cluster reference details.
            type: dict
            suboptions:
                ext_id:
                    description:
                        - The external ID of the cluster.
                    type: str
                    required: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger
author:
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: PE PC registration
  nutanix.ncp.ntnx_pc_registration_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "00000000-0000-0000-0000-000000000000"
    remote_cluster:
      aos_remote_cluster:
        remote_cluster:
          address:
            ipv4:
              value: "10.0.0.1"
          credentials:
            authentication:
              username: "admin"
              password: "password"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
        - Response for prism central registration operation.
        - This field typically holds the task details.
  returned: always
  type: dict
  sample:
    {
        "cluster_ext_ids": null,
        "completed_time": "2024-10-15T07:16:04.131903+00:00",
        "completion_details": null,
        "created_time": "2024-10-15T07:15:25.618518+00:00",
        "entities_affected": [
            {
                "ext_id": "00062458-703d-3e3f-0992-ff4d2894511e",
                "name": "00062458-703d-3e3f-0992-ff4d2894511e",
                "rel": "clustermgmt:config:cluster"
            },
            {
                "ext_id": "d2f9994f-44fb-4d4c-ad3c-92055316444f",
                "name": "PC_10.44.76.49",
                "rel": "prism:management:domain_manager"
            }
        ],
        "error_messages": null,
        "ext_id": "ZXJnb24=:1dd2b6d5-595d-5c4e-918b-b2e312141ac0",
        "is_background_task": false,
        "is_cancelable": false,
        "last_updated_time": "2024-10-15T07:16:04.131902+00:00",
        "legacy_error_message": null,
        "number_of_entities_affected": 2,
        "number_of_subtasks": 0,
        "operation": "RegisterAOS",
        "operation_description": "Register Prism Element",
        "owned_by": {
            "ext_id": "00000000-0000-0000-0000-000000000000",
            "name": "admin"
        },
        "parent_task": null,
        "progress_percentage": 100,
        "root_task": null,
        "started_time": "2024-10-15T07:15:27.717634+00:00",
        "status": "SUCCEEDED",
        "sub_steps": null,
        "sub_tasks": null,
        "warnings": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: When an error occurs
  type: str

ext_id:
  description: The external ID of the prism central cluster.
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"

task_ext_id:
    description: Task external ID.
    type: str
    returned: always
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
)
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

    ipv4_address = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    fqdn = dict(value=dict(type="str", required=True))

    address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address,
            obj=prism_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address,
            obj=prism_sdk.IPv6Address,
            required=False,
        ),
        fqdn=dict(type="dict", options=fqdn, obj=prism_sdk.FQDN, required=False),
    )
    credentials_spec = dict(
        authentication=dict(
            type="dict",
            obj=prism_sdk.BasicAuth,
            options=dict(
                username=dict(type="str", required=True),
                password=dict(type="str", required=True, no_log=True),
            ),
            required=True,
        )
    )

    remote_cluster_spec = dict(
        address=dict(
            type="dict",
            options=address_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
            mutually_exclusive=[("ipv4", "ipv6", "fqdn")],
        ),
        credentials=dict(
            type="dict",
            options=credentials_spec,
            obj=prism_sdk.Credentials,
            required=True,
        ),
    )
    domain_manager_remote_cluster_spec = dict(
        remote_cluster=dict(
            type="dict",
            options=remote_cluster_spec,
            obj=prism_sdk.RemoteClusterSpec,
            required=True,
        ),
        cloud_type=dict(
            type="str",
            choices=["NUTANIX_HOSTED_CLOUD", "ONPREM_CLOUD"],
            required=True,
        ),
    )

    aos_remote_cluster_spec = dict(
        remote_cluster=dict(
            type="dict",
            options=remote_cluster_spec,
            obj=prism_sdk.RemoteClusterSpec,
            required=True,
        ),
    )

    cluster_reference_spec = dict(
        ext_id=dict(type="str", required=True),
    )
    remote_cluster_allowed_types = {
        "domain_manager_remote_cluster": prism_sdk.DomainManagerRemoteClusterSpec,
        "aos_remote_cluster": prism_sdk.AOSRemoteClusterSpec,
        "cluster_reference": prism_sdk.ClusterReference,
    }
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        remote_cluster=dict(
            type="dict",
            obj=remote_cluster_allowed_types,
            options=dict(
                domain_manager_remote_cluster=dict(
                    type="dict",
                    options=domain_manager_remote_cluster_spec,
                    required=False,
                ),
                aos_remote_cluster=dict(
                    type="dict",
                    options=aos_remote_cluster_spec,
                    required=False,
                ),
                cluster_reference=dict(
                    type="dict", options=cluster_reference_spec, required=False
                ),
            ),
            mutually_exclusive=[
                (
                    "domain_manager_remote_cluster",
                    "aos_remote_cluster",
                    "cluster_reference",
                )
            ],
            required=True,
        ),
    )
    return module_args


def register_pc(module, domain_manager, result):
    sg = SpecGenerator(module)
    default_spec = prism_sdk.ClusterRegistrationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating PC registration Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = domain_manager.register(body=spec, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while PC registration",
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
            msg=missing_required_lib("ntnx_prism_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    domain_manager = get_domain_manager_api_instance(module)
    register_pc(module, domain_manager, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
