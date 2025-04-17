#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_object_stores_info_v2
short_description: Get Object Stores info
version_added: 2.2.0
description:
    - Fetch specific object store info if external ID is provided
    - Fetch list of multiple object stores info if external ID is not provided with optional filters
options:
    ext_id:
        description: External ID to fetch specific object store info
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
author:
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
"""

RETURN = r"""
response:
    description:
        - Response for fetching object store info
        - Object store info if external ID is provided
        - List of multiple object stores info if external ID is not provided
    type: dict
    returned: always
    sample:

ext_id:
    description: External ID of the object store
    returned: always
    type: str
    sample: "cda893b8-2aee-34bf-817d-d2ee6026790b"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.objects.helpers import get_object_store  # noqa: E402
from ..module_utils.v4.objects.api_client import (  # noqa: E402
    get_objects_api_instance,
)
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


def get_object_store_with_ext_id(module, object_stores_api, result):
    ext_id = module.params.get("ext_id")
    resp = get_object_store(module, object_stores_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_object_stores(module, object_stores_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating object stores info Spec", **result)
    try:
        resp = object_stores_api.list_object_stores(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object stores info",
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
    result = {"changed": False, "response": None}
    object_stores_api = get_objects_api_instance(module)
    if module.params.get("ext_id"):
        get_object_store_with_ext_id(module, object_stores_api, result)
    else:
        get_object_stores(module, object_stores_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
