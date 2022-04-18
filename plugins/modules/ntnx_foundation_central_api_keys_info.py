from operator import mod
from ..module_utils.fc.api_keys import ApiKeys
from ..module_utils.base_module import BaseModule

from ..module_utils.utils import remove_param_with_none_value

def get_module_spec():
    module_args = dict(
        key_uuid = dict(type=str),
        alias = dict(type=str)

    )
    return module_args

def list_api_keys(module, result):
    key_uuid= module.params.get("key_uuid")
    alias = module.params.get("alias")
    list_api = ApiKeys(module)
    if key_uuid:
        resp = list_api.read(key_uuid)
        result["api_keys"] = resp
    elif alias:
        spec = {
            "length": 0,
            "offset": 0 
        }
        resp = list_api.list(spec)
        
        for i in resp:
            print(i[0]["alias"])

        result["list_api_keys"]= resp
        


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {}
    list_api_keys(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
