
from http.client import IncompleteRead
from ..module_utils.fc.imaged_clusters import  ImagedClusters
from ..module_utils.base_module import BaseModule
from ..module_utils.utils import remove_param_with_none_value

def get_module_spec():
    module_args = dict(
        imaged_cluster_uuid = dict(type="str"),
        filter_spec = dict(
            type = "dict",
            length=dict(type="int", default=0),
            offset=dict(type="int", default=0),
            filters=dict(
                archived = dict(type="bool", default=False)
            )
        )
    )

    return module_args

def list_clusters_nodes(module, result):
    imaged_cluster_uuid = module.params.get("imaged_cluster_uuid")
    filter_spec = module.params.get("filter_spec")
    list_imaged_clusters = ImagedClusters(module)
    if imaged_cluster_uuid:
        resp = list_imaged_clusters.read(imaged_cluster_uuid)
        result["imaged_clusters"] = resp
    else:
        resp = list_imaged_clusters.list(filter_spec)
        result["list_imaged_clusters"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {}
    list_clusters_nodes(module, result)
    module.exit_json(**result)



def main():
    run_module()

if __name__ == "__main__":
    main()