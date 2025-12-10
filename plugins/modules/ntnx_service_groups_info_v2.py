#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_service_groups_info_v2
short_description: service_group info module
version_added: 2.0.0
description:
    - This module is used to get service groups info.
    - It can be used to get all service groups or a particular service group using ext_id.
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - Service group external id.
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
- name: test getting particular service_group using external id
  nutanix.ncp.ntnx_service_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: '{{ result.response.0.ext_id }}'

- name: test getting all service groups
  nutanix.ncp.ntnx_service_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
"""
RETURN = r"""
response:
  description:
      - Response for fetching service groups info.
      - One service group info if External ID is provided.
      - List of multiple service groups info if External ID is not provided.
  returned: always
  type: dict
  sample: {
                "created_by": null,
                "description": "IPv6 Behind NAT44 CPEs",
                "ext_id": "8f6351f3-ccf2-4e05-ac11-79daa1ad8158",
                "icmp_services": null,
                "is_system_defined": true,
                "links": null,
                "name": "6a44",
                "policy_references": null,
                "tcp_services": [
                    {
                        "end_port": 1027,
                        "start_port": 1027
                    }
                ],
                "tenant_id": null,
                "udp_services": null
            }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching service groups info"

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

total_available_results:
    description:
        - The total number of available service groups in PC.
    type: int
    returned: when all service groups are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_service_groups_api_instance,
)
from ..module_utils.v4.flow.helpers import get_service_group  # noqa: E402
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


def get_service_group_using_ext_id(module, result):
    ext_id = module.params.get("ext_id")
    service_groups = get_service_groups_api_instance(module)
    resp = get_service_group(module, service_groups, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_service_groups(module, result):
    service_groups = get_service_groups_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating service groups info Spec", **result)

    try:
        resp = service_groups.list_service_groups(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching service groups info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

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
        get_service_group_using_ext_id(module, result)
    else:
        get_service_groups(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
