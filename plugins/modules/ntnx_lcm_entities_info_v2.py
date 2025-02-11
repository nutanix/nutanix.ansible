#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_config_info_v2
short_description: Fetch LCM Entities Info
description:
    - This module fetches LCM Entities Info.
    - Fetch a particular LCM entity details using external ID.
version_added: 2.0.0
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
options:
    ext_id:
        description:
            - The external ID of the entity.
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
"""

RETURN = r"""
response:
    description: The response from the LCM config API
    type: dict
    returned: always
    sample:
        {}
changed:
    description: Whether the module made any changes
    type: bool
    returned: always
    sample: false
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: bool
    returned: always
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_entity_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.lcm.helpers import get_lcm_entity  # noqa: E402
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


def get_entity_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_lcm_entity(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_entities(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed to generate info spec for entities", **result)

    try:
        resp = api_instance.list_entities(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM entities info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }

    api_instance = get_entity_api_instance(module)
    if module.params.get("ext_id"):
        get_entity_using_ext_id(module, api_instance, result)
    else:
        get_entities(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
