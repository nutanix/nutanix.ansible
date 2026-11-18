#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_image_rate_limit_policy_v2
short_description: Manage image rate limit policies in Nutanix Prism Central
description:
    - This module allows you to create, update, and delete image rate limit policies in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
version_added: "2.6.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create an image rate limit policy) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Update an image rate limit policy) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Delete an image rate limit policy) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then the operation will be create the image rate limit policy.
            - if C(state) is set to C(present) and C(ext_id) is given then it will update the image rate limit policy.
            - if C(state) is set to C(absent) and C(ext_id) is given then it will delete the image rate limit policy.
        choices:
            - present
            - absent
        type: str
        default: present
    ext_id:
        description:
            - The unique identifier of the image rate limit policy.
            - This parameter is required for update and delete operations.
        required: false
        type: str
    name:
        description:
            - The name of the image rate limit policy.
            - Required for create operation.
        required: false
        type: str
    description:
        description:
            - Image rate limit policy specification.
        required: false
        type: str
    rate_limit_kbps:
        description:
            - Network bandwidth in KBps that the rate limited image operation can utilize.
            - Required for create operation.
        required: false
        type: int
    cluster_entity_filter:
        description:
            - Category-based entity filter.
            - Required for create operation.
        required: false
        type: dict
        suboptions:
            type:
                description:
                    - The type of filter to apply.
                required: true
                choices:
                    - CATEGORIES_MATCH_ALL
                    - CATEGORIES_MATCH_ANY
                type: str
            category_ext_ids:
                description:
                    - Filter matches entities that have these categories attached.
                required: true
                type: list
                elements: str
author:
 - Abhinav Bansal (@abhinavbansal29)
 - George Ghawali (@george-ghawali)
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Create an image rate limit policy
  nutanix.ncp.ntnx_image_rate_limit_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: my_rate_limit_policy
    description: Rate limit policy for images
    rate_limit_kbps: 1024
    cluster_entity_filter:
      type: CATEGORIES_MATCH_ALL
      category_ext_ids:
        - "d89e250f-8535-4251-8e9d-2a50240f4502"

- name: Update an image rate limit policy
  nutanix.ncp.ntnx_image_rate_limit_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
    name: updated_rate_limit_policy
    rate_limit_kbps: 2048
    cluster_entity_filter:
      type: CATEGORIES_MATCH_ANY
      category_ext_ids:
        - "d89e250f-8535-4251-8e9d-2a50240f4502"
        - "605a0cf9-d04e-3be7-911b-1e6f193f6ebe"

- name: Delete an image rate limit policy
  nutanix.ncp.ntnx_image_rate_limit_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
    state: absent
"""


RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting image rate limit policy
    - If the operation is create or update and C(wait) is true, it will return the image rate limit policy details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
        "cluster_entity_filter": {
            "category_ext_ids": [
                "bbc3555a-133b-5348-9764-bfff196e84e4",
                "e4bda88f-e5da-5eb1-a031-2c0bb00d923d"
            ],
            "type": "CATEGORIES_MATCH_ANY"
        },
        "create_time": "2026-05-24T11:11:31.134515+00:00",
        "description": "ansible_rate_limit_policy_LBZXZWtFgMFT_all_description",
        "ext_id": "f119e0f4-5bf8-4202-af9a-8d82bad400f5",
        "last_update_time": "2026-05-24T11:11:31.134515+00:00",
        "links": null,
        "matching_cluster_ext_ids": null,
        "name": "ansible_rate_limit_policy_LBZXZWtFgMFT_all",
        "owner_ext_id": "00000000-0000-0000-0000-000000000000",
        "owner_name": "admin",
        "rate_limit_kbps": 2048,
        "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the image rate limit policy.
  returned: always
  type: str
  sample: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: false

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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks  # noqa: E402
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
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_image_rate_limit_policy_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_rate_limit_policy  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Returns the module specification.
    """
    entity_filter = dict(
        type=dict(
            type="str",
            required=True,
            choices=["CATEGORIES_MATCH_ALL", "CATEGORIES_MATCH_ANY"],
        ),
        category_ext_ids=dict(type="list", required=True, elements="str"),
    )
    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        rate_limit_kbps=dict(type="int", required=False),
        cluster_entity_filter=dict(
            type="dict", required=False, options=entity_filter, obj=vmm_sdk.Filter
        ),
    )
    return module_args


def create_rate_limit_policy(module, api_instance, result):
    validate_required_params(module, ["rate_limit_kbps", "cluster_entity_filter"])
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.RateLimitPolicy()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create Image Rate Limit Policy Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_rate_limit_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Image Rate Limit Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(
            task, rel=Tasks.RelEntityType.IMAGE_RATE_LIMIT_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            policy = get_rate_limit_policy(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(policy.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Image Rate Limit Policy"
                ),
                msg="Failed to get entity ext_id from task for Image Rate Limit Policy",
            )

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    strip_internal_attributes(current_spec)
    strip_internal_attributes(update_spec)
    if current_spec == update_spec:
        return True
    return False


def update_rate_limit_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_rate_limit_policy(module, api_instance, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Image Rate Limit Policy update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "unable to fetch etag for updating Image Rate Limit Policy", **result
        )

    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.update_rate_limit_policy_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Image Rate Limit Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        updated_policy = get_rate_limit_policy(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(updated_policy.to_dict())
    result["changed"] = True


def delete_rate_limit_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Policy with ext_id:{0} will be deleted.".format(ext_id)
        return

    try:
        resp = api_instance.delete_rate_limit_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Image Rate Limit Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
    }

    api_instance = get_image_rate_limit_policy_api_instance(module)

    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_rate_limit_policy(module, api_instance, result)
        else:
            create_rate_limit_policy(module, api_instance, result)
    else:
        delete_rate_limit_policy(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
