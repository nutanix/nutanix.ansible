#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_profiles_info_v2
short_description: Fetch security profile information
version_added: "2.7.0"
description:
    - This module allows you to fetch information about security profiles in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific security profile.
    - If C(ext_id) is not provided, list multiple security profiles optionally filtered or paginated.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View Security Profile) -
      Required Roles: Prism Admin, Prism Viewer, Security Dashboard Admin, Security Dashboard Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
    ext_id:
        description:
            - External ID of the security profile.
        type: str
        required: false
    expand:
        description:
            - A URL query parameter that allows clients to request related resources.
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch security profile by External ID
  nutanix.ncp.ntnx_security_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "64eae63e-d671-483f-a8bf-e55e426a7168"
  register: result

- name: List security profiles
  nutanix.ncp.ntnx_security_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List security profiles with filter
  nutanix.ncp.ntnx_security_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "clusterExtId eq '64eae63e-d671-483f-a8bf-e55e426a7168'"
  register: result

- name: List security profiles with limit
  nutanix.ncp.ntnx_security_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List all security profiles with fetch_all
  nutanix.ncp.ntnx_security_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC security profiles info v4 API.
        - It can be a single security profile if External ID is provided.
        - List of multiple security profiles if External ID is not provided with optional filter or limit.
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_id": "64eae63e-d671-483f-a8bf-e55e426a7168",
            "ext_id": "64eae63e-d671-483f-a8bf-e55e426a7168",
            "failure_details": null,
            "links": null,
            "tenant_id": null,
            "type": "STANDARD"
        }
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: false
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
ext_id:
    description: The external ID of the security profile.
    type: str
    returned: when External ID is provided
    sample: "64eae63e-d671-483f-a8bf-e55e426a7168"
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Failed generating security profiles info Spec"
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
total_available_results:
    description:
        - The total number of available security profiles in PC.
    type: int
    returned: when all security profiles are fetched
    sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_security_profiles_api_instance,
)
from ..module_utils.v4.security.helpers import (  # noqa: E402
    get_security_profile_by_ext_id,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        expand=dict(type="str"),
    )
    return module_args


def get_security_profile_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_security_profile_by_ext_id(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_security_profiles(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating security profiles info Spec", **result)

    try:
        resp = list_entities(
            api_instance.list_security_profiles,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching security profiles info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_security_profiles_api_instance(module)
    if module.params.get("ext_id"):
        get_security_profile_using_ext_id(module, api_instance, result)
    else:
        get_security_profiles(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
