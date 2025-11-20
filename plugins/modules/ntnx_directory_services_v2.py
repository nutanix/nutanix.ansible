#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_directory_services_v2
short_description: Module to create, update and delete directory services in Nutanix PC.
version_added: "2.0.0"
description:
    - This module is used to create, update and delete directory services in Nutanix PC.
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - State of the directory service. Whether to create, update, or delete.
            - If C(state) is C(present) and C(ext_id) is not provided, create a new directory service.
            - If C(state) is C(present) and C(ext_id) is provided, update the directory service.
            - If C(state) is C(absent), it will delete the directory service with the given External ID.
        type: str
        choices: ['present', 'absent']
    ext_id:
        description:
            - External ID of the Directory Service.
            - Required for updating or deleting the Directory Service.
        required: false
        type: str
    name:
        description:
            - Name for the Directory Service.
            - Required for creating directory service.
        type: str
    url:
        description:
            - URL for the Directory Service.
            - Required for creating directory service.
        type: str
    secondary_urls:
        description:
            - Secondary URL for the Directory Service.
        required: false
        type: list
        elements: str
    domain_name:
        description:
            - Domain name for the Directory Service.
            - Required for creating directory service.
        type: str
    directory_type:
        description:
            - Type of Directory Service.
        choices: ['ACTIVE_DIRECTORY', 'OPEN_LDAP']
        type: str
    service_account:
        description:
            - Information of Service account to connect to the Directory Service.
            - Required for creating directory service.
        type: dict
        suboptions:
            username:
                description:
                    - Username to connect to the Directory Service.
                type: str
            password:
                description:
                    - Password to connect to the Directory Service.
                    - If provided, idempotency check will be skipped.
                type: str
    open_ldap_configuration:
        description:
            - Configuration for OpenLDAP Directory Service.
        required: false
        type: dict
        suboptions:
            user_configuration:
                description:
                    - User configuration for OpenLDAP Directory Service.
                type: dict
                suboptions:
                    user_object_class:
                        description:
                            - Object class in the OpenLDAP system that corresponds to Users.
                        type: str
                    user_search_base:
                        description:
                            - Base DN for User search.
                        type: str
                    username_attribute:
                        description:
                            - Unique Identifier for each User which can be used in Authentication.
                        type: str
            user_group_configuration:
                description:
                    - User Group configuration for OpenLDAP Directory Service.
                type: dict
                suboptions:
                    group_object_class:
                        description:
                            - Object class in the OpenLDAP system that corresponds to groups.
                        type: str
                    group_search_base:
                        description:
                            - Base DN for group search.
                        type: str
                    group_member_attribute:
                        description:
                            - Attribute in a group that associates Users to the group.
                        type: str
                    group_member_attribute_value:
                        description:
                            - User attribute value that will be used in group entity to associate User to the group.
                        type: str
    group_search_type:
        description:
            - Group membership search type for the Directory Service.
        required: false
        choices: ['NON_RECURSIVE', 'RECURSIVE']
        type: str
    white_listed_groups:
        description:
            - List of allowed User Groups for the Directory Service.
        required: false
        type: list
        elements: str
    wait:
        description:
            - Wait for the operation to complete.
            - it is not supported here as this module does not have task polling required.
        type: bool
        required: false
        default: True
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger
author:
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create ACTIVE_DIRECTORY service
  nutanix.ncp.ntnx_directory_services_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: directory_service_name
    url: ldap://10.0.0.0:389
    directory_type: "ACTIVE_DIRECTORY"
    domain_name: "nutanix"
    service_account:
      username: admin
      password: Nutanix@123456
  register: result

- name: Update ACTIVE_DIRECTORY service
  nutanix.ncp.ntnx_directory_services_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"
    name: directory_service_name
    url: ldap://10.0.0.0:389
    directory_type: "ACTIVE_DIRECTORY"
    domain_name: "nutanix"
    service_account:
      username: admin
      password: Nutanix@123456
    white_listed_groups:
      - test_group_updated
  register: result

- name: Delete ACTIVE_DIRECTORY service
  nutanix.ncp.ntnx_directory_services_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"
  register: result
"""
RETURN = r"""
response:
    description:
        - Response for creating, updating or deleting directory services.
        - Directory service details in case of creating or updating directory service.
        - None in case of deleting directory service.
    type: dict
    returned: always
    sample:
        {
            "created_by": "00000000-0000-0000-0000-000000000000",
            "created_time": "2024-07-02T05:34:25.878533+00:00",
            "directory_type": "ACTIVE_DIRECTORY",
            "domain_name": "nutanix",
            "ext_id": "075b79bb-fc36-5cdd-9296-0b141d531266",
            "group_search_type": "NON_RECURSIVE",
            "last_updated_time": "2024-07-02T05:34:25.878533+00:00",
            "links": null,
            "name": "stxRVGlcSTMhansible-ag",
            "open_ldap_configuration": null,
            "secondary_urls": null,
            "service_account": {
                "password": "****",
                "username": "nutanix@email.com"
            },
            "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df",
            "url": "ldap://10.0.0.2:485",
            "white_listed_groups": [
                "test_updated"
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

ext_id:
  description: External ID of the Directory Service
  returned: always
  type: str
  sample: "075b79bb-fc36-5cdd-9296-0b141d531266"

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: String containing any message from module.
  returned: always
  type: str
  sample: "Directory Service with ext_id: 075b79bb-fc36-5cdd-9296-0b141d531266 deleted successfully"
"""


import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_directory_service_api_instance,
    get_etag,
)
from ..module_utils.v4.iam.helpers import get_directory_service  # noqa: E402
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
    account_spec = dict(
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )

    user_config_spec = dict(
        user_object_class=dict(type="str"),
        user_search_base=dict(type="str"),
        username_attribute=dict(type="str"),
    )

    user_group_config_spec = dict(
        group_object_class=dict(type="str"),
        group_search_base=dict(type="str"),
        group_member_attribute=dict(type="str"),
        group_member_attribute_value=dict(type="str"),
    )

    open_ldap_config_spec = dict(
        user_configuration=dict(
            type="dict", options=user_config_spec, obj=iam_sdk.UserConfiguration
        ),
        user_group_configuration=dict(
            type="dict",
            options=user_group_config_spec,
            obj=iam_sdk.UserGroupConfiguration,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        url=dict(type="str"),
        secondary_urls=dict(type="list", elements="str"),
        domain_name=dict(type="str"),
        directory_type=dict(type="str", choices=["ACTIVE_DIRECTORY", "OPEN_LDAP"]),
        service_account=dict(
            type="dict", options=account_spec, obj=iam_sdk.DsServiceAccount
        ),
        open_ldap_configuration=dict(
            type="dict", options=open_ldap_config_spec, obj=iam_sdk.OpenLdapConfig
        ),
        group_search_type=dict(type="str", choices=["NON_RECURSIVE", "RECURSIVE"]),
        white_listed_groups=dict(type="list", elements="str"),
    )
    return module_args


def create_directory_service(module, directory_services, result):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.DirectoryService()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create directory services spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = directory_services.create_directory_service(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating directory service",
        )

    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def check_directory_services_idempotency(old_spec, update_spec):
    if old_spec != update_spec:
        return False

    return True


def update_directory_service(module, directory_services, result):

    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_directory_service(module, directory_services, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating directory services update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    # check for idempotency
    if not module.params.get("service_account", {}).get("password"):
        if check_directory_services_idempotency(
            current_spec.to_dict(), update_spec.to_dict()
        ):
            result["skipped"] = True
            module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = directory_services.update_directory_service_by_id(
            extId=ext_id, body=update_spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating directory service",
        )
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    result["changed"] = True


def delete_directory_service(module, directory_services, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_directory_service(module, directory_services, ext_id=ext_id)

    if module.check_mode:
        result["msg"] = "Directory service with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "unable to fetch etag for deleting directory service", **result
        )

    kwargs = {"if_match": etag}
    try:
        resp = directory_services.delete_directory_service_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting directory service",
        )

    result["changed"] = True
    if resp is None:
        result["msg"] = "Directory Service with ext_id: {} deleted successfully".format(
            ext_id
        )
    else:
        result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
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
    directory_services = get_directory_service_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_directory_service(module, directory_services, result)
        else:
            create_directory_service(module, directory_services, result)
    else:
        delete_directory_service(module, directory_services, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
