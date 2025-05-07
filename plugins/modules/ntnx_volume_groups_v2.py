#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_v2
short_description: Manage Nutanix volume group in PC
description:
    - This module allows you to create and delete volume group in Nutanix PC.
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then module will create volume group.
            - if C(state) is set to C(absent) then module will delete volume group.
        choices:
            - present
            - absent
        type: str
        default: present
    wait:
        description: Wait for the operation to complete.
        type: bool
        required: false
        default: True
    ext_id:
        description:
            - The external ID of the volume group.
            - Required for C(state)=absent for delete.
        type: str
        required: false
    name:
        description:
            - Name of VG
        type: str
        required: false
    description:
        description:
            - Description of VG
        type: str
        required: false
    sharing_status:
        description:
            - Indicates whether the Volume Group can be shared across multiple iSCSI initiators.
            - The mode cannot be changed from SHARED to NOT_SHARED on a Volume Group with multiple attachments.
            - Similarly, a Volume Group cannot be associated with more than one attachment as long as it is in exclusive mode.
            - This is an optional field.
        type: str
        required: false
        choices:
            - SHARED
            - NOT_SHARED
    should_load_balance_vm_attachments:
        description:
            - Indicates whether to enable Volume Group load balancing for VM attachments.
        type: bool
        required: false
    target_prefix:
        description:
            - The specifications contain the target prefix for external clients as the value.
            - This is an optional field.
            - Mutually exclusive with C(target_name).
        required: false
        type: str
    target_name:
        description:
            - Name of the external client target that will be visible and accessible to the client
            - This is an optional field.
            - Mutually exclusive with C(target_prefix).
        required: false
        type: str
    enabled_authentications:
        description:
            - The authentication type enabled for the Volume Group. This is an optional field.
            - If omitted, authentication is not configured for the Volume Group.
            - If this is set to CHAP, the target/client secret must be provided.
            - This is an optional field.
        required: false
        choices:
            - CHAP
            - NONE
        type: str
    cluster_reference:
        description:
            - Cluster reference for VG, required for create.
        required: false
        type: str
    usage_type:
        description:
            - Expected usage type for the Volume Group.
            - This is an indicative hint on how the caller will consume the Volume Group.
            - This is an optional field.
        required: false
        type: str
        choices:
            - BACKUP_TARGET
            - INTERNAL
            - TEMPORARY
            - USER
    is_hidden:
        description:
            - Indicates whether the Volume Group is hidden.
        required: False
        type: bool
    storage_features:
        description:
            - Storage optimization features which must be enabled on the Volume Group
        required: false
        type: dict
        suboptions:
            flash_mode:
                description:
                    - Enable flash mode on the Volume Group.
                type: dict
                required: True
                suboptions:
                    is_enabled:
                        description:
                            - Indicates whether the flash mode is enabled or not.
                        type: bool
                        required: True
    iscsi_features:
        description:
            - iSCSI specific settings for the Volume Group.
        required: false
        type: dict
        suboptions:
            target_secret:
                description:
                    - Target secret in case of a CHAP authentication.
                type: str
                required: True
            enabled_authentications:
                description:
                    - The authentication type enabled for the Volume Group. This is an optional field.
                    - If omitted, authentication is not configured for the Volume Group.
                    - If this is set to CHAP, the target/client secret must be provided.
                    - This is an optional field.
                required: false
                choices:
                    - CHAP
                    - NONE
                type: str

extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Create Volume group with all config and enabled chap auth
  nutanix.ncp.ntnx_volume_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    name: "{{vg1_name}}"
    description: "Volume group 2"
    should_load_balance_vm_attachments: true
    sharing_status: "SHARED"
    target_prefix: "vg1"
    cluster_reference: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35
    usage_type: "USER"
    storage_features:
      flash_mode:
        is_enabled: true
    iscsi_features:
      target_secret: "Secret1234567"
      enabled_authentications: "CHAP"
  register: result
  ignore_errors: true

- name: Create Volume group with min spec and no Auth
  nutanix.ncp.ntnx_volume_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    name: "{{vg1_name}}"
    description: "Volume group 1"
    cluster_reference: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35
  register: result
  ignore_errors: true

- name: Delete Volume groups
  nutanix.ncp.ntnx_volume_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: absent
    ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b67
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Volume group details after creation if C(wait) is true.
        - Task details if C(wait) is false.
    type: dict
    returned: always
    sample: {
            "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
            "created_by": null,
            "created_time": null,
            "description": "Volume group 2",
            "enabled_authentications": null,
            "ext_id": "792cd764-37b5-4da3-7ef1-ea3f618c1648",
            "is_hidden": null,
            "iscsi_features": {
                "enabled_authentications": "CHAP",
                "iscsi_target_name": null,
                "target_secret": null
            },
            "iscsi_target_name": null,
            "iscsi_target_prefix": null,
            "links": null,
            "load_balance_vm_attachments": null,
            "name": "ansible-vgs-KjRMtTRxhrww2",
            "sharing_status": "SHARED",
            "should_load_balance_vm_attachments": true,
            "storage_features": {
                "flash_mode": {
                    "is_enabled": true
                }
            },
            "target_name": "vg1-792cd764-37b5-4da3-7ef1-ea3f618c1648",
            "target_prefix": null,
            "target_secret": null,
            "tenant_id": null,
            "usage_type": "USER"
        }
ext_id:
    description: Volume Group external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
task_ext_id:
    description: The task external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
error:
    description: The error message if any.
    type: str
    returned: when error occurs
    sample: "Failed generating create volume group spec"
changed:
    description: Indicates whether the resource has changed.
    type: bool
    returned: always
    sample: true
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_etag,
    get_vg_api_instance,
)
from ..module_utils.v4.volumes.helpers import get_volume_group  # noqa: E402
from ..module_utils.v4.volumes.spec.volume_group import (  # noqa: E402
    VGSpecs as vg_specs,
)

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = vg_specs.get_volume_group_spec()

    return module_args


def create_vg(module, result):
    vgs = get_vg_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.VolumeGroup()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create volume group spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vgs.create_volume_group(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating volume groups",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.VOLUME_GROUP
        )
        if ext_id:
            resp = get_volume_group(module, vgs, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_vg(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "VG with ext_id: {0} will be deleted.".format(ext_id)
        return

    vgs = get_vg_api_instance(module)
    vg = get_volume_group(module, vgs, ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vgs.delete_volume_group_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting volume group",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
        mutually_exclusive=[["target_name", "target_prefix"]],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_volumes_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            # Update not supported for pc.2024.1 release.
            pass
        else:
            create_vg(module, result)
    else:
        delete_vg(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
