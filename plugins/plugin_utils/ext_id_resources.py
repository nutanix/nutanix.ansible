# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..module_utils.v4.clusters_mgmt.api_client import (
    get_cluster_profiles_api_instance,
    get_clusters_api_instance,
    get_storage_containers_api_instance,
)
from ..module_utils.v4.data_policies.api_client import (
    get_protection_policies_api_instance,
    get_storage_policies_api_instance,
)
from ..module_utils.v4.data_protection.api_client import (
    get_recovery_point_api_instance,
)
from ..module_utils.v4.flow.api_client import (
    get_address_groups_api_instance,
    get_entity_groups_api_instance,
    get_network_security_policy_api_instance,
    get_service_groups_api_instance,
)
from ..module_utils.v4.iam.api_client import (
    get_authorization_policy_api_instance,
    get_directory_service_api_instance,
    get_identity_provider_api_instance,
    get_permission_api_instance,
    get_role_api_instance,
    get_user_api_instance,
    get_user_group_api_instance,
)
from ..module_utils.v4.network.api_client import (
    get_floating_ip_api_instance,
    get_network_function_api_instance,
    get_routing_policies_api_instance,
    get_subnet_api_instance,
    get_virtual_switches_api_instance,
    get_vpc_api_instance,
)
from ..module_utils.v4.objects.api_client import get_objects_api_instance
from ..module_utils.v4.prism.pc_api_client import get_categories_api_instance
from ..module_utils.v4.vmm.api_client import (
    get_image_api_instance,
    get_image_placement_policy_api_instance,
    get_ova_api_instance,
    get_templates_api_instance,
    get_vm_api_instance,
)
from ..module_utils.v4.volumes.api_client import (
    get_iscsi_client_api_instance,
    get_vg_api_instance,
)

# Maps a resource keyword to how its list API is reached and which attribute
# its names live under. Any top level entity that exposes a list API supporting
# an OData $filter and returning an ext_id can be added here. The
# ``filter_attribute`` is the server side OData property name (camelCase), which
# defaults to ``name`` for most entities.
RESOURCE_MAP = {
    # --- clusters management --------------------------------------------------
    "cluster": {
        "get_api_instance": get_clusters_api_instance,
        "list_method": "list_clusters",
        "filter_attribute": "name",
    },
    "cluster_profile": {
        "get_api_instance": get_cluster_profiles_api_instance,
        "list_method": "list_cluster_profiles",
        "filter_attribute": "name",
    },
    "storage_container": {
        "get_api_instance": get_storage_containers_api_instance,
        "list_method": "list_storage_containers",
        "filter_attribute": "name",
    },
    # --- networking -----------------------------------------------------------
    "subnet": {
        "get_api_instance": get_subnet_api_instance,
        "list_method": "list_subnets",
        "filter_attribute": "name",
    },
    "vpc": {
        "get_api_instance": get_vpc_api_instance,
        "list_method": "list_vpcs",
        "filter_attribute": "name",
    },
    "virtual_switch": {
        "get_api_instance": get_virtual_switches_api_instance,
        "list_method": "list_virtual_switches",
        "filter_attribute": "name",
    },
    "floating_ip": {
        "get_api_instance": get_floating_ip_api_instance,
        "list_method": "list_floating_ips",
        "filter_attribute": "name",
    },
    "network_function": {
        "get_api_instance": get_network_function_api_instance,
        "list_method": "list_network_functions",
        "filter_attribute": "name",
    },
    "routing_policy": {
        "get_api_instance": get_routing_policies_api_instance,
        "list_method": "list_routing_policies",
        "filter_attribute": "name",
    },
    # --- virtual machine management -------------------------------------------
    "vm": {
        "get_api_instance": get_vm_api_instance,
        "list_method": "list_vms",
        "filter_attribute": "name",
    },
    "image": {
        "get_api_instance": get_image_api_instance,
        "list_method": "list_images",
        "filter_attribute": "name",
    },
    "image_placement_policy": {
        "get_api_instance": get_image_placement_policy_api_instance,
        "list_method": "list_placement_policies",
        "filter_attribute": "name",
    },
    "template": {
        "get_api_instance": get_templates_api_instance,
        "list_method": "list_templates",
        "filter_attribute": "templateName",
    },
    "ova": {
        "get_api_instance": get_ova_api_instance,
        "list_method": "list_ovas",
        "filter_attribute": "name",
    },
    # --- volumes --------------------------------------------------------------
    "volume_group": {
        "get_api_instance": get_vg_api_instance,
        "list_method": "list_volume_groups",
        "filter_attribute": "name",
    },
    "iscsi_client": {
        "get_api_instance": get_iscsi_client_api_instance,
        "list_method": "list_iscsi_clients",
        "filter_attribute": "iscsiInitiatorName",
    },
    # --- prism ----------------------------------------------------------------
    "category": {
        "get_api_instance": get_categories_api_instance,
        "list_method": "list_categories",
        "filter_attribute": "key",
    },
    # --- IAM ------------------------------------------------------------------
    "user": {
        "get_api_instance": get_user_api_instance,
        "list_method": "list_users",
        "filter_attribute": "username",
    },
    "user_group": {
        "get_api_instance": get_user_group_api_instance,
        "list_method": "list_user_groups",
        "filter_attribute": "name",
    },
    "role": {
        "get_api_instance": get_role_api_instance,
        "list_method": "list_roles",
        "filter_attribute": "displayName",
    },
    "operation": {
        "get_api_instance": get_permission_api_instance,
        "list_method": "list_operations",
        "filter_attribute": "displayName",
    },
    "authorization_policy": {
        "get_api_instance": get_authorization_policy_api_instance,
        "list_method": "list_authorization_policies",
        "filter_attribute": "displayName",
    },
    "directory_service": {
        "get_api_instance": get_directory_service_api_instance,
        "list_method": "list_directory_services",
        "filter_attribute": "name",
    },
    "saml_identity_provider": {
        "get_api_instance": get_identity_provider_api_instance,
        "list_method": "list_saml_identity_providers",
        "filter_attribute": "name",
    },
    # --- flow / microsegmentation ---------------------------------------------
    "service_group": {
        "get_api_instance": get_service_groups_api_instance,
        "list_method": "list_service_groups",
        "filter_attribute": "name",
    },
    "address_group": {
        "get_api_instance": get_address_groups_api_instance,
        "list_method": "list_address_groups",
        "filter_attribute": "name",
    },
    "network_security_policy": {
        "get_api_instance": get_network_security_policy_api_instance,
        "list_method": "list_network_security_policies",
        "filter_attribute": "name",
    },
    "entity_group": {
        "get_api_instance": get_entity_groups_api_instance,
        "list_method": "list_entity_groups",
        "filter_attribute": "name",
    },
    # --- data protection ------------------------------------------------------
    "recovery_point": {
        "get_api_instance": get_recovery_point_api_instance,
        "list_method": "list_recovery_points",
        "filter_attribute": "name",
    },
    # --- data policies --------------------------------------------------------
    "protection_policy": {
        "get_api_instance": get_protection_policies_api_instance,
        "list_method": "list_protection_policies",
        "filter_attribute": "name",
    },
    "storage_policy": {
        "get_api_instance": get_storage_policies_api_instance,
        "list_method": "list_storage_policies",
        "filter_attribute": "name",
    },
    # --- objects --------------------------------------------------------------
    "object_store": {
        "get_api_instance": get_objects_api_instance,
        "list_method": "list_objectstores",
        "filter_attribute": "name",
    },
}
