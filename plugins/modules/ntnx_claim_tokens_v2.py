#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_claim_tokens_v2
short_description: Create, Update, Delete Foundation Central claim tokens
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Foundation Central claim tokens.
  - A claim token is a secure token used for node authentication and registration with
    Foundation Central during onboarding.
  - This module uses the Life Cycle Management (lifecycle) v4 APIs based SDK.
notes:
  - This module talks to B(Foundation Central (FCVM)), not Prism Central.
    Point C(nutanix_host) and C(nutanix_port) at the Foundation Central VM endpoint.
  - >-
    This module requires the appropriate Foundation Central role/permissions to be assigned
    to the user performing the operation.
  - B(Create a claim token) - Requires an admin role on Foundation Central.
    C(name), C(expiry_time) and C(max_usage_count) are all required on create.
  - The C(expiry_time) must be at most 3 months in the future.
  - B(Update a claim token) - Requires an admin role on Foundation Central.
  - B(Delete a claim token) - Requires an admin role on Foundation Central.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create claim token.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update claim token.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete claim token.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the claim token.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the claim token.
      - Required for create operation.
    type: str
    required: false
  expiry_time:
    description:
      - The expiry time of the claim token in ISO 8601 format (e.g. C(2026-11-01T00:00:00Z)).
      - After this time the claim token can no longer be used to register nodes.
      - Required for create operation.
      - The expiry time validity must be at most 3 months in the future, otherwise Foundation Central rejects the request.
    type: str
    required: false
  max_usage_count:
    description:
      - The maximum number of times this claim token can be used to register nodes.
      - Required for create operation.
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
- name: Create claim token
  nutanix.ncp.ntnx_claim_tokens_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "claim_token_ansible"
    expiry_time: "2026-11-01T00:00:00Z"
    max_usage_count: 5
  register: result
  ignore_errors: true

- name: Update claim token
  nutanix.ncp.ntnx_claim_tokens_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "claim_token_ansible_updated"
    expiry_time: "2026-12-01T00:00:00Z"
    max_usage_count: 10
  register: result
  ignore_errors: true

- name: Delete claim token
  nutanix.ncp.ntnx_claim_tokens_v2:
    nutanix_host: "{{ foundation_central_host }}"
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
    - Response for creating, updating, or deleting a claim token.
    - If the operation is create or update and C(wait) is true, it will return the claim token details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "created_time": "2026-09-08T06:29:30.183575+00:00",
      "current_usage_count": 0,
      "expiry_time": "2026-11-01T00:00:00+00:00",
      "ext_id": "5b3a0229-c34b-40e1-92be-216f5256666b",
      "links": null,
      "max_usage_count": 5,
      "name": "claim_token_ansible",
      "owner_ext_id": "7cb3e9ea-7815-4d1a-9c1e-4e3a9277c17b",
      "tenant_id": "703c7c79-5e87-4813-a137-76c09b808db9"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the claim token.
  returned: always
  type: str
  sample: "5b3a0229-c34b-40e1-92be-216f5256666b"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency.
  returned: when applicable
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
  sample: "Api Exception raised while creating claim token"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402
from datetime import datetime, timezone  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_claim_tokens_api_instance,
    get_etag,
)
from ..module_utils.v4.lcm.helpers import get_claim_token  # noqa: E402
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
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        expiry_time=dict(type="str"),
        max_usage_count=dict(type="int"),
    )
    return module_args


def create_claim_tokens(module, result, api_instance):
    validate_required_params(module, ["name", "expiry_time", "max_usage_count"])
    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.ClaimToken()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create claim token spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_claim_token(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating claim token",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
        ext_id = get_entity_ext_id_from_task(task_resp)
        if ext_id:
            result["ext_id"] = ext_id
            claim_token = get_claim_token(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(claim_token.to_dict())
    result["changed"] = True


def _normalize_expiry_time(value):
    """Normalize an expiry_time value (datetime or ISO 8601 str) to a
    timezone-aware datetime for reliable idempotency comparison."""
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value)
        # Support the trailing 'Z' (UTC) designator used in examples/tests.
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(text)
        except ValueError:
            return value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def check_claim_token_idempotency(current_spec, update_spec):
    current = deepcopy(current_spec)
    update = deepcopy(update_spec)
    current["expiry_time"] = _normalize_expiry_time(current.get("expiry_time"))
    update["expiry_time"] = _normalize_expiry_time(update.get("expiry_time"))
    return current == update


def update_claim_tokens(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_obj = get_claim_token(module, api_instance, ext_id)
    etag = get_etag(current_obj)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating claim token", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_obj))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update claim token spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_claim_token_idempotency(current_obj.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_claim_token_by_id(
            extId=ext_id, body=update_spec, if_match=etag
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating claim token",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        claim_token = get_claim_token(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(claim_token.to_dict())
    result["changed"] = True


def delete_claim_tokens(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Claim token with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_claim_token_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting claim token",
        )

    task_ext_id = getattr(resp.data, "ext_id", None) if resp and resp.data else None
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
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
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "task_ext_id": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_claim_tokens_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_claim_tokens(module, result, api_instance)
        else:
            create_claim_tokens(module, result, api_instance)
    else:
        delete_claim_tokens(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
