#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_directory_server_config_v2
short_description: Create, Update, Delete directory server config
version_added: 2.6.0
description:
    - Create, Update, Delete directory server config
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Configure Directory Servers) -
      Operation Name: Create Directory Server Config -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - >-
      B(Delete a Directory Server by ExtID) -
      Operation Name: Delete Directory Server Config -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - >-
      B(Update a Directory Server by ExtID) -
      Operation Name: Update Directory Server Config -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=microseg)"
options:
    state:
        description:
            - State of the directory server config, whether to create, update or delete.
            - present -> Create directory server config if external ID is not provided,
              Update directory server config if external ID is provided.
            - absent -> Delete directory server config with the given external ID.
        type: str
        choices: ['present', 'absent']
    ext_id:
        description:
            - Directory server config External ID.
            - Required for updating or deleting directory server config.
        type: str
    is_default_category_enabled:
        description:
            - Whether the default category is enabled.
        type: bool
    should_keep_default_category_on_login:
        description:
            - Whether to keep the default category on login.
        type: bool
    matching_criterias:
        description:
            - List of matching criterias for the directory server config.
        type: list
        elements: dict
        suboptions:
            match_entity:
                description:
                    - The entity to match against.
                type: str
                choices: ["VM"]
            match_field:
                description:
                    - The field to match against.
                type: str
                choices: ["NAME"]
            match_type:
                description:
                    - The type of match to perform.
                type: str
                choices: ["ALL", "CONTAINS"]
            criteria:
                description:
                    - The criteria string for matching.
                type: str
    directory_service_reference:
        description:
            - The external ID of the directory service reference.
        type: str
    domain_controllers:
        description:
            - List of domain controllers for the directory server config.
        type: list
        elements: dict
        suboptions:
            ipv4:
                description:
                    - IPv4 address of the domain controller.
                type: dict
                suboptions:
                    value:
                        description: The IPv4 address value.
                        type: str
                    prefix_length:
                        description: The prefix length of the IPv4 address.
                        type: int
                        default: 32
            ipv6:
                description:
                    - IPv6 address of the domain controller.
                type: dict
                suboptions:
                    value:
                        description: The IPv6 address value.
                        type: str
                    prefix_length:
                        description: The prefix length of the IPv6 address.
                        type: int
                        default: 128
            fqdn:
                description:
                    - FQDN of the domain controller.
                type: dict
                suboptions:
                    value:
                        description: The FQDN value.
                        type: str
    wait:
        description:
            - Wait for the task to complete
        type: bool
        default: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create directory server config
  nutanix.ncp.ntnx_directory_server_config_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: present
    directory_service_reference: "00062ffc-95ad-19e9-185b-ac1f6b6f97a3"
    matching_criterias:
      - match_entity: VM
        match_field: NAME
        match_type: CONTAINS
        criteria: "test"
    is_default_category_enabled: true
    should_keep_default_category_on_login: false
  register: result

- name: Update directory server config
  nutanix.ncp.ntnx_directory_server_config_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: present
    ext_id: "{{ result.ext_id }}"
    directory_service_reference: "00062ffc-95ad-19e9-185b-ac1f6b6f97a3"
    matching_criterias:
      - match_entity: VM
        match_field: NAME
        match_type: ALL
    is_default_category_enabled: false
    should_keep_default_category_on_login: true
  register: result

- name: Delete directory server config
  nutanix.ncp.ntnx_directory_server_config_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: absent
    ext_id: "{{ result.ext_id }}"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for directory server config operations.
    - Directory server config details if C(wait) is true and the operation is create or update.
    - Task details if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
        "directory_service_reference": "00062ffc-95ad-19e9-185b-ac1f6b6f97a3",
        "domain_controllers": null,
        "ext_id": "b215708c-252f-400c-bc90-2f36242d3d3c",
        "is_default_category_enabled": true,
        "links": null,
        "matching_criterias": [
            {
                "criteria": "test",
                "match_entity": "VM",
                "match_field": "NAME",
                "match_type": "CONTAINS"
            }
        ],
        "should_keep_default_category_on_login": false,
        "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: str

failed:
    description: This field indicates if the task execution failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode (in delete operation)
    type: str
    sample: "Failed generating create directory server config Spec"

ext_id:
  description: The directory server config ext_id
  returned: always
  type: str
  sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"

task_ext_id:
  description: The task ext_id for the operation
  returned: when applicable
  type: str
  sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"

skipped:
  description: This indicates whether the task was skipped due to idempotency checks
  returned: when applicable
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_directory_server_configs_api_instance,
    get_etag,
)
from ..module_utils.v4.flow.helpers import get_directory_server_config  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_microseg_py_client as mic_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as mic_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ipv4_sub_spec = dict(
        value=dict(type="str"),
        prefix_length=dict(type="int", default=32),
    )

    ipv6_sub_spec = dict(
        value=dict(type="str"),
        prefix_length=dict(type="int", default=128),
    )

    fqdn_sub_spec = dict(
        value=dict(type="str"),
    )

    domain_controller_sub_spec = dict(
        ipv4=dict(type="dict", options=ipv4_sub_spec, obj=mic_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_sub_spec, obj=mic_sdk.IPv6Address),
        fqdn=dict(type="dict", options=fqdn_sub_spec, obj=mic_sdk.FQDN),
    )

    matching_criteria_sub_spec = dict(
        match_entity=dict(type="str", choices=["VM"]),
        match_field=dict(type="str", choices=["NAME"]),
        match_type=dict(type="str", choices=["ALL", "CONTAINS"]),
        criteria=dict(type="str"),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        is_default_category_enabled=dict(type="bool"),
        should_keep_default_category_on_login=dict(type="bool"),
        matching_criterias=dict(
            type="list",
            elements="dict",
            options=matching_criteria_sub_spec,
            obj=mic_sdk.MatchingCriteria,
        ),
        directory_service_reference=dict(type="str"),
        domain_controllers=dict(
            type="list",
            elements="dict",
            options=domain_controller_sub_spec,
            obj=mic_sdk.IPAddressOrFQDN,
        ),
    )

    return module_args


def create_directory_server_config(module, api_instance, result):

    sg = SpecGenerator(module)
    default_spec = mic_sdk.DirectoryServerConfig()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create directory server config Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_directory_server_config(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating directory server config",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status,
            rel=TASK_CONSTANTS.RelEntityType.DIRECTORY_SERVER_CONFIG,
        )
        if ext_id:
            resp = get_directory_server_config(module, api_instance, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_directory_server_config_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)
    if old_spec != update_spec:
        return False

    return True


def update_directory_server_config(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_directory_server_config(module, api_instance, ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating directory server config update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_directory_server_config_idempotency(
        current_spec.to_dict(), update_spec.to_dict()
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    etag = get_etag(current_spec)
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.update_directory_server_config_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating directory server config",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_directory_server_config(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_directory_server_config(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Directory server config with ext_id:{0} will be deleted.".format(ext_id)
        )
        return

    current_spec = get_directory_server_config(module, api_instance, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting directory server config", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = api_instance.delete_directory_server_config_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting directory server config",
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
            ("state", "present", ("directory_service_reference", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_microseg_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    api_instance = get_directory_server_configs_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_directory_server_config(module, api_instance, result)
        else:
            create_directory_server_config(module, api_instance, result)
    else:
        delete_directory_server_config(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
