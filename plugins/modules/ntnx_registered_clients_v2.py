#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_registered_clients_v2
short_description: Create and update registered clients
version_added: "2.7.0"
description:
    - Create and update registered clients in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present) and C(ext_id) is not provided, the module will create a new registered client.
            - If C(state) is C(present) and C(ext_id) is provided, the module will update the existing registered client.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external ID of the registered client.
            - Required for updating the registered client.
        type: str
        required: false
    name:
        description:
            - Unique name of the client.
            - Required for create operation.
        type: str
        required: false
    display_name:
        description:
            - UI name of the client.
            - Required for create operation.
        type: str
        required: false
    description:
        description:
            - Description of the client.
        type: str
        required: false
    deployment_list:
        description:
            - Deployment List related to the client.
        type: list
        elements: str
        required: false
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: false
        default: true
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
- name: Create a registered client
  nutanix.ncp.ntnx_registered_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "ansible_test_client"
    display_name: "AnsibleTestClient"
    description: "Client created by Ansible"
    deployment_list:
      - "onPrem"
  register: result
  ignore_errors: true

- name: Update a registered client
  nutanix.ncp.ntnx_registered_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "21bc5e8e-5854-5bd4-8dcc-924f24b0ddf4"
    name: "ansible_test_client_updated"
    display_name: "AnsibleTestClientUpdated"
    description: "Updated client description"
    deployment_list:
      - "onPrem"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or updating registered client.
    - If the operation is create, it will contain the registered client details after creation.
    - If the operation is update, it will contain the registered client details after update.
  returned: always
  type: dict
   sample:
    {
      "created_by": null,
      "created_time": "2026-10-14T07:25:50.338347+00:00",
      "deployment_list": [
        "onPrem"
      ],
      "description": "description",
      "display_name": "CatalogService",
      "ext_id": "1b214b08-275a-4753-62a1-53c2501f999e",
      "last_updated_time": "2026-10-14T07:25:50.338347+00:00",
      "links": null,
      "name": "CatalogService",
      "tenant_id": null
    }
 ext_id:
   description:
     - The external ID of the registered client.
   returned: always
   type: str
   sample: "1b214b08-275a-4753-62a1-53c2501f999e"
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
skipped:
  description: This indicates whether the task was skipped
  returned: when module is idempotent
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
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while creating registered client"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_registered_client_api_instance,
)
from ..module_utils.v4.iam.helpers import get_registered_client  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as iam_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as iam_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        display_name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        deployment_list=dict(type="list", elements="str", required=False),
    )
    return module_args


def check_registered_client_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)
    # Normalize deployment_list ordering for comparison
    for spec in (old_spec, update_spec):
        dl = spec.get("deployment_list")
        if dl:
            spec["deployment_list"] = sorted(dl)
    return old_spec == update_spec


def create_registered_client(module, result, api_instance):
    validate_required_params(module, ["name", "display_name"])
    sg = SpecGenerator(module)
    default_spec = iam_sdk.Client()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create registered client spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_registered_client(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating registered client",
        )

    # Create returns Message, not entity. Try to get ext_id from response or via list.
    # First, set response to Message payload
    try:
        result["response"] = strip_internal_attributes(resp.to_dict())
        # Try to extract data message
        if hasattr(resp, "data") and resp.data:
            data_dict = strip_internal_attributes(resp.data.to_dict())
            result["response"] = data_dict
    except Exception:
        result["response"] = (
            strip_internal_attributes(resp.to_dict())
            if hasattr(resp, "to_dict")
            else {}
        )

    # Try to resolve ext_id by listing with name filter
    ext_id = None
    try:
        # Look for newly created client by name via list API
        sg2 = SpecGenerator(module)
        kwargs, err2 = sg2.get_info_spec(
            attr={"filter": "name eq '{0}'".format(module.params.get("name"))}
        )
        if not err2:
            list_resp = list_entities(
                api_instance.list_registered_clients, kwargs=kwargs
            )
            list_data = strip_internal_attributes(list_resp.to_dict()).get("data") or []
            # Find matching name
            for item in list_data:
                if item.get("name") == module.params.get("name"):
                    ext_id = item.get("ext_id")
                    result["ext_id"] = ext_id
                    result["response"] = item
                    break
    except Exception:
        pass

    # Fallback: if ext_id still not found, try to use name filter result's first entry
    if not ext_id:
        # Keep Message as response, but set ext_id if we can parse
        result["ext_id"] = None

    result["changed"] = True


def update_registered_client(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_registered_client(module, api_instance, ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating registered client update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_registered_client_idempotency(
        current_spec.to_dict(), update_spec.to_dict()
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating registered client", **result
        )
    kwargs = {"if_match": etag}

    try:
        resp = api_instance.update_registered_client_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating registered client",
        )

    # Update returns Message; re-fetch entity for response
    try:
        updated = get_registered_client(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(updated.to_dict())
    except Exception:
        # Fallback to Message response
        try:
            result["response"] = strip_internal_attributes(resp.data.to_dict())
        except Exception:
            result["response"] = (
                strip_internal_attributes(resp.to_dict())
                if hasattr(resp, "to_dict")
                else {}
            )

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[("state", "present", ("name", "ext_id"), True)],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}

    api_instance = get_registered_client_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_registered_client(module, result, api_instance)
        else:
            create_registered_client(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
