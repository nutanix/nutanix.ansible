#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_iscsi_clients_info_v2
short_description: Fetch ISCSI clients info.
description:
    - By default, Fetch all iscsi clients currently attached to any VG
    - Fetch iscsi client if C(ext_id) is given
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
            - The external ID of the iscsi client.
            - This will fetch the iscsi client with the given external ID.
        type: str
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
- name: Fetch specific iscsi client info
  nutanix.ncp.ntnx_volume_groups_iscsi_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35
  register: result

- name: Fetch all iscsi clients attached across VGs
  nutanix.ncp.ntnx_volume_groups_iscsi_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    limit: 10
  register: result
"""

RETURN = r"""
response:
    description:
        - list of iscsi clients currently attached to any VG
        - specific iscsi client if ext_id given
    type: dict
    returned: always
    sample:   [
            {
                "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
                "created_time": null,
                "ext_id": "aea43b5c-ae4d-4b60-934b-f8f581275dec",
                "links": [
                    {
                        "href": "https://*****:9440/api/volumes/v4.0.b1/config/iscsi-clients/aea43b5c-ae4d-4b60-934b-f8f581275dec",
                        "rel": "external_attachment"
                    }
                ],
                "tenant_id": null
            }
        ]
ext_id:
    description: Iscsi client external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
error:
    description: The error message if any.
    type: str
    returned: when error occurs
    sample: "Api Exception raised while fetching ISCSI clients attached to VGs"
changed:
    description: Indicates whether the resource has changed.
    type: bool
    returned: always
    sample: true
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_iscsi_client_api_instance,
)


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_iscsi_client(module, result):
    clients = get_iscsi_client_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = clients.get_iscsi_client_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching given ISCSI client",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_iscsi_clients(module, result):
    clients = get_iscsi_client_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating info Spec", **result)

    try:
        resp = clients.list_iscsi_clients(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching all available ISCSI clients",
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
    if module.params.get("ext_id"):
        get_iscsi_client(module, result)
    else:
        get_iscsi_clients(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
