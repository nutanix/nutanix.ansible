#from __future__ import absolute_import, division, print_function

from ast import alias
from ..module_utils.fc.api_keys import ApiKeys
from ..module_utils.base_module import BaseModule

from ..module_utils.utils import remove_param_with_none_value

def get_module_spec():
    module_args = dict(
        alias = dict(type=str)
    )
    return module_args


def create(module, result):
    key = ApiKeys(module)
    spec, error = key.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating api_key Spec", **result)

    resp = key.create(spec)
    result["api_key"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {}
    create(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
