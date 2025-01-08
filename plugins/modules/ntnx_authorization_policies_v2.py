#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: ntnx_authorization_policies_v2
short_description: Manage Nutanix PC IAM authorization policies
description:
    - This module allows you to create, update, and delete authorization policies in Nutanix PC.
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
options:
    state:
        description:
            - If C(state) is C(present) and C(ext_id) is not provided, create a new authorization policy.
            - If C(state) is C(present) and C(ext_id) is provided, update the authorization policy.
            - If C(state) is C(absent), it will delete the authorization policy with the given External ID.
        type: str
        choices: ['present', 'absent']
    ext_id:
        description:
            - Role External ID.
            - Required for updating or deleting the auth policy.
        type: str
        required: false
    display_name:
        description:
            - The display name for the Authorization Policy.
        required: false
        type: str
    description:
        description:
            - Description of the Authorization Policy.
        required: false
        type: str
    identities:
        description:
            - List of expressions representing identities for access to given entities.
            - During update, the identities are replaced with the new given identities.
            - Check examples for more information.
        required: false
        type: list
        elements: dict
    entities:
        description:
            - List of expressions representing entities access to identities.
            - During update, the entities are replaced with the new given entities.
        required: false
        type: list
        elements: dict
    role:
        description:
            - The Role associated with the Authorization Policy
        required: false
        type: str
    authorization_policy_type:
        description:
            - Type of Authorization Policy.
        required: false
        type: str
        choices:
            - USER_DEFINED
        default: USER_DEFINED
    wait:
        description:
            - Wait for the task to complete.
            - Not supported for this module.
        required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
  - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: Create auth policy with access to images, certain directory service and self owned marketplace items
  nutanix.ncp.ntnx_authorization_policies_v2:
    nutanix_host: "{{ nutanix_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: present
    display_name: "ansible-created-acp"
    description: "ansible created acps"
    role: "ebbfbd38-122b-5529-adcc-dcb6b4177382"
    authorization_policy_type: "USER_DEFINED"
    entities:
      - "images":
          "*":
            "eq": "*"
      - "directory_service":
          "uuid":
            "anyof":
              - "ebbfbd38-794b-5529-adcc-dcb6b4177382"
              - "ebbfbd38-794b-5529-adcc-dcb6b4177383"
      - "marketplace_item":
          "owner_uuid":
            "eq": "SELF_OWNED"
    identities:
      - "user":
          "uuid":
            "anyof":
              - "ebbfbd38-794b-5529-adcc-dcb6b4177384"
              - "ebbfbd38-794b-5529-adcc-dcb6b4177385"
      - "user":
          "group":
            "anyof":
              - "ebbfbd38-794b-5529-adcc-dcb6b4177386"
              - "ebbfbd38-794b-5529-adcc-dcb6b4177387"
  register: result
  ignore_errors: true

- name: Create a basic auth policy with access to all images
  nutanix.ncp.ntnx_authorization_policies_v2:
    nutanix_host: "{{ nutanix_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: present
    display_name: "acp1"
    role: "ebb123232-794b-5529-adcc-dcb6b4137384"
    entities:
      - "images":
          "*":
            "eq": "*"
    identities:
      - "user":
          "group":
            "anyof":
              - "<user group uuid>"
  register: result
  ignore_errors: true

- name: Update access to users and remove access of user groups
  nutanix.ncp.ntnx_authorization_policies_v2:
    nutanix_host: "{{ nutanix_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: present
    ext_id: "ebbfbd38-794b-5529-adcc-dcb6b4137384"
    identities:
      - "user":
          "uuid":
            "anyof":
              - "ebbfbd38-794b-1529-adcc-dcb6b4177384"
              - "ebbfbd38-794b-5521-adcc-dcb6b4177384"
  register: result
  ignore_errors: true

- name: delete auth policy
  nutanix.ncp.ntnx_authorization_policies_v2:
    nutanix_host: "{{ nutanix_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: absent
    ext_id: "ebbfbd38-794b-5529-adcc-dcb6b4137384"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description: Authorization policy current state spec
  returned: always
  type: dict
  sample:
        {
                "authorizationPolicyType": "PREDEFINED_READ_ONLY",
                "clientName": "",
                "createdBy": "",
                "createdTime": "2024-03-20T09:54:34.846946Z",
                "description": "",
                "displayName": "Super Admin_acp",
                "entities": [
                    {
                        "$reserved": {
                            "*": {
                                "*": {
                                    "eq": "*"
                                }
                            }
                        }
                    }
                ],
                "extId": "00000000-0000-0000-0000-000000000000",
                "identities": [
                    {
                        "$reserved": {
                            "user": {
                                "uuid": {
                                    "anyof": [
                                        "00000000-0000-0000-0000-000000000000"
                                    ]
                                }
                            }
                        }
                    }
                ],
                "isSystemDefined": true,
                "lastUpdatedTime": "2024-03-20T09:54:34.846946Z",
                "role": "00000000-0000-0000-0000-000000000000"
            }
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
ext_id:
  description: authorization policy external id
  returned: always
  type: str
  sample: "00001000-0000-0000-0000-000000000000"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_authorization_policy_api_instance,
    get_etag,
)
from ..module_utils.v4.iam.helpers import get_authorization_policy  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as iam_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as iam_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        display_name=dict(type="str"),
        description=dict(type="str"),
        identities=dict(type="list", elements="dict"),
        entities=dict(type="list", elements="dict"),
        role=dict(type="str"),
        authorization_policy_type=dict(
            type="str",
            choices=["USER_DEFINED"],
            default="USER_DEFINED",
        ),
    )
    return module_args


def create_entities_spec(entities):
    entities_spec = []
    for entity in entities:
        entity_spec = iam_sdk.EntityFilter(entity_filter=entity)
        entities_spec.append(entity_spec)
    return entities_spec


def create_identities_spec(identities):
    identities_spec = []
    for identity in identities:
        identity_spec = iam_sdk.IdentityFilter(identity_filter=identity)
        identities_spec.append(identity_spec)
    return identities_spec


def create_authorization_policy(module, result):
    authorization_policies = get_authorization_policy_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = iam_sdk.AuthorizationPolicy()
    spec, err = sg.generate_spec(obj=default_spec)

    # handling identities and entities spec creation separately as their dicts are to be passed in $reserved
    identities = module.params.get("identities")
    if identities:
        spec.identities = create_identities_spec(identities)
    entities = module.params.get("entities")
    if entities:
        spec.entities = create_entities_spec(entities)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create authorization policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = authorization_policies.create_authorization_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating authorization policy",
        )

    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    result["changed"] = True


def check_authorization_policies_idempotency(old_spec, update_spec):
    if old_spec == update_spec:
        return True
    return False


def update_authorization_policy(module, result):
    authorization_policies = get_authorization_policy_api_instance(module)

    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_authorization_policy(
        module, authorization_policies, ext_id=ext_id
    )
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating authorization policy update spec", **result
        )

    # handling identities and entities spec creation separately as their dicts are to be passed in $reserved
    identities = module.params.get("identities")
    if identities:
        update_spec.identities = create_identities_spec(identities)
    entities = module.params.get("entities")
    if entities:
        update_spec.entities = create_entities_spec(entities)
    # check for idempotency
    if check_authorization_policies_idempotency(
        strip_internal_attributes(current_spec.to_dict()),
        strip_internal_attributes(update_spec.to_dict()),
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = authorization_policies.update_authorization_policy_by_id(
            extId=ext_id, body=update_spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating authorization policy",
        )

    if getattr(resp.data, "severity", None) == "ERROR":
        result["error"] = resp.data.message
        msg = "Failed to update authorization policy"
        module.fail_json(msg=msg, **result)

    resp = get_authorization_policy(module, authorization_policies, ext_id=ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_authorization_policy(module, result):
    authorization_policies = get_authorization_policy_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_authorization_policy(
        module, authorization_policies, ext_id=ext_id
    )

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting authorization policy", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = authorization_policies.delete_authorization_policy_by_id(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting authorization policy",
        )

    result["changed"] = True
    if resp is None:
        result[
            "msg"
        ] = "Authorization policy with ext_id: {} deleted successfully".format(ext_id)
    else:
        result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            (
                "state",
                "present",
                ("display_name", "identities", "entities", "role"),
                True,
            ),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_authorization_policy(module, result)
        else:
            create_authorization_policy(module, result)
    else:
        delete_authorization_policy(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
