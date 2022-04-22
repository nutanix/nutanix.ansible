from email.policy import default

from requests import options
from ..module_utils.fc.imaged_nodes import ImagedNodes
from ..module_utils.base_module import BaseModule

from ..module_utils.utils import remove_param_with_none_value


def get_module_spec():
    module_args = dict(
        imaged_node_uuid = dict(type="str"),
        length=dict(type="int", default=10),
        offset=dict(type="int", default=0),
        filters=dict(
            type="dict",
            node_state = dict(type="str", choices=["STATE_AVAILABLE", "STATE_UNAVAILABLE", "STATE_DISCOVERING", "STATE_IMAGING"],
            default = None)
        )
    )

    return module_args


def list_imaged_nodes(module, result):
    imaged_node_uuid = module.params.get("imaged_node_uuid")
    list_imaged_nodes = ImagedNodes(module)
    
    if imaged_node_uuid:
        resp = list_imaged_nodes.read(imaged_node_uuid)
        result["imaged_node_details"] = resp
    else:
        spec, error = list_imaged_nodes.get_spec()
        if error:
            result["error"] = error
            module.fail_json(msg="Failed generating Image Nodes Spec", **result)

        resp = list_imaged_nodes.list(spec)

        offset = module.params.get("offset") 
        length = module.params.get("length") + offset
        total_matches = resp["metadata"]["length"]

        if length>total_matches:
            length = total_matches

        resp["imaged_nodes"] = resp["imaged_nodes"][offset:length]
        result["imaged_nodes_list"] = resp
        

def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {}
    list_imaged_nodes(module, result)
    module.exit_json(**result)

def main():
    run_module()

if __name__ == "__main__":
    main()
