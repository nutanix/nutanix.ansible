
from http.client import IncompleteRead
from ..module_utils.fc.imaged_clusters import  ImagedClusters
from ..module_utils.base_module import BaseModule
from ..module_utils.utils import remove_param_with_none_value

def get_module_spec():
    module_args = dict(
        imaged_cluster_uuid = dict(type="str"),
        length=dict(type="int", default=10),
        offset=dict(type="int", default=0),
        filters=dict(
            type="dict",
            archived = dict(type="bool", default=False)
        )
    )

    return module_args

def list_clusters_nodes(module, result):
    imaged_cluster_uuid = module.params.get("imaged_cluster_uuid")
    list_imaged_clusters = ImagedClusters(module)
    
    if imaged_cluster_uuid:
        resp = list_imaged_clusters.read(imaged_cluster_uuid)
        result["imaged_clusters"] = resp
    else:
        spec, error = list_imaged_clusters.get_spec()
        if error:
            result["error"] = error
            module.fail_json(msg="Failed generating Image Clusters Spec", **result)

        resp = list_imaged_clusters.list(spec)

        offset = module.params.get("offset") 
        length = module.params.get("length") + offset
        total_matches = resp["metadata"]["length"]

        if length>total_matches:
            length = total_matches

        resp["imaged_clusters"] = resp["imaged_clusters"][offset:length]
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