#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_object_stores_data_movement_targets_v2
short_description: Create a data movement target for a Nutanix Object store
version_added: "2.7.0"
description:
    - Create a new data movement target resource under the given Object store.
    - Currently only remote Nutanix Objects data movement targets are supported.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Create Endpoint Object Store) -
      Required Roles: Objects Admin, Objects Editor, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=objects)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will create the data movement target.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    object_store_ext_id:
        description:
            - The UUID of the Object store.
        type: str
        required: true
    name:
        description:
            - The name of the data movement target in the Object store.
            - The name can contain only letters, numbers, and hyphens but must begin
              with a letter and end with a letter or a number.
            - For example - C(data-movement-target-1).
        type: str
        required: true
    type:
        description:
            - The type of the data movement target in the Object store.
            - C(NTNX_OBJECTS) indicates the data movement target belongs to remote
              Nutanix Objects.
        type: str
        required: true
        choices:
            - NTNX_OBJECTS
    details:
        description:
            - The details specific to the type of the data movement target in the
              Object store.
            - Nutanix Objects Data Movement Target Definition.
        type: dict
        required: true
        suboptions:
            object_store_ext_id:
                description:
                    - The extId of the remote Object store associated with the Nutanix
                      Objects data movement target.
                type: str
                required: true
            object_store_fqdn:
                description:
                    - The FQDN of the remote Object store associated with the Nutanix
                      Objects data movement target.
                type: dict
                required: true
                suboptions:
                    value:
                        description:
                            - The FQDN value.
                        type: str
                        required: true
            domain_manager_name:
                description:
                    - The name of the Domain Manager (Prism Central) instance that hosts
                      the remote Nutanix Objects.
                type: str
                required: false
            domain_manager_ext_id:
                description:
                    - The UUID of the Domain Manager (Prism Central) instance that hosts
                      the remote Nutanix Objects.
                    - This instance should already be registered with Prism Central that
                      is hosting the source Object store if the source and target
                      Object stores are hosted in different Prism Central instances.
                type: str
                required: true
            object_store_public_network_ips:
                description:
                    - The public network IP addresses of the Nutanix Objects associated
                      with the data movement target.
                type: list
                elements: dict
                required: true
                suboptions:
                    ipv4:
                        description:
                            - An IPv4 address.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description:
                                    - The IPv4 address value.
                                type: str
                                required: true
                            prefix_length:
                                description:
                                    - The prefix length of the network to which this
                                      host IPv4 address belongs.
                                type: int
                                required: false
                    ipv6:
                        description:
                            - An IPv6 address.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description:
                                    - The IPv6 address value.
                                type: str
                                required: true
                            prefix_length:
                                description:
                                    - The prefix length of the network to which this
                                      host IPv6 address belongs.
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
- name: Create a data movement target for an object store
  nutanix.ncp.ntnx_object_stores_data_movement_targets_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    object_store_ext_id: "7e69f898-227f-4b37-bdd3-cccd5f46fc96"
    name: "data-movement-target-1"
    type: "NTNX_OBJECTS"
    details:
      object_store_ext_id: "00062664-c65f-f854-65af-7cc25581f458"
      object_store_fqdn:
        value: "objects-0.pc.nutanix.com"
      domain_manager_ext_id: "00062664-c65f-f854-65af-7cc25581f459"
      object_store_public_network_ips:
        - ipv4:
            value: "10.10.10.10"
        - ipv4:
            value: "10.10.10.11"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for creating a data movement target.
        - Data movement target details if C(wait) is true.
        - Task details if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "tenant_id": "4cf559d1-4510-4f5f-ab44-008b4600f2b1",
            "ext_id": "8e36bec3-b4a4-427a-b54f-600604fd1e4c",
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ],
            "name": "data-movement-target-1",
            "type": "NTNX_OBJECTS",
            "details": {
                "object_store_ext_id": "00062664-c65f-f854-65af-7cc25581f458",
                "object_store_fqdn": {
                    "value": "objects-0.pc.nutanix.com"
                },
                "domain_manager_name": "alpha",
                "domain_manager_ext_id": "00062664-c65f-f854-65af-7cc25581f459",
                "object_store_public_network_ips": [
                    {
                        "ipv4": {
                            "value": "92.41.252.152",
                            "prefix_length": 32
                        },
                        "ipv6": {
                            "value": "0047:3611:a7d9:a64d:f8dd:fd83:9c6c:4eae",
                            "prefix_length": 128
                        }
                    }
                ]
            }
        }

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
    description: The external ID of the data movement target.
    returned: always
    type: str
    sample: "a1352721-9ade-4a39-a338-7569e57f3afc"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "Api Exception raised while creating object store data movement target"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.objects.api_client import (  # noqa: E402
    get_data_movement_targets_api_instance,
)
from ..module_utils.v4.objects.helpers import get_data_movement_target  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_objects_py_client as objects_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as objects_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )
    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )
    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )
    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_spec,
            obj=objects_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
            obj=objects_sdk.IPv6Address,
        ),
    )
    details_spec = dict(
        object_store_ext_id=dict(type="str", required=True),
        object_store_fqdn=dict(
            type="dict",
            required=True,
            options=fqdn_spec,
            obj=objects_sdk.FQDN,
        ),
        domain_manager_name=dict(type="str"),
        domain_manager_ext_id=dict(type="str", required=True),
        object_store_public_network_ips=dict(
            type="list",
            elements="dict",
            required=True,
            options=ip_address_spec,
            obj=objects_sdk.IPAddress,
        ),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        object_store_ext_id=dict(type="str", required=True),
        name=dict(type="str", required=True),
        type=dict(type="str", required=True, choices=["NTNX_OBJECTS"]),
        details=dict(
            type="dict",
            required=True,
            options=details_spec,
            obj=objects_sdk.NTNXObjectsDataMovementTarget,
        ),
    )
    return module_args


def create_data_movement_target(module, data_movement_targets_api, result):
    validate_required_params(module, ["object_store_ext_id", "name", "type", "details"])
    object_store_ext_id = module.params.get("object_store_ext_id")

    sg = SpecGenerator(module)
    default_spec = objects_sdk.DataMovementTarget()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating object store data movement target spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Data movement target would be created for object store with "
            "ext_id: {0} (check mode).".format(object_store_ext_id)
        )
        return

    try:
        resp = data_movement_targets_api.create_data_movement_target(
            objectStoreExtId=object_store_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating object store data movement target",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.DATA_MOVEMENT_TARGET
        )
        if ext_id:
            resp = get_data_movement_target(
                module, data_movement_targets_api, object_store_ext_id, ext_id
            )
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Data Movement Target"
                ),
                msg="Failed to get entity ext_id from task for Data Movement Target",
            )

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_objects_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    data_movement_targets_api = get_data_movement_targets_api_instance(module)
    create_data_movement_target(module, data_movement_targets_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
