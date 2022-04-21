
import time
from ..module_utils.fc.imaged_clusters import ImagedClusters
from ..module_utils.base_module import BaseModule
from ..module_utils.fc.imaged_nodes import ImagedNodes
from ..module_utils.utils import remove_param_with_none_value

def get_module_spec():
    common_network_setting_spec_dict = dict(
        cvm_dns_servers = dict(type="list"),
        hypervisor_dns_servers = dict(type="list"),
        cvm_ntp_servers= dict(type="list", Required=True),
        hypervisor_ntp_servers= dict(type="list", Required=True)
    )

    hypervisor_iso_details_spec_dict = dict(
        hyperv_sku = dict(type="str", default=None),
        url = dict(type="str", Required=True),
        hyperv_product_key = dict(type="str", default=None),
        sha256sum= dict(type="str", default=None)
    )

    nodes_list_spec_dict = dict(
        cvm_gateway = dict(type="str", Required=True),
        ipmi_netmask = dict(type="str", Required=True),
        rdma_passthrough = dict(type="bool", Default=False),
        imaged_node_uuid = dict(type="str", Required=True),
        cvm_vlan_id= dict(type="int", default=None),
        hypervisor_type = dict(type="str", Required=True, choice="[kvm, esx, hyperv]"),
        image_now = dict(type="bool", default=True),
        hypervisor_hostname = dict(type="str", Required=True),
        hypervisor_netmask = dict(type="str", Required=True),
        cvm_netmask = dict(type="str", Required=True),
        ipmi_ip = dict(type="str", Required=True),
        hypervisor_gateway = dict(type="str", Required=True),
        hardware_attributes_override = dict(type="dict", default=None),
        cvm_ram_gb = dict(type="int", default=None),
        cvm_ip = dict(type="str", Required=True),
        hypervisor_ip = dict(type="str", Required=True),
        use_existing_network_settings = dict(type="bool", default=False),
        ipmi_gateway =dict(type="str", Required=True)

    )

    module_args = dict(
        cluster_external_ip = dict(type="str", default=None),
        storage_node_count = dict(type="int", default=None),
        redundancy_factor = dict(type="int", Required=True, default=2),
        cluster_name = dict(type="str", Required=True),
        aos_package_url = dict(type="str", Required=True),
        cluster_size = dict(type="int", default=None),
        aos_package_sha256sum= dict(type="str", default=None),
        timezone= dict(type="str",default=None),
        common_network_settings = dict(type="dict", Required=True, options=common_network_setting_spec_dict),
        hypervisor_iso_details = dict(type="dict", options=hypervisor_iso_details_spec_dict),
        nodes_list = dict(type="list", elements="dict", Required=True, options=nodes_list_spec_dict),
        skip_cluster_creation = dict(type="bool", default=False)
    )

    return module_args


def imageNodes(module, result):
    imaging = ImagedClusters(module)
    spec, error = imaging.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating Image Nodes Spec", **result)
    
    check_node_available(module, spec["nodes_list"], result)

    resp = imaging.create(spec)
    result["imaged_cluster_uuid"] = resp["imaged_cluster_uuid"]

    wait_till_completion(module, result)


def check_node_available(module, nodes, result):
    av = ImagedNodes(module)
    for i in nodes:
        node_detail = av.read(i["imaged_node_uuid"])
        node_state = node_detail["node_state"]
        if node_state != "STATE_AVAILABLE":
            avial, err = wait_till_node_available(module, i["imaged_node_uuid"], node_state)
            if err:
                result["error"] = err
                result["response"] = avial
                module.fail_json(msg="Nodes not available or may be part of other cluster", **result)

    

def wait_till_node_available(module, node_uuid, node_state):
    timeout = time.time() + 1800
    delay = 60
    img = ImagedNodes(module)
    while node_state!= "STATE_AVAILABLE" :
        node_detail = img.read(node_uuid)
        new_node_state = node_detail["node_state"]
        if new_node_state != "STATE_AVAILABLE":
            if time.time() > timeout:
                return (
                    None,
                    "Timeout. Node is in {}\n".format(new_node_state)
                )
            time.sleep(delay)
        else:
            node_state = new_node_state
        
    return node_state, None



def wait_till_completion(module, result):
    imaged_cluster_uuid = result["imaged_cluster_uuid"]
    resp, err = wait_for_completion(module, imaged_cluster_uuid)
    result["response"] = resp
    if err:
        result["error"] = err
        result["response"] = resp
        module.fail_json(msg="Failed to image nodes", **result)

def wait_for_completion(module, uuid):
    state = ""
    delay = 30
    timeout = time.time() + (2*60*60)
    time.sleep(15*60)
    progress= ImagedClusters(module)
    while state != "COMPLETED":
        response = progress.get(uuid)
        stopped = response["cluster_status"]["imaging_stopped"]
        aggregate_percent_complete = response["cluster_status"]["aggregate_percent_complete"]
        if stopped:
            if aggregate_percent_complete < 100:
                status = _get_progress_error_status(response)
                return response, status
            state = "COMPLETED"
        else:
            state = "PENDING"
            if time.time() > timeout:
                return (
                    None,
                    "Failed to poll on image node progress. Reason: Timeout",
                )
            time.sleep(delay)
    return response, None

def _get_progress_error_status(progress):
    return "Imaging stopped before completion.\nClusters: {}\nNodes: {}".format(
        _get_cluster_progress_messages(progress, "cluster_progress_details", "cluster_name"),
        _get_node_progress_messages(progress, "node_progress_details", "imaged_node_uuid"),
    )

def _get_cluster_progress_messages(progress, entity_type, entity_name):
    res = ""
    cluster = progress["cluster_status"][entity_type]
    if cluster.get(entity_name):
        res += "cluster_name: {}\n".format(cluster[entity_name])
    res += "status:\n{}\n".format(cluster["status"])

    return res

def _get_node_progress_messages(progress, entity_type, entity_name):
    res = ""
    nodes = progress["cluster_status"][entity_type]
    if nodes:
        for c in nodes:
            res += "node_uuid: {}\n".format(c[entity_name])
            res += "status:\n{}\n".format(c["status"])
    return res


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {}
    imageNodes(module, result)
    module.exit_json(**result)


def main():
    run_module()

if __name__ == "__main__":
    main()