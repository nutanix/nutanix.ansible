#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_licensing_keys_info_v2
short_description: Get license key(s) info
version_added: 2.4.0
description:
    - Fetch specific license key info using external ID
    - Fetch list of multiple license keys info if external ID is not provided with optional filters
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - External ID to fetch specific license key info
        type: str
extends_documentation_fragment:
        - nutanix.ncp.ntnx_credentials
        - nutanix.ncp.ntnx_info_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""
EXAMPLES = r"""

"""
RETURN = r"""

"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.licensing.api_client import (  # noqa: E402
    get_licensing_key_api_instance,
)
from ..module_utils.v4.licensing.helpers import get_licensing_key  # noqa: E402
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
        expand=dict(type="str"),
    )

    return module_args


def get_licensing_key_using_ext_id(module, licensing_keys, result):
    ext_id = module.params.get("ext_id")
    resp = get_licensing_key(module, licensing_keys, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_licensing_keys(module, licensing_keys, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating license keys info Spec", **result)

    try:
        resp = licensing_keys.list_license_keys(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching license keys info",
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
    licensing_keys = get_licensing_key_api_instance(module)
    if module.params.get("ext_id"):
        get_licensing_key_using_ext_id(module, licensing_keys, result)
    else:
        get_licensing_keys(module, licensing_keys, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
