#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_licensing_key_v2
short_description: Add or Delete a licensing key
version_added: 2.4.0
description:
    - Add or Delete a licensing key
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - The state of the licensing key, whether to add or delete.
            - present -> Add licensing key if external ID is not provided.
            - absent -> Delete licensing key using the provided licensing key external ID.
        type: str
        choices: ["present", "absent"]
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
"""
RETURN = r"""
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.licensing.api_client import (  # noqa: E402
    get_licensing_key_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_licensing_py_client as licensing_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as licensing_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        state=dict(type="str", choices=["present", "absent"], default="present"),
        key=dict(type="str"),
        validation_detail=dict(type="str"),
        type=dict(
            type="str",
            choices=[
                "CALM",
                "DRS",
                "NDA",
                "NDB",
                "FLOW",
                "NDB_PLATFORM",
                "EUC",
                "NCI_C",
                "NCI_D",
                "UNIFIED_STORAGE",
                "VDI",
                "FILE",
                "NDS",
                "EDGE",
                "AOS",
                "NCM_EUC",
                "NDA_PLATFORM",
                "NO_LICENSE",
                "OBJECTS",
                "PRISM",
                "OBJECT",
                "ROBO",
                "NDS_PLATFORM",
                "NUS",
                "NKPFS",
                "NKP",
                "NCI",
                "ERA",
                "NCM_CLOUD",
                "MINE",
                "NAI",
                "NCM",
                "NCM_EDGE",
            ],
        ),
        category=dict(
            type="str",
            choices=[
                "CALM",
                "CLOUD",
                "ANALYTICS",
                "NDA",
                "PRO",
                "ULTIMATE",
                "CLOUD_ULTIMATE",
                "NDB",
                "ADV_REPLICATION",
                "ADR",
                "STANDALONE",
                "ADVANCED_REPLICATION",
                "AOS_MINE",
                "NDK",
                "STARTER",
                "CLOUD_NATIVE",
                "NDS",
                "ULTIMATE_TRIAL",
                "STANDARD",
                "PUBLIC_CLOUD",
                "CLOUD_PRO",
                "PRO_SPECIAL",
                "DATA_ENCRYPTION",
                "NO_LICENSE",
                "PRISM_STARTER",
                "OBJECT",
                "APPAUTOMATION",
                "SOFTWARE_ENCRYPTION",
                "NKS",
                "UST",
                "DRASS",
                "SECURITY",
                "NUS_ENCRYPTION",
                "NUS_REPLICATION",
            ],
        ),
        sub_category=dict(type="str", choices=["ADDON", "PRIMARY"]),
        meter=dict(
            type="str",
            choices=[
                "CORES",
                "VI",
                "VM_PACKS",
                "NODE",
                "VM",
                "VCPU",
                "TIB",
                "USERS",
                "FLASH",
            ],
        ),
    )
    return module_args


def add_licensing_key(module, licensing_keys, result):
    sg = SpecGenerator(module)
    default_spec = licensing_sdk.LicenseKey()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create licensing key Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = licensing_keys.add_license_key(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating licensing key",
        )
    if resp.get("data", {}).get("ext_id", 0):
        result["ext_id"] = resp.get("data", {}).get("ext_id")
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def delete_licensing_key(module, licensing_keys, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Licensing key with ext_id:{0} will be deleted.".format(ext_id)
        return

    try:
        resp = licensing_keys.delete_license_key_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting licensing key",
        )
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            (
                "state",
                "absent",
                ("ext_id",),
            ),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_licensing_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    licensing_keys = get_licensing_key_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        add_licensing_key(module, licensing_keys, result)
    else:
        delete_licensing_key(module, licensing_keys, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
