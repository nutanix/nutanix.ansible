#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_directory_services_info_v2
short_description: Fetch directory services info
version_added: 2.0.0
description:
    - This module is used to fetch directory services.
    - Fetch a directory service using ext_id or multiple directory services.
options:
    ext_id:
        description:
            - directory service external ID.
            - If used, only the directory service with the specified external ID will be fetched.
              Else, multiple directory services will be fetched as per query params.
        required: false
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: List all directory services
  nutanix.ncp.ntnx_directory_services_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Fetch directory service by ext_id
  nutanix.ncp.ntnx_directory_services_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"
  register: result

- name: List all directory services with filter
  nutanix.ncp.ntnx_directory_services_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'directory_service_name'"
  register: result
"""
RETURN = r"""
response:
    description:
        - Response for fetching directory services.
        - Returns directory service info using directory service external ID or list of directory services.
    type: dict
    returned: always
    sample:
        {
            "created_by": "00000000-0000-0000-0000-000000000000",
            "created_time": "2024-05-29T08:34:50.438254+00:00",
            "directory_type": "ACTIVE_DIRECTORY",
            "domain_name": "nutanix",
            "ext_id": "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a",
            "group_search_type": "NON_RECURSIVE",
            "last_updated_time": "2024-05-29T13:10:40.771273+00:00",
            "links": null,
            "name": "qa_nucalm_io",
            "open_ldap_configuration": null,
            "secondary_urls": null,
            "service_account": {
                "password": "****",
                "username": "admin@email.com"
            },
            "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df",
            "url": "ldap://10.0.0.1:256",
            "white_listed_groups": [
                "cn=group1,cn=users_test,dc=nutanix",
                "cn=group2,cn=users_test,dc=nutanix",
                "cn=group3,cn=users_test,dc=nutanix"
            ]
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

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_directory_service_api_instance,
)
from ..module_utils.v4.iam.helpers import get_directory_service  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_directory_service_by_ext_id(module, directory_services, result):
    ext_id = module.params.get("ext_id")
    resp = get_directory_service(module, directory_services, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_directory_services(module, directory_services, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating directory services info Spec", **result)

    try:
        resp = directory_services.list_directory_services(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching directory services info",
        )

    resp = strip_internal_attributes(resp.to_dict()).get("data")
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
    result = {"changed": False, "error": None, "response": None}
    directory_services = get_directory_service_api_instance(module)
    if module.params.get("ext_id"):
        get_directory_service_by_ext_id(module, directory_services, result)
    else:
        get_directory_services(module, directory_services, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
