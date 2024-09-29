=========================
Nutanix.Ncp Release Notes
=========================

.. contents:: Topics

v1.9.2
======

Release Summary
---------------

Deprecating support for ansible-core less than v2.15.0

Breaking Changes / Porting Guide
--------------------------------

- nutanix.ncp collection - Due to all versions of ansible-core version less than v2.15.0 are EOL, we are also deprecating support for same and minimum version to use this collection is ansible-core==2.15.0. [[\#479](https://github.com/nutanix/nutanix.ansible/issues/479)]

v1.9.1
======

Release Summary
---------------

This release included bug fixes and improvement.

Minor Changes
-------------

- docs - [Imprv] add doc regarding running integration tests locally [[\#435](https://github.com/nutanix/nutanix.ansible/issues/435)]
- info modules - [Imprv] add examples for custom_filter  [[\#416](https://github.com/nutanix/nutanix.ansible/issues/416)]
- ndb clones - [Imprv] Enable database clones and clone refresh using latest snapshot flag [[\#391](https://github.com/nutanix/nutanix.ansible/issues/391)]
- ndb clones - [Imprv] add examples for NDB database clone under examples folder [[\#386](https://github.com/nutanix/nutanix.ansible/issues/386)]
- ntnx_prism_vm_inventory - Add support for PC Categories [[\#405](https://github.com/nutanix/nutanix.ansible/issues/405)]
- ntnx_prism_vm_inventory - [Imprv] add examples for dynamic inventory using ntnx_prism_vm_inventory  [[\#401](https://github.com/nutanix/nutanix.ansible/issues/401)]
- ntnx_vms - [Imprv] add possibility to specify / modify vm user ownership and project [[\#378](https://github.com/nutanix/nutanix.ansible/issues/378)]
- ntnx_vms - owner association upon vm creation module [[\#359](https://github.com/nutanix/nutanix.ansible/issues/359)]
- ntnx_vms_info - [Imprv] add examples with guest customization for module ntnx_vms [[\#395](https://github.com/nutanix/nutanix.ansible/issues/395)]

Bugfixes
--------

- ntnx_foundation - [Bug] Error when Clusters Block is missing in module ntnx_foundation [[\#397](https://github.com/nutanix/nutanix.ansible/issues/397)]
- ntnx_ndb_time_machines_info - [Bug] ntnx_ndb_time_machines_info not fetching all attributes when name is used for fetching [[\#418](https://github.com/nutanix/nutanix.ansible/issues/418)]
- ntnx_security_rules - Fix Syntax Errors in Create App Security Rule Example [[\#394](https://github.com/nutanix/nutanix.ansible/pull/394/files)]
- ntnx_vms - [Bug] Error when updating size_gb using the int filter in module ntnx_vms [[\#400](https://github.com/nutanix/nutanix.ansible/issues/400)]
- ntnx_vms - [Bug] hard_poweroff has been moved to state from operation [[\#415](https://github.com/nutanix/nutanix.ansible/issues/415)]
- ntnx_vms_clone - [Bug] cannot change boot_config when cloning in module ntnx_vms_clone [[\#360](https://github.com/nutanix/nutanix.ansible/issues/359)]
- website - [Bug] Github page deployment action is failing. [[\#483](https://github.com/nutanix/nutanix.ansible/issues/483)]

v1.9.0
======

Minor Changes
-------------

- ntnx_profiles_info - [Impr] Develop ansible module for getting available IPs for given network profiles in NDB [\#345](https://github.com/nutanix/nutanix.ansible/issues/345)
- ntnx_security_rules - [Imprv] Flow Network Security Multi-Tier support in Security Policy definition [\#319](https://github.com/nutanix/nutanix.ansible/issues/319)

Deprecated Features
-------------------

- ntnx_security_rules - The ``apptier`` option in target group has been removed. New option called ``apptiers`` has been added to support multi tier policy.

Bugfixes
--------

- info modules - [Bug] Multiple filters params are not considered for fetching entities in PC based info modules [[\#352](https://github.com/nutanix/nutanix.ansible/issues/352)]
- ntnx_foundation - [Bug] clusters parameters not being passed to Foundation Server in module nutanix.ncp.ntnx_foundation [[\#307](https://github.com/nutanix/nutanix.ansible/issues/307)]
- ntnx_karbon_clusters - [Bug] error in sample karbon/create_k8s_cluster.yml [[\#349](https://github.com/nutanix/nutanix.ansible/issues/349)]
- ntnx_karbon_clusters - [Bug] impossible to deploy NKE cluster with etcd using disk smaller than 120GB [[\#350](https://github.com/nutanix/nutanix.ansible/issues/350)]
- ntnx_subnets - [Bug] wrong virtual_switch selected in module ntnx_subnets [\#328](https://github.com/nutanix/nutanix.ansible/issues/328)

New Modules
-----------

- ntnx_karbon_clusters_node_pools - Create,Update and Delete a worker node pools with the provided configuration.
- ntnx_ndb_tags_info - info module for ndb tags info

v1.8.0
======

New Modules
-----------

- ntnx_ndb_authorize_db_server_vms - module for authorizing db server vm
- ntnx_ndb_clones_info - info module for database clones
- ntnx_ndb_clusters - Create, Update and Delete NDB clusters
- ntnx_ndb_clusters_info - info module for ndb clusters info
- ntnx_ndb_database_clone_refresh - module for database clone refresh.
- ntnx_ndb_database_clones - module for create, update and delete of ndb database clones
- ntnx_ndb_database_log_catchup - module for performing log catchups action
- ntnx_ndb_database_restore - module for restoring database instance
- ntnx_ndb_database_scale - module for scaling database instance
- ntnx_ndb_database_snapshots - module for creating, updating and deleting database snapshots
- ntnx_ndb_databases - Module for create, update and delete of single instance database. Currently, postgres type database is officially supported.
- ntnx_ndb_databases_info - info module for ndb database instances
- ntnx_ndb_db_server_vms - module for create, delete and update of database server vms
- ntnx_ndb_db_servers_info - info module for ndb db server vms info
- ntnx_ndb_linked_databases - module to manage linked databases of a database instance
- ntnx_ndb_maintenance_tasks - module to add and remove maintenance related tasks
- ntnx_ndb_maintenance_window - module to create, update and delete maintenance window
- ntnx_ndb_maintenance_windows_info - module for fetching maintenance windows info
- ntnx_ndb_profiles - module for create, update and delete of profiles
- ntnx_ndb_profiles_info - info module for ndb profiles
- ntnx_ndb_register_database - module for database instance registration
- ntnx_ndb_register_db_server_vm - module for registration of database server vm
- ntnx_ndb_replicate_database_snapshots - module for replicating database snapshots across clusters of time machine
- ntnx_ndb_slas - moudle for creating, updating and deleting slas
- ntnx_ndb_slas_info - info module for ndb slas
- ntnx_ndb_snapshots_info - info module for ndb snapshots info
- ntnx_ndb_stretched_vlans - Module for create, update and delete of stretched vlan.
- ntnx_ndb_tags - module for create, update and delete of tags
- ntnx_ndb_time_machine_clusters - Module for create, update and delete for data access management in time machines.
- ntnx_ndb_time_machines_info - info module for ndb time machines
- ntnx_ndb_vlans - Module for create, update and delete of ndb vlan.
- ntnx_ndb_vlans_info - info module for ndb vlans

v1.7.0
======

Minor Changes
-------------

- examples - [Imprv] Add version related notes to examples [\#279](https://github.com/nutanix/nutanix.ansible/issues/279)
- examples - [Imprv] Fix IaaS example [\#250](https://github.com/nutanix/nutanix.ansible/issues/250)
- examples - [Imprv] add examples of Images and Static Routes Module [\#256](https://github.com/nutanix/nutanix.ansible/issues/256)
- ntnx_projects - [Feat] Add capability to configure role mappings with collaboration on/off in ntnx_projects [\#252](https://github.com/nutanix/nutanix.ansible/issues/252)
- ntnx_projects - [Imprv] add vpcs and overlay subnets configure capability to module ntnx_projects [\#289](https://github.com/nutanix/nutanix.ansible/issues/289)
- ntnx_vms - [Imprv] add functionality to set network mac_address to module ntnx_vms [\#201](https://github.com/nutanix/nutanix.ansible/issues/201)
- nutanix.ncp.ntnx_prism_vm_inventory - [Imprv] add functionality constructed to module inventory [\#235](https://github.com/nutanix/nutanix.ansible/issues/235)

Bugfixes
--------

- ntnx_projects - [Bug] Clusters and subnets configured in project are not visible in new projects UI [\#283](https://github.com/nutanix/nutanix.ansible/issues/283)
- ntnx_vms - Subnet Name --> UUID Lookup should be PE Cluster Aware [\#260](https://github.com/nutanix/nutanix.ansible/issues/260)
- nutanix.ncp.ntnx_prism_vm_inventory - [Bug] Inventory does not fetch more than 500 Entities [[\#228](https://github.com/nutanix/nutanix.ansible/issues/228)]

v1.6.0
======

New Modules
-----------

- ntnx_karbon_clusters - Nutanix module for karbon clusters
- ntnx_karbon_clusters_info - Nutanix info module for karbon clusters with kubeconifg and ssh config
- ntnx_karbon_registries - Nutanix module for karbon private registry
- ntnx_karbon_registries_info - Nutanix info module for karbon private registry

v1.5.0
======

New Modules
-----------

- ntnx_protection_rules - Nutanix module for protection rules
- ntnx_protection_rules_info - Nutanix info module for protection rules
- ntnx_recovery_plan_jobs - Nutanix module for recovery plan jobs
- ntnx_recovery_plan_jobs_info - Nutanix info module for protection
- ntnx_recovery_plans - Nutanix module for recovery plan
- ntnx_recovery_plans_info - Nutanix info module for recovery plan

v1.4.0
======

Bugfixes
--------

- Fix examples of info modules [\#226](https://github.com/nutanix/nutanix.ansible/issues/226)

New Modules
-----------

- ntnx_acps - acp module which supports acp Create, update and delete operations
- ntnx_acps_info - acp info module
- ntnx_address_groups - module which supports address groups CRUD operations
- ntnx_address_groups_info - address groups info module
- ntnx_categories - category module which supports pc category management CRUD operations
- ntnx_categories_info - categories info module
- ntnx_clusters_info - cluster info module
- ntnx_hosts_info - host  info module
- ntnx_permissions_info - permissions info module
- ntnx_projects - module for create, update and delete pc projects
- ntnx_projects_info - projects info module
- ntnx_roles - module which supports role CRUD operations
- ntnx_roles_info - role info module
- ntnx_service_groups - service_groups module which supports service_groups CRUD operations
- ntnx_service_groups_info - service_group info module
- ntnx_user_groups - user_groups module which supports pc user_groups management create delete operations
- ntnx_user_groups_info - User Groups info module
- ntnx_users - users module which supports pc users management create delete operations
- ntnx_users_info - users info module

v1.3.0
======

New Modules
-----------

- ntnx_image_placement_policies_info - image placement policies info module
- ntnx_image_placement_policy - image placement policy module which supports Create, update and delete operations
- ntnx_images - images module which supports pc images management CRUD operations
- ntnx_images_info - images info module
- ntnx_security_rules - security_rule module which supports security_rule CRUD operations
- ntnx_security_rules_info - security_rule info module
- ntnx_static_routes - vpc static routes
- ntnx_static_routes_info - vpc static routes info module

v1.2.0
======

Minor Changes
-------------

- VM's update functionality

New Modules
-----------

- ntnx_floating_ips_info - Nutanix info module for floating Ips
- ntnx_pbrs_info - Nutanix info module for policy based routing
- ntnx_subnets_info - Nutanix info module for subnets
- ntnx_vms_clone - VM module which supports VM clone operations
- ntnx_vms_info - Nutanix info module for vms
- ntnx_vms_ova - VM module which supports ova creation
- ntnx_vpcs_info - Nutanix info module for vpcs

v1.1.0
======

Minor Changes
-------------

- Added integration tests for foundation and foundation central

New Modules
-----------

- ntnx_foundation - Nutanix module to image nodes and optionally create clusters
- ntnx_foundation_bmc_ipmi_config - Nutanix module which configures IPMI IP address on BMC of nodes.
- ntnx_foundation_central - Nutanix module to imaged Nodes and optionally create cluster
- ntnx_foundation_central_api_keys - Nutanix module which creates api key for foundation central
- ntnx_foundation_central_api_keys_info - Nutanix module which returns the api key
- ntnx_foundation_central_imaged_clusters_info - Nutanix module which returns the imaged clusters within the Foundation Central
- ntnx_foundation_central_imaged_nodes_info - Nutanix module which returns the imaged nodes within the Foundation Central
- ntnx_foundation_discover_nodes_info - Nutanix module which returns nodes discovered by Foundation
- ntnx_foundation_hypervisor_images_info - Nutanix module which returns the hypervisor images uploaded to Foundation
- ntnx_foundation_image_upload - Nutanix module which uploads hypervisor or AOS image to foundation vm.
- ntnx_foundation_node_network_info - Nutanix module which returns node network information discovered by Foundation

v1.0.0
======

Major Changes
-------------

- CICD pipeline using GitHub actions

Minor Changes
-------------

- Add meta file for collection
- Allow environment variables for nutanix connection parameters
- Codegen - Ansible code generator
- Imprv cluster uuid [\#75](https://github.com/nutanix/nutanix.ansible/pull/75)
- Imprv/code coverage [\#97](https://github.com/nutanix/nutanix.ansible/pull/97)
- Imprv/vpcs network prefix [\#81](https://github.com/nutanix/nutanix.ansible/pull/81)

Bugfixes
--------

- Bug/cluster UUID issue68 [\#72](https://github.com/nutanix/nutanix.ansible/pull/72)
- Client SDK with inventory [\#45](https://github.com/nutanix/nutanix.ansible/pull/45)
- Creating a VM based on a disk_image without specifying the size_gb
- Fix error messages for get_uuid() response [\#47](https://github.com/nutanix/nutanix.ansible/pull/47)
- Fix/integ [\#96](https://github.com/nutanix/nutanix.ansible/pull/96)
- Sanity and python fix [\#46](https://github.com/nutanix/nutanix.ansible/pull/46)
- Task/fix failing sanity [\#117](https://github.com/nutanix/nutanix.ansible/pull/117)
- black fixes [\#30](https://github.com/nutanix/nutanix.ansible/pull/30)
- black fixes [\#32](https://github.com/nutanix/nutanix.ansible/pull/32)
- clean up pbrs.py [\#113](https://github.com/nutanix/nutanix.ansible/pull/113)
- clear unused files and argument [\#29](https://github.com/nutanix/nutanix.ansible/pull/29)
- code cleanup - fix github issue#59 [\#60](https://github.com/nutanix/nutanix.ansible/pull/60)
- device index calculation fixes, updates for get by name functionality[\#254](https://github.com/nutanix/nutanix.ansible/pull/42)
- fix project name [\#107](https://github.com/nutanix/nutanix.ansible/pull/107)
- fixed variables names issue74 [\#77](https://github.com/nutanix/nutanix.ansible/pull/77)
- fixes to get spec from collection [\#17](https://github.com/nutanix/nutanix.ansible/pull/17)
- icmp "any" code value in module PBR
- solve python 2.7 issues [\#41](https://github.com/nutanix/nutanix.ansible/pull/41)
- updates for guest customization spec [\#20](https://github.com/nutanix/nutanix.ansible/pull/20)

New Modules
-----------

- ntnx_floating_ips - Nutanix module for floating Ips
- ntnx_pbrs - Nutanix module for policy based routing
- ntnx_subnets - Nutanix module for subnets
- ntnx_vms - Nutanix module for vms
- ntnx_vpcs - Nutanix module for vpcs
