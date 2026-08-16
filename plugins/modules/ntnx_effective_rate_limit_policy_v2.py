#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_effective_rate_limit_policy_v2
short_description: Create, Update, Delete image rate limit policies in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete image rate limit policies in Nutanix Prism Central.
  - An image rate limit policy throttles the bandwidth (in Kbps) that image
    upload / checkout / placement operations can consume on the clusters that
    match its C(cluster_entity_filter).
  - When multiple rate limit policies match the same cluster, Prism Central
    resolves an B(EffectiveRateLimitPolicy) (see
    M(nutanix.ncp.ntnx_vm_effective_rate_limit_policies_info_v2)) that enforces
    the lowest configured limit.
  - This module uses PC v4 APIs based SDKs.
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create an image rate limit policy.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the image rate limit policy.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the image rate limit policy.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the image rate limit policy.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the image rate limit policy.
      - Required for the create operation.
      - Minimum 1, maximum 256 characters.
    type: str
    required: false
  description:
    description:
      - Description of the image rate limit policy.
    type: str
    required: false
  rate_limit_kbps:
    description:
      - The bandwidth (in Kbps) that image operations are allowed to consume on
        matching clusters.
      - Required for the create operation.
      - Must be a positive integer.
    type: int
    required: false
  cluster_entity_filter:
    description:
      - Category-based filter that selects the clusters (Prism Elements) on
        which this rate limit policy is enforced.
      - Required for the create operation.
    type: dict
    required: false
    suboptions:
      type:
        description:
          - Match type used to combine C(category_ext_ids).
        type: str
        required: true
        choices:
          - CATEGORIES_MATCH_ALL
          - CATEGORIES_MATCH_ANY
      category_ext_ids:
        description:
          - List of category external identifiers that identify the clusters on
            which this policy applies.
        type: list
        elements: str
        required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation. The required roles depend on the operation
    being performed.
  - >-
    B(Create an Image Rate Limit Policy) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Update an Image Rate Limit Policy) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Delete an Image Rate Limit Policy) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create image rate limit policy
  nutanix.ncp.ntnx_effective_rate_limit_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "image_rate_limit_policy_ansible"
    description: "Image rate limit policy created by Ansible"
    rate_limit_kbps: 1024
    cluster_entity_filter:
      type: CATEGORIES_MATCH_ANY
      category_ext_ids:
        - "b1a1c07c-6b8a-4b0a-8f27-7d3c9df20e6a"
  register: result
  ignore_errors: true

- name: Update image rate limit policy
  nutanix.ncp.ntnx_effective_rate_limit_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "image_rate_limit_policy_ansible_updated"
    description: "Updated image rate limit policy description"
    rate_limit_kbps: 2048
    cluster_entity_filter:
      type: CATEGORIES_MATCH_ALL
      category_ext_ids:
        - "b1a1c07c-6b8a-4b0a-8f27-7d3c9df20e6a"
  register: result
  ignore_errors: true

- name: Delete image rate limit policy
  nutanix.ncp.ntnx_effective_rate_limit_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting the image rate limit policy.
    - If the operation is create or update and C(wait) is true, it will return the image rate limit policy details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "cluster_entity_filter": {
          "category_ext_ids": [
              "b1a1c07c-6b8a-4b0a-8f27-7d3c9df20e6a"
          ],
          "type": "CATEGORIES_MATCH_ANY"
      },
      "create_time": "2026-07-21T12:34:56.000000+00:00",
      "description": "Image rate limit policy created by Ansible",
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "last_update_time": "2026-07-21T12:34:56.000000+00:00",
      "links": null,
      "matching_cluster_ext_ids": [
          "000647b8-ddb3-6bbb-0000-000000028f57"
      ],
      "name": "image_rate_limit_policy_ansible",
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "owner_name": "admin",
      "rate_limit_kbps": 1024,
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
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
  returned: When the operation is skipped due to idempotency.
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "EffectiveRateLimitPolicy with name 'image_rate_limit_policy_ansible' already exists. Skipping creation."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
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
from ..module_utils.v4.vmm.helpers import get_image_rate_limit_policy  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Read-only server-populated fields that must be scrubbed before an update PUT.
_RATE_LIMIT_POLICY_READ_ONLY_FIELDS = (
    "create_time",
    "last_update_time",
    "owner_ext_id",
    "owner_name",
    "matching_cluster_ext_ids",
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Return the argument spec for the ntnx_effective_rate_limit_policy_v2 module.
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
            type="dict",
            required=False,
            options=entity_filter,
            obj=virtual_machine_management_sdk.Filter,
        ),
    )
    return module_args


def find_rate_limit_policy_by_name(module, api_instance, name):
    """
    Return the first image rate limit policy matching ``name`` or ``None`` if
    no policy with that name exists. Used for pre-create idempotency.
    """
    try:
        resp = api_instance.list_rate_limit_policies(
            _filter="name eq '{0}'".format(name)
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while checking existing image rate limit policies for idempotency",
        )
    data = getattr(resp, "data", None) or []
    for item in data:
        if getattr(item, "name", None) == name:
            return item
    return None


def create_EffectiveRateLimitPolicy(module, result, api_instance):
    """
    Create an image rate limit policy.
    """
    validate_required_params(
        module, ["name", "rate_limit_kbps", "cluster_entity_filter"]
    )

    name = module.params.get("name")
    existing = find_rate_limit_policy_by_name(module, api_instance, name)
    if existing is not None:
        result["skipped"] = True
        result["ext_id"] = getattr(existing, "ext_id", None)
        result["response"] = strip_internal_attributes(existing.to_dict())
        result["msg"] = (
            "EffectiveRateLimitPolicy with name '{0}' already exists. "
            "Skipping creation.".format(name)
        )
        return

    sg = SpecGenerator(module)
    default_spec = virtual_machine_management_sdk.RateLimitPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create Image Rate Limit Policy spec", **result
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
        result["response"] = strip_internal_attributes(task.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task, rel=TASK_CONSTANTS.RelEntityType.IMAGE_RATE_LIMIT_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            policy = get_image_rate_limit_policy(module, api_instance, ext_id)
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


def _canonicalize_for_diff(policy_dict):
    """
    Return a normalized copy of a RateLimitPolicy dict suitable for equality
    comparison: internal attributes and read-only fields removed and any
    ``category_ext_ids`` list sorted (the API does not preserve insertion
    order, so an unsorted compare would falsely report drift).
    """
    canonical = strip_internal_attributes(deepcopy(policy_dict))
    for field in _RATE_LIMIT_POLICY_READ_ONLY_FIELDS:
        canonical.pop(field, None)
    cluster_filter = canonical.get("cluster_entity_filter") or {}
    category_ext_ids = cluster_filter.get("category_ext_ids")
    if isinstance(category_ext_ids, list):
        cluster_filter["category_ext_ids"] = sorted(category_ext_ids)
    return canonical


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """
    Compare current and desired specs and return True when nothing meaningful
    changes. Read-only fields are stripped and list-valued fields are
    canonicalized (sorted) before the compare.
    """
    return _canonicalize_for_diff(old_spec_dict) == _canonicalize_for_diff(
        update_spec_dict
    )


def _remove_read_only_attributes(spec):
    """
    Clear server-populated read-only fields on the update spec before sending
    the PUT. The SDK exposes these as properties without deleters, so we set
    them to ``None`` (which the serializer subsequently omits from the body).
    """
    for field in _RATE_LIMIT_POLICY_READ_ONLY_FIELDS:
        if hasattr(spec, field):
            setattr(spec, field, None)


def update_EffectiveRateLimitPolicy(module, result, api_instance):
    """
    Update an existing image rate limit policy identified by ``ext_id``.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(
        module, ["name", "rate_limit_kbps", "cluster_entity_filter"]
    )

    current_spec = get_image_rate_limit_policy(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for updating Image Rate Limit Policy", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update Image Rate Limit Policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    _remove_read_only_attributes(update_spec)

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
        updated = get_image_rate_limit_policy(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(updated.to_dict())
    result["changed"] = True


def delete_EffectiveRateLimitPolicy(module, result, api_instance):
    """
    Delete an image rate limit policy identified by ``ext_id``.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Image Rate Limit Policy with ext_id:{0} will be deleted.".format(ext_id)
        )
        return

    current_spec = get_image_rate_limit_policy(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for deleting Image Rate Limit Policy", **result
        )

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.delete_rate_limit_policy_by_id(extId=ext_id, **kwargs)
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
        task_status = wait_for_completion(module, task_ext_id, raise_error=True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    """
    Ansible module entry point. Dispatches Create / Update / Delete based on
    ``state`` and the presence of ``ext_id``.
    """
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_image_rate_limit_policy_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_EffectiveRateLimitPolicy(module, result, api_instance)
        else:
            create_EffectiveRateLimitPolicy(module, result, api_instance)
    else:
        delete_EffectiveRateLimitPolicy(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
