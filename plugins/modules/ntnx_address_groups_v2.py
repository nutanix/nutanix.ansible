#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_address_groups_v2
short_description: Create, Update, Delete address groups
version_added: 2.0.0
description:
    - Create, Update, Delete address groups
    - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
        - State of the address group, whether to create, update or delete.
        - present -> Create address group if external ID is not provided, Update address group if external ID is provided.
        - absent -> Delete address group with the given external ID.
    type: str
    choices: ['present', 'absent']

  ext_id:
    description:
        - Address group External ID.
        - Required for updating or deleting address group.
    type: str

  name:
    description:
       - Address group name.
    type: str

  description:
    description:
      - Address group description.
    type: str

  ipv4_addresses:
    description: List of IPv4 addresses.
    type: list
    elements: dict
    suboptions:
          value:
            description: The IPv4 address value.
            type: str
          prefix_length:
            description: The prefix length of the IPv4 address.
            type: int
  ip_ranges:
    description: List of IP ranges.
    type: list
    elements: dict
    suboptions:
          start_ip:
            description: Starting IP address of the range.
            type: str
          end_ip:
            description: Ending IP address of the range.
            type: str
  wait:
    description:
      - Wait for the task to complete
    type: bool
    default: true

extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create address group
  nutanix.ncp.ntnx_address_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: present
    name: "{{ag1}}"
    description: test-ansible-group-1-desc
    ipv4_addresses:
      - value: "10.1.1.0"
        prefix_length: 24
      - value: "10.1.2.2"
        prefix_length: 32

- name: delete address group
  nutanix.ncp.ntnx_address_groups_v2:
    state: absent
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "{{ todelete }}"
"""

RETURN = r"""
response:
  description:
      - Response for address groups operations
      - Address group details if C(wait) is True
      - Task details if C(wait) is False
  returned: always
  type: dict
  sample:
        {
            "created_by": "00000000-0000-0000-0000-000000000000",
            "description": "test-ansible-group-1-desc",
            "ext_id": "63311404-8b2e-4dbf-9e33-7848cc88d330",
            "ip_ranges": null,
            "ipv4_addresses": [
                {
                    "prefix_length": 24,
                    "value": "10.1.1.0"
                },
                {
                    "prefix_length": 32,
                    "value": "10.1.2.2"
                }
            ],
            "links": null,
            "name": "yclaDaQKtEGIansible-ag2",
            "policy_references": null,
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
  type: bool
  sample: false

failed:
    description: This field indicates if the task execution failed
    returned: always
    type: bool
    sample: false

ext_id:
  description: The created address group ext_id
  returned: always
  type: str
  sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_address_groups_api_instance,
    get_etag,
)
from ..module_utils.v4.flow.helpers import get_address_group  # noqa: E402
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
    ip_address_sub_spec = dict(
        value=dict(type="str"),
        prefix_length=dict(type="int"),
    )

    ip_range_spec = dict(
        start_ip=dict(type="str"),
        end_ip=dict(type="str"),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        ipv4_addresses=dict(
            type="list",
            elements="dict",
            options=ip_address_sub_spec,
            obj=mic_sdk.IPv4Address,
        ),
        ip_ranges=dict(
            type="list", elements="dict", options=ip_range_spec, obj=mic_sdk.IPv4Range
        ),
    )

    return module_args


def create_address_group(module, result):
    address_groups = get_address_groups_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = mic_sdk.AddressGroup()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create address groups Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = address_groups.create_address_group(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating address group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.ADDRESS_GROUP
        )
        if ext_id:
            resp = get_address_group(module, address_groups, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_address_groups_idempotency(old_spec, update_spec):
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    if old_spec != update_spec:
        return False

    return True


def update_address_group(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    address_groups = get_address_groups_api_instance(module)

    current_spec = get_address_group(module, address_groups, ext_id)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating address_groups update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    # check for idempotency
    if check_address_groups_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = None
    try:
        resp = address_groups.update_address_group_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating address_group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_address_group(module, address_groups, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_address_group(module, result):
    address_groups = get_address_groups_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Address group with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_address_group(module, address_groups, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting address group", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = address_groups.delete_address_group_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting address_group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_microseg_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_address_group(module, result)
        else:
            create_address_group(module, result)
    else:
        delete_address_group(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
