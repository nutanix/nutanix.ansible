#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_backup_api_instance,
)
from ..module_utils.v4.prism.helpers import get_restore_point  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        restore_source_ext_id=dict(type="str", required=True),
        restorable_domain_manager_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def get_restore_points(module, domain_manager_backups_api, result):
    restore_source_ext_id = module.params.get("restore_source_ext_id")
    restorable_domain_manager_ext_id = module.params.get(
        "restorable_domain_manager_ext_id"
    )
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating restore points info Spec", **result)
    try:
        resp = domain_manager_backups_api.list_restore_points(
            restoreSourceExtId=restore_source_ext_id,
            restorableDomainManagerExtId=restorable_domain_manager_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching restore points info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_restore_points_with_ext_id(module, domain_manager_backups_api, result):
    restore_source_ext_id = module.params.get("restore_source_ext_id")
    restorable_domain_manager_ext_id = module.params.get(
        "restorable_domain_manager_ext_id"
    )
    ext_id = module.params.get("ext_id")
    resp = get_restore_point(
        module,
        domain_manager_backups_api,
        ext_id,
        restore_source_ext_id,
        restorable_domain_manager_ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


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
    domain_manager_backups_api = get_domain_manager_backup_api_instance(module)
    if module.params.get("ext_id"):
        get_restore_points_with_ext_id(module, domain_manager_backups_api, result)
    else:
        get_restore_points(module, domain_manager_backups_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
