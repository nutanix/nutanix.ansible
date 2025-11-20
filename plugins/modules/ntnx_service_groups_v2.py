#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_service_groups_v2
short_description: "Create, Update, Delete service groups"
version_added: 2.0.0
description: "Create, Update, Delete service groups"
options:
  state:
    description:
      - State of the service group, whether to create, update or delete.
      - present -> Create service group if external ID is not provided, Update service group if external ID is provided.
      - absent -> Delete service group with the given external ID.
      - This module uses PC v4 APIs based SDKs
    type: str
    required: false
    choices: ['present', 'absent']

  ext_id:
    description:
      - Service group External ID.
      - Required for updating or deleting service group.
    type: str

  name:
    description:
      - Service group name.
    type: str

  description:
    description:
      - Service group description.
    type: str

  tcp_services:
    description:
      - List of TCP services.
    type: list
    elements: dict
    suboptions:
          start_port:
            description: Starting port of the range.
            type: int
          end_port:
            description: Ending port of the range.
            type: int

  udp_services:
    description:
      - List of UDP services.
    type: list
    elements: dict
    suboptions:
          start_port:
            description: Starting port of the range.
            type: int
          end_port:
            description: Ending port of the range.
            type: int

  icmp_services:
    description:
      - List of ICMP services.
    type: list
    elements: dict
    suboptions:
          is_all_allowed:
            description: Indicates if all code types are allowed.
            type: bool
          type:
            description: ICMP message type.
            type: int
          code:
            description: ICMP message code.
            type: int
  wait:
    description:
      - Wait for the task to complete
    type: bool
    default: true

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
- name: create tcp service group
  nutanix.ncp.ntnx_service_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: tcp_service_group
    description: desc
    tcp_services:
      - start_port: 10
        end_port: 50
      - start_port: 60
        end_port: 90
      - start_port: 98
        end_port: 98
      - start_port: 99
        end_port: 99

- name: create udp service group
  nutanix.ncp.ntnx_service_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: udp_service_group
    description: desc
    udp_services:
      - start_port: 10
        end_port: 50
      - start_port: 60
        end_port: 90
      - start_port: 98
        end_port: 98
      - start_port: 99
        end_port: 99

- name: create icmp with service group
  nutanix.ncp.ntnx_service_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: icmp_srvive_group
    description: desc
    icmp_services:
      - code: 10
        type: 1
      - code: 3
        type: 2

- name: Delete all created service groups
  nutanix.ncp.ntnx_service_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "{{ item }}"
"""

RETURN = r"""
response:
  description:
      - Response for service groups operations.
      - Service group details if C(wait) is True.
      - Task details if C(wait) is False.
  returned: always
  type: dict
  sample: {
            "created_by": "00000000-0000-0000-0000-000000000000",
            "description": "desc",
            "ext_id": "24107d61-2b08-470f-afda-cd0350182b3b",
            "icmp_services": null,
            "is_system_defined": false,
            "links": null,
            "name": "service_group_sekEkbklgvOJ_2",
            "policy_references": null,
            "tcp_services": null,
            "tenant_id": null,
            "udp_services": [
                {
                    "end_port": 50,
                    "start_port": 10
                },
                {
                    "end_port": 90,
                    "start_port": 60
                },
                {
                    "end_port": 98,
                    "start_port": 98
                },
                {
                    "end_port": 99,
                    "start_port": 99
                }
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
  description: The created service group ext_id
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

skipped:
  description: This indicates whether the task was skipped due to idempotency checks
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_etag,
    get_service_groups_api_instance,
)
from ..module_utils.v4.flow.helpers import (  # noqa: E402
    get_service_group,
    strip_service_group_extra_attributes,
)
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
    icmp_service_spec = dict(
        is_all_allowed=dict(type="bool"),
        type=dict(type="int"),
        code=dict(type="int"),
    )

    range_spec = dict(
        start_port=dict(type="int"),
        end_port=dict(type="int"),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        tcp_services=dict(
            type="list",
            elements="dict",
            options=range_spec,
            obj=mic_sdk.TcpPortRangeSpec,
        ),
        udp_services=dict(
            type="list",
            elements="dict",
            options=range_spec,
            obj=mic_sdk.UdpPortRangeSpec,
        ),
        icmp_services=dict(
            type="list",
            elements="dict",
            options=icmp_service_spec,
            obj=mic_sdk.IcmpTypeCodeSpec,
        ),
    )

    return module_args


def create_service_group(module, result):
    service_groups = get_service_groups_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = mic_sdk.ServiceGroup()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create service groups Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = service_groups.create_service_group(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating service group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.SERVICE_GROUP
        )
        if ext_id:
            resp = get_service_group(module, service_groups, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_service_groups_idempotency(old_spec, update_spec):
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    if old_spec != update_spec:
        return False

    return True


def update_service_group(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    service_groups = get_service_groups_api_instance(module)
    current_spec = get_service_group(module, service_groups, ext_id)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating service_groups update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    # check for idempotency
    if check_service_groups_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    strip_service_group_extra_attributes(update_spec)

    resp = None
    service_groups = get_service_groups_api_instance(module)
    try:
        resp = service_groups.update_service_group_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating service_group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_service_group(module, service_groups, ext_id)
        result["ext_id"] = ext_id
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_service_group(module, result):
    service_groups = get_service_groups_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Service group with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_service_group(module, service_groups, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting service group", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = service_groups.delete_service_group_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting service_group",
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
            ("state", "absent", ("ext_id",)),
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
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_service_group(module, result)
        else:
            create_service_group(module, result)
    else:
        delete_service_group(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
