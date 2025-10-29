=========================
Nutanix.Ncp Release Notes
=========================

.. contents:: Topics

v2.3.0
======

Release Summary
---------------

This release introduces new modules for OVA and Password Management in Nutanix Prism Central, along with major improvements and bug fixes across multiple modules. Built on v4.1 APIs/SDKs.

New Modules
-----------

- ntnx_ova_v2 - Create, Update and Delete OVA in Nutanix Prism Central.
- ntnx_ova_info_v2 - Fetch information about OVA in Nutanix Prism Central.
- ntnx_ova_deploy_vm_v2 - Deploy a VM from an OVA in Nutanix Prism Central.
- ntnx_ova_download_v2 - Download an OVA from Nutanix Prism Central.
- ntnx_password_managers_info_v2 - Fetch information about Password Managers in Nutanix Prism Central.
- ntnx_password_managers_v2 - Update Password of System Users in Nutanix Prism Central.
- ntnx_pc_tasks_info_v2 - Fetch information about PC Tasks in Nutanix Prism Central.
- ntnx_pc_task_abort_v2 - Abort a PC Task in Nutanix Prism Central.
- ntnx_vms_disks_migrate_v2 - Migrate disks of a VM in Nutanix Prism Central.

Bugfixes
--------

- ntnx_vms_ngt_v2 - [Bug] Documentation is incorrect in module ntnx_vms_ngt_v2 [https://github.com/nutanix/nutanix.ansible/issues/693]
- ntnx_vms_ngt_insert_iso_v2 - [Bug] How to unmount NGT ISO after install? [https://github.com/nutanix/nutanix.ansible/issues/739]
- ntnx_clusters_v2 - [Bug] Data type mismatch for categories attribute in module ntnx_clusters_v2 [https://github.com/nutanix/nutanix.ansible/issues/759]

Minor Changes
-------------

- ntnx_security_rules_v2 - [Imprv] add support for additional fields in ntnx_security_rules_v2 [https://github.com/nutanix/nutanix.ansible/issues/719]
- ntnx_vms_power_actions_v2 - [Imprv] add examples for module ntnx_vms_power_actions_v2 [https://github.com/nutanix/nutanix.ansible/issues/727]
- ntnx_volume_groups_v2 - [Feat] Add update support to ntnx_volume_groups_v2 Ansible module [https://github.com/nutanix/nutanix.ansible/issues/705]
- ntnx_vms_v2 - [Imprv] add automatic cluster selection verification to ntnx_vms_v2 tests [https://github.com/nutanix/nutanix.ansible/issues/715]
- ntnx_vms_v2 - [Imprv] add functionality to specify project to module ntnx_vms_v2 [https://github.com/nutanix/nutanix.ansible/issues/690]
- ntnx_vms_v2 - [Imprv] add support for additional fields in nics in ntnx_vms_v2 [https://github.com/nutanix/nutanix.ansible/issues/724]
- ntnx_images_v2 - [Imprv] add tests for creating images and OVAs using Objects Lite Source [https://github.com/nutanix/nutanix.ansible/issues/717]
- ntnx_images_v2 - [Imprv] add complete example playbook for module ntnx_images_v2 covering multiple image sources and operations [https://github.com/nutanix/nutanix.ansible/issues/718]
- All info modules - [Imprv] Enhance Info Modules to Return Total Entities Count for Improved Data Retrieval [https://github.com/nutanix/nutanix.ansible/issues/614]
- All modules - [Imprv] add functionality to disable the state which are not applicable for all the modules [https://github.com/nutanix/nutanix.ansible/issues/746]
- ntnx_prism_vm_inventory - [Imprv] add functionality to be able to set a variable when using module ntnx_prism_vm_inventory [https://github.com/nutanix/nutanix.ansible/issues/644]
- requirements.txt - [Imprv] Remove extra python packages from the requirements.txt file [https://github.com/nutanix/nutanix.ansible/issues/785]

v2.2.0
======

Release Summary
---------------

Releasing new modules for Object Stores, Service Accounts and Several Bugs using PC GA v4.1 sdks

New Modules
-----------

- ntnx_users_v2 - Create Service account in Nutanix Prism Central using ntnx_users_v2 module.
- ntnx_users_api_key_v2 - Generate or Delete API key for a Service account user in Nutanix Prism Central.
- ntnx_users_api_key_info_v2 - Fetch API key information for a Service account user in Nutanix Prism Central.
- ntnx_users_revoke_api_key_v2 - Revoke API key for a Service account user in Nutanix Prism Central.
- ntnx_object_stores_v2 - Create, Update and Delete object stores in Nutanix Prism Central.
- ntnx_object_stores_info_v2 - Fetch information about object stores in Nutanix Prism Central.
- ntnx_object_stores_certificate_v2 - Create, Update and Delete object stores certificates in Nutanix Prism Central.
- ntnx_object_stores_certificate_info_v2 - Fetch information about object stores certificates in Nutanix Prism Central.

Bugfixes
--------

- ntnx_acps - [Bug] Fix comparison of old_context_list and update_context_list in module ntnx_acps [https://github.com/nutanix/nutanix.ansible/issues/475]
- ntnx_prism_vm_inventory - [Bug] API failure is not in shown while creating dynamic inventory [https://github.com/nutanix/nutanix.ansible/issues/421]
- ntnx_prism_vm_inventory - [Bug] Results of VMs is not more then 500 by default in module inventory [https://github.com/nutanix/nutanix.ansible/issues/354]
- ntnx_prism_vm_inventory - [Bug] galaxy.ansible doc for ntnx_prism_vm_inventory is having Documentation Syntax Error. [https://github.com/nutanix/nutanix.ansible/issues/453]
- ntnx_protection_rules - [Bug] Fix invalid OU check in user_groups module [https://github.com/nutanix/nutanix.ansible/issues/481]
- ntnx_security_rules - [Bug] Purpose field mandatory to update the security policy from Ansible in module ntnx_security_rules [https://github.com/nutanix/nutanix.ansible/issues/485]
- ntnx_vmm - [Bug] "not enough positional arguments" in module plugins/modules/ntnx_vmy.py, line 881 [https://github.com/nutanix/nutanix.ansible/issues/465]
- ntnx_vms - [Bug] Attaching image to existing disk in module ntnx_vms [https://github.com/nutanix/nutanix.ansible/issues/454]
- ntnx_vms - [Bug] Cannot assign IP address on an unmanaged network in module ntnx_vms [https://github.com/nutanix/nutanix.ansible/issues/593]
- ntnx_vms_info_v2 - [Bug] Can't fetch all VMs [https://github.com/nutanix/nutanix.ansible/issues/662]
- ntnx_vms_v2 - [Bug] No disk resizing in module ntnx_vms_v2 [https://github.com/nutanix/nutanix.ansible/issues/578]
- ntnx_vms_v2 - [Bug] state absent does not respect --check mode in module nutanix_vms [https://github.com/nutanix/nutanix.ansible/issues/534]
- recovery_plans - [Bug] recovery_plan fails to create in module plugin_modules/prism/recovery_plans.py [https://github.com/nutanix/nutanix.ansible/issues/515]
- v3 modules - [Bug] "Failed to convert API response into JSON" in all modules of Nutanix.ncp ansible collection [https://github.com/nutanix/nutanix.ansible/issues/490]

Minor Changes
-------------

- Check mode for delete - [Imprv] add functionality check_mode to module ntnx_vms [https://github.com/nutanix/nutanix.ansible/issues/334]
- Documentation changes - [Imprv] Add detailed doc for using uuid in modules [https://github.com/nutanix/nutanix.ansible/issues/433]
- ntnx_prism_vm_inventory - [Imprv] Add support for retrieving all VMs without specifying length in inventory plugin [https://github.com/nutanix/nutanix.ansible/issues/651]
- ntnx_prism_vm_inventory - [Imprv] Make changes to include project_reference in dynamic inventory for groupping [https://github.com/nutanix/nutanix.ansible/issues/500]
- ntnx_vms_v2 - [Imprv] add functionality uefi boot_order to module ntnx_vms_v2 [https://github.com/nutanix/nutanix.ansible/issues/579]

v2.1.1
======

Release Summary
---------------

Releasing this to make it inline with guidelines of Redhat by removing version cap or fixed version from requirements.txt

Bugfixes
--------

- requirements file - [Bug] The entries in the requirements file MUST NOT have a version cap or be fixed [https://github.com/nutanix/nutanix.ansible/issues/631]

v2.1.0
======

Release Summary
---------------

Releasing new modules for Prism, Data Protection, Data Policies, LCM and Volumes using PC GA v4 sdks

Breaking Changes / Porting Guide
--------------------------------

- nutanix.ncp collection - We are deprecating support for ansible-core==2.15.0 and minimum version to use this collection is ansible-core==2.16.0.

New Modules
-----------

- ntnx_lcm_config_info_v2 - Fetch LCM Configuration
- ntnx_lcm_config_v2 - Update LCM Configuration
- ntnx_lcm_entities_info_v2 - Fetch LCM Entities Info
- ntnx_lcm_inventory_v2 - Perform Inventory
- ntnx_lcm_prechecks_v2 - Perform LCM Prechecks
- ntnx_lcm_status_info_v2 - Get the LCM framework status.
- ntnx_lcm_upgrades_v2 - Perform LCM upgrades
- ntnx_pc_backup_target_info_v2 - Get PC backup targets info
- ntnx_pc_backup_target_v2 - Create, Update and Delete a PC backup target.
- ntnx_pc_config_info_v2 - Get PC Configuration info
- ntnx_pc_deploy_v2 - Deploys a Prism Central using the provided details
- ntnx_pc_restorable_domain_managers_info_v2 - Fetch restorable domain managers info
- ntnx_pc_restore_points_info_v2 - Fetch pc restore points info
- ntnx_pc_restore_source_info_v2 - Get PC restore source info
- ntnx_pc_restore_source_v2 - Creates or Deletes a restore source pointing to a cluster or object store to restore the domain manager.
- ntnx_pc_restore_v2 - Restores a domain manager(PC) from a cluster or object store backup location based on the selected restore point.
- ntnx_pc_unregistration_v2 - Unregister a PC-PC setup connected using availability zone.
- ntnx_promote_protected_resources_v2 - Module to promote a protected resource in Nutanix Prism Central.
- ntnx_protected_resources_info_v2 - Module to fetch protected resource in Nutanix Prism Central.
- ntnx_protection_policies_info_v2 - Fetch protection policies info in Nutanix Prism Central
- ntnx_protection_policies_v2 - Create, Update, Delete protection policy in Nutanix Prism Central
- ntnx_restore_protected_resources_v2 - Module to restore a protected resource in Nutanix Prism Central.
- ntnx_volume_groups_categories_v2 - Module to associate or disassociate categories with a volume group in Nutanix Prism Central.

v2.0.0
======

Release Summary
---------------

Releasing new modules using PC GA v4 sdks

New Modules
-----------

- ntnx_address_groups_info_v2 - Get address groups info
- ntnx_address_groups_v2 - Create, Update, Delete address groups
- ntnx_authorization_policies_info_v2 - Fetch Authorization policies info from Nutanix PC.
- ntnx_authorization_policies_v2 - Manage Nutanix PC IAM authorization policies
- ntnx_categories_info_v2 - Nutanix PC categories info module
- ntnx_categories_v2 - Manage categories in Nutanix Prism Central
- ntnx_clusters_info_v2 - Retrieve information about Nutanix clusters from PC
- ntnx_clusters_nodes_v2 - Add or Remove nodes from cluster using Nutanix PC
- ntnx_clusters_v2 - Manage Nutanix clusters in Prism Central
- ntnx_directory_services_info_v2 - Fetch directory services info
- ntnx_directory_services_v2 - Module to create, update and delete directory services in Nutanix PC.
- ntnx_discover_unconfigured_nodes_v2 - Discover unconfigured nodes from Nutanix Prism Central
- ntnx_floating_ips_info_v2 - floating_ip info module
- ntnx_floating_ips_v2 - floating_ips module which supports floating_ip CRUD operations
- ntnx_hosts_info_v2 - Retrieve information about Nutanix hosts from PC.
- ntnx_image_placement_policies_info_v2 - Fetches information about Nutanix PC image placement policies.
- ntnx_image_placement_policies_v2 - Manage image placement policies in Nutanix Prism Central
- ntnx_images_info_v2 - Fetch information about Nutanix images
- ntnx_images_v2 - Manage Nutanix Prism Central images.
- ntnx_nodes_network_info_v2 - Get network information for unconfigured cluster nodes
- ntnx_operations_info_v2 - Module to fetch IAM operations info (previously `permissions`)
- ntnx_pbrs_info_v2 - Routing Policies info module
- ntnx_pbrs_v2 - Module for create, update and delete of Policy based routing.
- ntnx_pc_registration_v2 - Registers a domain manager (Prism Central) instance to other entities like PE and PC
- ntnx_recovery_point_replicate_v2 - Replicate recovery points
- ntnx_recovery_point_restore_v2 - Restore recovery points, Creates a clone of the VM/VG from the selected recovery point
- ntnx_recovery_points_info_v2 - Get recovery points info
- ntnx_recovery_points_v2 - Create, Update, Delete  recovery points
- ntnx_roles_info_v2 - Get roles info
- ntnx_roles_v2 - Create, update, and delete roles.
- ntnx_route_tables_info_v2 - Route tables info module
- ntnx_routes_info_v2 - Routes info module
- ntnx_routes_v2 - Module to create, update, and delete routes in route table in VPC
- ntnx_saml_identity_providers_info_v2 - Fetch SAML identity providers from Nutanix PC
- ntnx_saml_identity_providers_v2 - Manage SAML identity providers in Nutanix PC
- ntnx_security_rules_info_v2 - Fetch network security policies info from Nutanix PC.
- ntnx_security_rules_v2 - Manage network security policies in Nutanix Prism Central
- ntnx_service_groups_info_v2 - service_group info module
- ntnx_service_groups_v2 - Create, Update, Delete service groups
- ntnx_storage_containers_info_v2 - Retrieve information about Nutanix storage container from PC
- ntnx_storage_containers_stats_v2 - Retrieve stats about Nutanix storage container from PC
- ntnx_storage_containers_v2 - Manage storage containers in Nutanix Prism Central
- ntnx_subnets_info_v2 - subnet info module
- ntnx_subnets_v2 - subnets module which supports Create, Update, Delete subnets
- ntnx_templates_deploy_v2 - Deploy Nutanix templates
- ntnx_templates_guest_os_v2 - Manage guest OS updates for Nutanix AHV templates.
- ntnx_templates_info_v2 - template info module
- ntnx_templates_v2 - Manage Nutanix AHV template resources
- ntnx_templates_version_v2 - Manage Nutanix template versions
- ntnx_templates_versions_info_v2 - Fetches information about Nutanix template versions.
- ntnx_user_groups_info_v2 - Fetch user groups
- ntnx_user_groups_v2 - Create and Delete user groups
- ntnx_users_info_v2 - Get users info
- ntnx_users_v2 - Module to create and update users from Nutanix PC.
- ntnx_vm_recovery_point_info_v2 - Get VM recovery point info
- ntnx_vm_revert_v2 - Revert VM from recovery point
- ntnx_vms_categories_v2 - Associate or disassociate categories to a VM in AHV Nutanix.
- ntnx_vms_cd_rom_info_v2 - Fetch information about Nutanix VM's CD ROM
- ntnx_vms_cd_rom_iso_v2 - Insert or Eject ISO from CD ROM of Nutanix VMs
- ntnx_vms_cd_rom_v2 - Manage CDROM for Nutanix AHV VMs
- ntnx_vms_clone_v2 - Clone a virtual machine in Nutanix AHV.
- ntnx_vms_disks_info_v2 - Fetch information about Nutanix VM's disks
- ntnx_vms_disks_v2 - Manage disks for Nutanix AHV VMs
- ntnx_vms_info_v2 - Fetch information about Nutanix AHV based PC VMs
- ntnx_vms_ngt_info_v2 - Get Nutanix Guest Tools (NGT) current config for a virtual machine.
- ntnx_vms_ngt_insert_iso_v2 - Insert Nutanix Guest Tools (NGT) ISO into a virtual machine.
- ntnx_vms_ngt_update_v2 - Update Nutanix Guest Tools (NGT) configuration for a VM.
- ntnx_vms_ngt_upgrade_v2 - Upgrade Nutanix Guest Tools on a VM
- ntnx_vms_ngt_v2 - Install or uninstall Nutanix Guest Tools (NGT) on a VM.
- ntnx_vms_nics_info_v2 - Fetch information about Nutanix VM's NICs
- ntnx_vms_nics_ip_v2 - Assign/Release IP to/from Nutanix VM NICs.
- ntnx_vms_nics_v2 - Manage NICs of Nutanix VMs
- ntnx_vms_serial_port_info_v2 - Fetch information about Nutanix VM's serial ports
- ntnx_vms_serial_port_v2 - VM Serial Port module which supports VM serial port CRUD states
- ntnx_vms_stage_guest_customization_v2 - Stage guest customization configuration for a Nutanix VM
- ntnx_vms_v2 - Create, Update and delete VMs in Nutanix AHV based PC
- ntnx_volume_groups_disks_info_v2 - Fetch information about Nutanix PC Volume group disks.
- ntnx_volume_groups_disks_v2 - Manage Nutanix volume group disks
- ntnx_volume_groups_info_v2 - Fetch information about Nutanix PC Volume groups.
- ntnx_volume_groups_iscsi_clients_info_v2 - Fetch ISCSI clients info.
- ntnx_volume_groups_iscsi_clients_v2 - Manage Nutanix volume groups iscsi clients in Nutanix PC.
- ntnx_volume_groups_v2 - Manage Nutanix volume group in PC
- ntnx_volume_groups_vms_v2 - Attach/Detach volume group to AHV VMs in Nutanix PC
- ntnx_vpcs_info_v2 - vpc info module
- ntnx_vpcs_v2 - vpcs module which supports vpc CRUD operations

v1.9.2
======

Release Summary
---------------

Deprecating support for ansible-core less than v2.15.0

Breaking Changes / Porting Guide
--------------------------------

- nutanix.ncp collection - Due to all versions of ansible-core version less than v2.15.0 are EOL, we are also deprecating support for same and minimum version to use this collection is ansible-core==2.15.0. [https://github.com/nutanix/nutanix.ansible/issues/479]

v1.9.1
======

Release Summary
---------------

This release included bug fixes and improvement.

Minor Changes
-------------

- docs - [Imprv] add doc regarding running integration tests locally [https://github.com/nutanix/nutanix.ansible/issues/435]
- info modules - [Imprv] add examples for custom_filter  [https://github.com/nutanix/nutanix.ansible/issues/416]
- ndb clones - [Imprv] Enable database clones and clone refresh using latest snapshot flag [https://github.com/nutanix/nutanix.ansible/issues/391]
- ndb clones - [Imprv] add examples for NDB database clone under examples folder [https://github.com/nutanix/nutanix.ansible/issues/386]
- ntnx_prism_vm_inventory - Add support for PC Categories [https://github.com/nutanix/nutanix.ansible/issues/405]
- ntnx_prism_vm_inventory - [Imprv] add examples for dynamic inventory using ntnx_prism_vm_inventory  [https://github.com/nutanix/nutanix.ansible/issues/401]
- ntnx_vms - [Imprv] add possibility to specify / modify vm user ownership and project [https://github.com/nutanix/nutanix.ansible/issues/378]
- ntnx_vms - owner association upon vm creation module [https://github.com/nutanix/nutanix.ansible/issues/359]
- ntnx_vms_info - [Imprv] add examples with guest customization for module ntnx_vms [https://github.com/nutanix/nutanix.ansible/issues/395]

Bugfixes
--------

- ntnx_foundation - [Bug] Error when Clusters Block is missing in module ntnx_foundation [https://github.com/nutanix/nutanix.ansible/issues/397]
- ntnx_ndb_time_machines_info - [Bug] ntnx_ndb_time_machines_info not fetching all attributes when name is used for fetching [https://github.com/nutanix/nutanix.ansible/issues/418]
- ntnx_security_rules - Fix Syntax Errors in Create App Security Rule Example [https://github.com/nutanix/nutanix.ansible/pull/394/files]
- ntnx_vms - [Bug] Error when updating size_gb using the int filter in module ntnx_vms [https://github.com/nutanix/nutanix.ansible/issues/400]
- ntnx_vms - [Bug] hard_poweroff has been moved to state from operation [https://github.com/nutanix/nutanix.ansible/issues/415]
- ntnx_vms_clone - [Bug] cannot change boot_config when cloning in module ntnx_vms_clone [https://github.com/nutanix/nutanix.ansible/issues/359]
- website - [Bug] Github page deployment action is failing. [https://github.com/nutanix/nutanix.ansible/issues/483]

v1.9.0
======

Minor Changes
-------------

- ntnx_profiles_info - [Impr] Develop ansible module for getting available IPs for given network profiles in NDB [https://github.com/nutanix/nutanix.ansible/issues/345]
- ntnx_security_rules - [Imprv] Flow Network Security Multi-Tier support in Security Policy definition [https://github.com/nutanix/nutanix.ansible/issues/319]

Deprecated Features
-------------------

- ntnx_security_rules - The ``apptier`` option in target group has been removed. New option called ``apptiers`` has been added to support multi tier policy.

Bugfixes
--------

- info modules - [Bug] Multiple filters params are not considered for fetching entities in PC based info modules [https://github.com/nutanix/nutanix.ansible/issues/352]
- ntnx_foundation - [Bug] clusters parameters not being passed to Foundation Server in module nutanix.ncp.ntnx_foundation [https://github.com/nutanix/nutanix.ansible/issues/307]
- ntnx_karbon_clusters - [Bug] error in sample karbon/create_k8s_cluster.yml [https://github.com/nutanix/nutanix.ansible/issues/349]
- ntnx_karbon_clusters - [Bug] impossible to deploy NKE cluster with etcd using disk smaller than 120GB [https://github.com/nutanix/nutanix.ansible/issues/350]
- ntnx_subnets - [Bug] wrong virtual_switch selected in module ntnx_subnets [https://github.com/nutanix/nutanix.ansible/issues/328]

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
- ntnx_ndb_slas - module for creating, updating and deleting slas
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

- examples - [Imprv] Add version related notes to examples [https://github.com/nutanix/nutanix.ansible/issues/279]
- examples - [Imprv] Fix IaaS example [https://github.com/nutanix/nutanix.ansible/issues/250]
- examples - [Imprv] add examples of Images and Static Routes Module [https://github.com/nutanix/nutanix.ansible/issues/256]
- ntnx_projects - [Feat] Add capability to configure role mappings with collaboration on/off in ntnx_projects [https://github.com/nutanix/nutanix.ansible/issues/252]
- ntnx_projects - [Imprv] add vpcs and overlay subnets configure capability to module ntnx_projects [https://github.com/nutanix/nutanix.ansible/issues/289]
- ntnx_vms - [Imprv] add functionality to set network mac_address to module ntnx_vms [https://github.com/nutanix/nutanix.ansible/issues/201]
- nutanix.ncp.ntnx_prism_vm_inventory - [Imprv] add functionality constructed to module inventory [https://github.com/nutanix/nutanix.ansible/issues/235]

Bugfixes
--------

- ntnx_projects - [Bug] Clusters and subnets configured in project are not visible in new projects UI [https://github.com/nutanix/nutanix.ansible/issues/283]
- ntnx_vms - Subnet Name --> UUID Lookup should be PE Cluster Aware [https://github.com/nutanix/nutanix.ansible/issues/260]
- nutanix.ncp.ntnx_prism_vm_inventory - [Bug] Inventory does not fetch more than 500 Entities [https://github.com/nutanix/nutanix.ansible/issues/228]

v1.6.0
======

New Modules
-----------

- ntnx_karbon_clusters - v4 sdks based module for karbon clusters
- ntnx_karbon_clusters_info - Nutanix info module for karbon clusters with kubeconifg and ssh config
- ntnx_karbon_registries - v4 sdks based module for karbon private registry
- ntnx_karbon_registries_info - Nutanix info module for karbon private registry

v1.5.0
======

New Modules
-----------

- ntnx_protection_rules - v4 sdks based module for protection rules
- ntnx_protection_rules_info - Nutanix info module for protection rules
- ntnx_recovery_plan_jobs - v4 sdks based module for recovery plan jobs
- ntnx_recovery_plan_jobs_info - Nutanix info module for protection
- ntnx_recovery_plans - v4 sdks based module for recovery plan
- ntnx_recovery_plans_info - Nutanix info module for recovery plan

v1.4.0
======

Bugfixes
--------

- Fix examples of info modules [https://github.com/nutanix/nutanix.ansible/issues/226]

New Modules
-----------

- ntnx_acps - acp module which suports acp Create, update and delete operations
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
- ntnx_service_groups - service_groups module which suports service_groups CRUD operations
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
- ntnx_security_rules - security_rule module which suports security_rule CRUD operations
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
- Imprv cluster uuid [https://github.com/nutanix/nutanix.ansible/pull/75]
- Imprv/code coverage [https://github.com/nutanix/nutanix.ansible/pull/97]
- Imprv/vpcs network prefix [https://github.com/nutanix/nutanix.ansible/pull/81]

Bugfixes
--------

- Bug/cluster UUID issue68 [https://github.com/nutanix/nutanix.ansible/pull/72]
- Client SDK with inventory [https://github.com/nutanix/nutanix.ansible/pull/45]
- Creating a VM based on a disk_image without specifying the size_gb
- Fix error messages for get_uuid() reponse [https://github.com/nutanix/nutanix.ansible/pull/47]
- Fix/integ [https://github.com/nutanix/nutanix.ansible/pull/96]
- Sanity and python fix [https://github.com/nutanix/nutanix.ansible/pull/46]
- Task/fix failing sanity [https://github.com/nutanix/nutanix.ansible/pull/117]
- black fixes [https://github.com/nutanix/nutanix.ansible/pull/30]
- black fixes [https://github.com/nutanix/nutanix.ansible/pull/32]
- clean up pbrs.py [https://github.com/nutanix/nutanix.ansible/pull/113]
- clear unused files and argument [https://github.com/nutanix/nutanix.ansible/pull/29]
- code cleanup - fix github issue#59 [https://github.com/nutanix/nutanix.ansible/pull/60]
- device index calculation fixes, updates for get by name functionality[https://github.com/nutanix/nutanix.ansible/pull/42]
- fix project name [https://github.com/nutanix/nutanix.ansible/pull/107]
- fixed variables names issue74 [https://github.com/nutanix/nutanix.ansible/pull/77]
- fixes to get spec from collection [https://github.com/nutanix/nutanix.ansible/pull/17]
- icmp "any" code value in module PBR
- solve python 2.7 issues [https://github.com/nutanix/nutanix.ansible/pull/41]
- updates for guest customization spec [https://github.com/nutanix/nutanix.ansible/pull/20]

New Modules
-----------

- ntnx_floating_ips - v4 sdks based module for floating Ips
- ntnx_pbrs - v4 sdks based module for policy based routing
- ntnx_subnets - v4 sdks based module for subnets
- ntnx_vms - v4 sdks based module for vms
- ntnx_vpcs - v4 sdks based module for vpcs
