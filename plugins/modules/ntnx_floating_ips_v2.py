#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_floating_ips_v2
short_description: floating_ips module which supports floating_ip CRUD operations
version_added: 2.0.0
description:
  - Create, Update, Delete floating_ips
  - For floating IP  create and delete, module will return tasks status in response after operation.
  - For floating IP update, module will return floating IP info if C(wait) is true, else task status.
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - if C(state) is present, it will create or update the floating IP.
      - If C(state) is set to C(present) and ext_id is not provided then the operation will be create the floating IP
      - If C(state) is set to C(present) and ext_id is provided then the operation will be update the floating IP
      - If C(state) is set to C(absent) and ext_id is provided , then operation will be delete the floating IP
    type: str
    choices: ['present', 'absent']
  ext_id:
    description:
      - Subnet external ID
      - Required only for updating or deleting the subnet.
    type: str
  association:
    description: Spec to associating Floating IP with either VM NIC or Private IP
    type: dict
    suboptions:
      private_ip_association:
        description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
        type: dict
        suboptions:
          private_ip:
            description: Private IP address specification.
            type: dict
            required: true
            suboptions:
              ipv4:
                description: IPv4 address specification.
                type: dict
                suboptions:
                  prefix_length:
                    description: Prefix length.
                    type: int
                  value:
                    description: IP address value.
                    type: str
              ipv6:
                description: IPv6 address specification.
                type: dict
                suboptions:
                  prefix_length:
                    description: Prefix length.
                    type: int
                  value:
                    description: IP address value.
                    type: str
          vpc_reference:
            description: VPC in which the private IP exists.
            type: str
            required: true
      vm_nic_association:
        description: VM NIC reference.
        type: dict
        suboptions:
          vpc_reference:
            description: VPC reference ID.
            type: str
          vm_nic_reference:
            description: VM NIC reference ID.
            type: str
            required: true
  description:
    description: Description for the Floating IP.
    type: str
  external_subnet_reference:
    description: External subnet reference ID.
    type: str
  floating_ip:
    description: Floating IP address.
    type: dict
    suboptions:
      ipv4:
        description: IPv4 floating IP details.
        type: dict
        suboptions:
          prefix_length:
            description: Prefix length.
            type: int
          value:
            description: IP address value.
            type: str
      ipv6:
        description: IPv6 floating IP details.
        type: dict
        suboptions:
          prefix_length:
            description: Prefix length.
            type: int
          value:
            description: IP address value.
            type: str
  metadata:
    description: Metadata for the floating ip.
    type: dict
    suboptions:
              category_ids:
                description: A list of globally unique identifiers that represent all the categories the resource is associated with.
                elements: str
                type: list
              owner_reference_id:
                description: A globally unique identifier that represents the owner of this resource.
                type: str
              owner_user_name:
                description: The userName of the owner of this resource.
                type: str
              project_name:
                description: The name of the project this resource belongs to.
                type: str
              project_reference_id:
                description: A globally unique identifier that represents the project this resource belongs to.
                type: str
  name:
    description:
      - Name of the floating ip.
      - Required for create.
    type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Create floating ip using private IP in VPC
  nutanix.ncp.ntnx_floating_ips_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vpc_reference: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
    name: "test"
    association:
      private_ip_association:
        private_ip:
          ipv4:
            value: "192.168.1.2"
        vpc_reference: "33dba56c-f123-4ec6-8b38-901e1cf716c2"

- name: Delete floating IP
  nutanix.ncp.ntnx_floating_ips_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"

- name: Create floating ip with external subnet and vm nic reference
  nutanix.ncp.ntnx_floating_ips_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    external_subnet_reference: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
    association:
      vm_nic_association:
        vm_nic_reference: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
    name: "test"
"""

RETURN = r"""
response:
  description:
    - Floating IP info for update operation
    - Task details for create or delete operation
  returned: always
  type: dict
  sample: {
    "data": {
        "extId": "00000000-0000-0000-0000-000000000000",
        "metadata": {
            "ownerReferenceId": "00000000-0000-0000-0000-000000000000",
            "ownerUserName": "admin"
        },
        "floatingIp": {
            "ipv4": {
                "value": "192.168.1.69"
            }
        },
        "externalSubnetReference": "00000000-0000-0000-0000-000000000000"
    },
    "metadata": {
        "flags": [
            {
                "name": "hasError",
                "value": false
            },
            {
                "name": "isPaginated",
                "value": false
            }
        ],
        "totalAvailableResults": 1
    }
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
  description: Floating IP
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_floating_ip_api_instance,
)
from ..module_utils.v4.network.helpers import get_floating_ip  # noqa: E402
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
    import ntnx_networking_py_client as net_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as net_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    association_obj_map = {
        "vm_nic_association": net_sdk.VmNicAssociation,
        "private_ip_association": net_sdk.PrivateIpAssociation,
    }

    ip_address_sub_spec = dict(
        value=dict(type="str"),
        prefix_length=dict(type="int"),
    )

    ip_address_spec = dict(
        ipv4=dict(type="dict", options=ip_address_sub_spec, obj=net_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ip_address_sub_spec, obj=net_sdk.IPv6Address),
    )

    floating_ip_spec = dict(
        ipv4=dict(
            type="dict", options=ip_address_sub_spec, obj=net_sdk.FloatingIPv4Address
        ),
        ipv6=dict(
            type="dict", options=ip_address_sub_spec, obj=net_sdk.FloatingIPv6Address
        ),
    )

    metadata_spec = dict(
        owner_reference_id=dict(type="str"),
        owner_user_name=dict(type="str"),
        project_reference_id=dict(type="str"),
        project_name=dict(type="str"),
        category_ids=dict(type="list", elements="str"),
    )

    vm_nic_association_spec = dict(
        vm_nic_reference=dict(type="str", required=True),
        vpc_reference=dict(type="str"),
    )

    private_ip_association_spec = dict(
        private_ip=dict(
            type="dict", options=ip_address_spec, obj=net_sdk.IPAddress, required=True
        ),
        vpc_reference=dict(type="str", required=True),
    )

    association_spec = dict(
        vm_nic_association=dict(type="dict", options=vm_nic_association_spec),
        private_ip_association=dict(type="dict", options=private_ip_association_spec),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        association=dict(
            type="dict",
            options=association_spec,
            obj=association_obj_map,
            mutually_exclusive=[("vm_nic_association", "private_ip_association")],
        ),
        floating_ip=dict(
            type="dict", options=floating_ip_spec, obj=net_sdk.FloatingIPAddress
        ),
        external_subnet_reference=dict(type="str"),
        metadata=dict(type="dict", options=metadata_spec, obj=net_sdk.Metadata),
    )

    return module_args


def create_floating_ip(module, result):
    floating_ips = get_floating_ip_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = net_sdk.FloatingIp()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create floating_ips Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = floating_ips.create_floating_ip(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating floating_ip",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, TASK_CONSTANTS.RelEntityType.FLOATING_IP
        )
        if ext_id:
            resp = get_floating_ip(module, floating_ips, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_floating_ips_idempotency(old_spec, update_spec):
    if old_spec != update_spec:
        return False
    return True


def update_floating_ip(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    floating_ips = get_floating_ip_api_instance(module)

    current_spec = get_floating_ip(module, floating_ips, ext_id=ext_id)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating floating_ips update spec", **result)

    # handle update of association type
    if getattr(current_spec, "association", None):
        association_type = current_spec.association.get_object_type()
        if module.params.get("association").get("private_ip_association", None):

            if association_type != "networking.v4.config.PrivateIpAssociation":
                associationSpec = net_sdk.PrivateIpAssociation()
                params = module.params.get("association").get("private_ip_association")
                update_spec.association, err = sg.generate_spec(associationSpec, params)

        elif module.params.get("association").get("vm_nic_association", None):

            if association_type != "networking.v4.config.VmNicAssociation":
                associationSpec = net_sdk.VmNicAssociation()
                params = module.params.get("association").get("vm_nic_association")
                update_spec.association, err = sg.generate_spec(associationSpec, params)

    # check for idempotency
    if check_floating_ips_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = floating_ips.update_floating_ip_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating floating_ip",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_floating_ip(module, floating_ips, ext_id)
        result["ext_id"] = ext_id
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_floating_ip(module, result):
    floating_ips = get_floating_ip_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_floating_ip(module, floating_ips, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "unable to fetch etag for deleting floating_ip", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = floating_ips.delete_floating_ip_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting floating_ip",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id, True)
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
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
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
            update_floating_ip(module, result)
        else:
            create_floating_ip(module, result)
    else:
        delete_floating_ip(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
