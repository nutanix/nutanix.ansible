#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_propagated_connectors_v2
short_description: Create and Delete propagated connectors in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Create and Delete propagated connectors in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned
      to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create propagated connector) -
      Required Roles: Super Admin, Prism Admin
    - >-
      B(Delete propagated connector) -
      Required Roles: Super Admin, Prism Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
  state:
    description:
      - State of the propagated connector.
      - If C(state) is C(present) then the module will create propagated connector.
      - If C(state) is C(absent) and C(ext_id) is provided then the module will delete propagated connector.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the propagated connector.
      - Required for delete operation.
    type: str
    required: false
  name:
    description:
      - Name of the propagated identity provider which is used as the connector name.
    type: str
    required: false
  domain_name:
    description:
      - Domain name for the directory service.
    type: str
    required: false
  type:
    description:
      - Type of the login provider configured.
    type: str
    required: false
    choices:
      - LOCAL
      - SAML
      - LDAP
      - CERT
      - SERVICE_ACCOUNT
  entity_id:
    description:
      - Entity identifier of identity provider.
    type: str
    required: false
  project_ext_id:
    description:
      - Project reference for the propagated connector.
    type: str
    required: false
  is_shared_with_all_projects:
    description:
      - Flag indicating whether the propagated connector is shared with all projects or not.
    type: bool
    required: false
  shared_with_projects:
    description:
      - List of projects with which the propagated connector is shared.
    type: list
    elements: str
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
- name: Create propagated connector with all fields
  nutanix.ncp.ntnx_propagated_connectors_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "propagated_connector_ansible"
    domain_name: "example.com"
    type: "SAML"
    entity_id: "https://example.com/entity/123"
    project_ext_id: "00000000-0000-0000-0000-000000000000"
    is_shared_with_all_projects: false
    shared_with_projects:
      - "11111111-1111-1111-1111-111111111111"
  register: result
  ignore_errors: true

- name: Delete propagated connector
  nutanix.ncp.ntnx_propagated_connectors_v2:
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
    - Response for creating or deleting propagated connector.
    - If the operation is create, it will contain the propagated connector details.
    - If the operation is delete, it will contain status of delete operation.
  returned: always
  type: dict
  sample:
    {
      "created_by": "00000000-0000-0000-0000-000000000000",
      "created_time": "2025-06-15T08:34:50.438254+00:00",
      "domain_name": "example.com",
      "entity_id": "https://example.com/entity/123",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "is_shared_with_all_projects": false,
      "last_updated_time": "2025-06-15T08:34:50.438254+00:00",
      "links": null,
      "name": "propagated_connector_ansible",
      "project_ext_id": "00000000-0000-0000-0000-000000000000",
      "shared_with_projects": null,
      "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df",
      "type": "SAML"
    }

ext_id:
  description:
    - The external ID of the propagated connector.
  returned: always
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

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
  sample: "Api Exception raised while creating propagated connector"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_propagated_connectors_api_instance,
)
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
        name=dict(type="str"),
        domain_name=dict(type="str"),
        type=dict(
            type="str",
            choices=[
                "LOCAL",
                "SAML",
                "LDAP",
                "CERT",
                "SERVICE_ACCOUNT",
            ],
        ),
        entity_id=dict(type="str"),
        project_ext_id=dict(type="str"),
        is_shared_with_all_projects=dict(type="bool"),
        shared_with_projects=dict(type="list", elements="str"),
    )
    return module_args


def create_propagated_connectors(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.PropagatedConnector()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create propagated connector spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_propagated_connector(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating propagated connector",
        )
    # Sync API returns entity directly
    if resp and getattr(resp, "data", None) is not None:
        data = resp.data
        # Handle TaskReference case if API returns task
        if hasattr(data, "ext_id") and type(data).__name__ == "TaskReference":
            result["task_ext_id"] = data.ext_id
            result["response"] = strip_internal_attributes(data.to_dict())
        else:
            result["ext_id"] = getattr(data, "ext_id", None)
            result["response"] = strip_internal_attributes(data.to_dict())
    elif resp:
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_propagated_connectors(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Propagated connector with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.delete_propagated_connector_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting propagated connector",
        )
    if resp and getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    elif resp:
        try:
            result["response"] = strip_internal_attributes(resp.to_dict())
        except Exception:
            result["response"] = {}
    else:
        result["response"] = {}
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
        mutually_exclusive=[
            ("is_shared_with_all_projects", "shared_with_projects"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_propagated_connectors_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        create_propagated_connectors(module, result, api_instance)
    else:
        delete_propagated_connectors(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
