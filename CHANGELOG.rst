=========================
Nutanix.Ncp Release Notes
=========================

.. contents:: Topics

v2.4.0
======

Release Summary
---------------

Built on v4 SDKs. Adds Key Management Server, STIGs, SSL Certificates, Storage Policies, EULA, Dynamic Inventory and Host Inventory modules with several improvements and bug fixes.

Minor Changes
-------------

- All modules - [Imprv] Add logger based on flag to enable debug logs [[\#294](https://github.com/nutanix/nutanix.ansible/issues/294)]
- ntnx_projects - [Imprv] Remove resource limit functionality from ntnx_projects as not supported by API [[\#880](https://github.com/nutanix/nutanix.ansible/issues/880)]
- ntnx_storage_policies_v2 - [Imprv] Add example for storage policy [[\#484](https://github.com/nutanix/nutanix.ansible/issues/484)]
- ntnx_vms - [Imprv] add functionality to provide sysprep or cloud-init to module ntnx_vms via a variable instead of a file [[\#389](https://github.com/nutanix/nutanix.ansible/issues/389)]
- ntnx_vms_cd_rom_iso_v2 - [Imprv] add code enhancement for ntnx_vms_cd_rom_iso_v2 module [[\#827](https://github.com/nutanix/nutanix.ansible/issues/827)]

Breaking Changes / Porting Guide
--------------------------------

- ntnx_projects - [Breaking] Remove resource limit functionality from ntnx_projects as not supported by API [[\#880](https://github.com/nutanix/nutanix.ansible/issues/880)]

Bugfixes
--------

- ntnx_lcm_config_v2 - [Bug] Remove Default Values in module ntnx_lcm_config_v2 [[\#879](https://github.com/nutanix/nutanix.ansible/issues/879)]
- ntnx_prism_vm_inventory - [Bug] Ansible Inventory Plugin is missing project filter [[\#869](https://github.com/nutanix/nutanix.ansible/issues/869)]
- ntnx_prism_vm_inventory - [Bug] Inventory Plugin Category Limitation [[\#846](https://github.com/nutanix/nutanix.ansible/issues/846)]
- ntnx_vms - [Bug] Setting script_path fails in module ncp.ntnx_vms [[\#835](https://github.com/nutanix/nutanix.ansible/issues/835)]
- ntnx_vms_v2 - [Bug] Not able to disable apc_config in module ntnx_vms_v2 [[\#872](https://github.com/nutanix/nutanix.ansible/issues/872)]
- website - [Bug] Github page deployment action is failing. [[\#383](https://github.com/nutanix/nutanix.ansible/issues/383)]

New Plugins
-----------

Inventory
~~~~~~~~~

- nutanix.ncp.ntnx_prism_host_inventory_v2 - Get a list of Nutanix hosts for ansible dynamic inventory using V4 APIs.
- nutanix.ncp.ntnx_prism_vm_inventory_v2 - Get a list of Nutanix VMs for ansible dynamic inventory using V4 APIs.

New Modules
-----------

- nutanix.ncp.ntnx_clusters_categories_v2 - Associate or disassociate categories with a Nutanix cluster
- nutanix.ncp.ntnx_clusters_profile_association_v2 - Associate or disassociate cluster profile with a cluster
- nutanix.ncp.ntnx_clusters_profiles_info_v2 - Fetch information about clusters profiles in Nutanix Prism Central
- nutanix.ncp.ntnx_clusters_profiles_v2 - Create, Update and Delete clusters profiles in Nutanix Prism Central
- nutanix.ncp.ntnx_eula_accept_v2 - Accept the EULA for a specific cluster
- nutanix.ncp.ntnx_eula_info_v2 - Fetch information about the EULA for a specific cluster
- nutanix.ncp.ntnx_key_management_server_info_v2 - Fetch information about key management server in Nutanix Prism Central
- nutanix.ncp.ntnx_key_management_server_v2 - Create, Update and Delete key management server in Nutanix Prism Central
- nutanix.ncp.ntnx_prism_host_inventory_v2 - Get a list of Nutanix hosts for ansible dynamic inventory
- nutanix.ncp.ntnx_prism_vm_inventory_v2 - Get a list of Nutanix hosts for ansible dynamic inventory
- nutanix.ncp.ntnx_ssl_certificates_info_v2 - Fetch information about the SSL certificate for a specific cluster
- nutanix.ncp.ntnx_ssl_certificates_v2 - Update the SSL certificate for a specific cluster
- nutanix.ncp.ntnx_stigs_info_v2 - Get STIGs info in Nutanix Prism Central.
- nutanix.ncp.ntnx_storage_policies_info_v2 - Fetch information about storage policies in Nutanix Prism Central
- nutanix.ncp.ntnx_storage_policies_v2 - Create, Update and Delete storage policies in Nutanix Prism Central

v2.3.0
======

Release Summary
---------------

Built on v4.1 SDKs. Adds OVA management, Password Managers, and VM Disk Migration modules with several improvements and bug fixes.

Minor Changes
-------------

- All info modules - [Imprv] Enhance Info Modules to Return Total Entities Count for Improved Data Retrieval [[\#614](https://github.com/nutanix/nutanix.ansible/issues/614)]
- All modules - [Imprv] add functionality to disable the state which are not applicable for all the modules [[\#746](https://github.com/nutanix/nutanix.ansible/issues/746)]
- ntnx_images_v2 - [Imprv] add complete example playbook for module ntnx_images_v2 covering multiple image sources and operations [[\#718](https://github.com/nutanix/nutanix.ansible/issues/718)]
- ntnx_images_v2 - [Imprv] add tests for creating images and OVAs using Objects Lite Source [[\#717](https://github.com/nutanix/nutanix.ansible/issues/717)]
- ntnx_prism_vm_inventory - [Imprv] add functionality to be able to set a variable when using module ntnx_prism_vm_inventory [[\#644](https://github.com/nutanix/nutanix.ansible/issues/644)]
- ntnx_security_rules_v2 - [Imprv] add support for additional fields in ntnx_security_rules_v2 [[\#719](https://github.com/nutanix/nutanix.ansible/issues/719)]
- ntnx_vms_power_actions_v2 - [Imprv] add examples for module ntnx_vms_power_actions_v2 [[\#727](https://github.com/nutanix/nutanix.ansible/issues/727)]
- ntnx_vms_v2 - [Imprv] add automatic cluster selection verification to ntnx_vms_v2 tests [[\#715](https://github.com/nutanix/nutanix.ansible/issues/715)]
- ntnx_vms_v2 - [Imprv] add functionality to specify project to module ntnx_vms_v2 [[\#690](https://github.com/nutanix/nutanix.ansible/issues/690)]
- ntnx_vms_v2 - [Imprv] add support for additional fields in nics in ntnx_vms_v2 [[\#724](https://github.com/nutanix/nutanix.ansible/issues/724)]
- ntnx_volume_groups_v2 - [Feat] Add update support to ntnx_volume_groups_v2 Ansible module [[\#705](https://github.com/nutanix/nutanix.ansible/issues/705)]
- requirements.txt - [Imprv] Remove extra python packages from the requirements.txt file [[\#785](https://github.com/nutanix/nutanix.ansible/issues/785)]

Bugfixes
--------

- ntnx_clusters_v2 - [Bug] Data type mismatch for categories attribute in module ntnx_clusters_v2 [[\#759](https://github.com/nutanix/nutanix.ansible/issues/759)]
- ntnx_vms_ngt_insert_iso_v2 - [Bug] How to unmount NGT ISO after install? [[\#739](https://github.com/nutanix/nutanix.ansible/issues/739)]
- ntnx_vms_ngt_v2 - [Bug] Documentation is incorrect in module ntnx_vms_ngt_v2 [[\#693](https://github.com/nutanix/nutanix.ansible/issues/693)]

New Modules
-----------

- nutanix.ncp.ntnx_ova_deploy_vm_v2 - Deploy a VM from an OVA in Nutanix Prism Central.
- nutanix.ncp.ntnx_ova_download_v2 - Download an OVA from Nutanix Prism Central.
- nutanix.ncp.ntnx_ova_info_v2 - Fetch information about OVA in Nutanix Prism Central.
- nutanix.ncp.ntnx_ova_v2 - Create, Update and Delete OVA in Nutanix Prism Central.
- nutanix.ncp.ntnx_password_managers_info_v2 - Fetch information about Password Managers in Nutanix Prism Central.
- nutanix.ncp.ntnx_password_managers_v2 - Update Password of System Users in Nutanix Prism Central.
- nutanix.ncp.ntnx_pc_task_abort_v2 - Abort a PC Task in Nutanix Prism Central.
- nutanix.ncp.ntnx_pc_tasks_info_v2 - Fetch information about PC Tasks in Nutanix Prism Central.
- nutanix.ncp.ntnx_vms_disks_migrate_v2 - Migrate disks of a VM in Nutanix Prism Central.

v2.2.0
======

Release Summary
---------------

Releasing new modules for Object Stores, Service Accounts and Several Bugs using PC GA v4.1 sdks

Minor Changes
-------------

- Check mode for delete - [Imprv] add functionality check_mode to module ntnx_vms [[\#334](https://github.com/nutanix/nutanix.ansible/issues/334)]
- Documentation changes - [Imprv] Add detailed doc for using uuid in modules [[\#433](https://github.com/nutanix/nutanix.ansible/issues/433)]
- ntnx_prism_vm_inventory - [Imprv] Add support for retrieving all VMs without specifying length in inventory plugin [[\#651](https://github.com/nutanix/nutanix.ansible/issues/651)]
- ntnx_prism_vm_inventory - [Imprv] Make changes to include project_reference in dynamic inventory for groupping [[\#500](https://github.com/nutanix/nutanix.ansible/issues/500)]
- ntnx_vms_v2 - [Imprv] add functionality uefi boot_order to module ntnx_vms_v2 [[\#579](https://github.com/nutanix/nutanix.ansible/issues/579)]

Bugfixes
--------

- ntnx_acps - [Bug] Fix comparison of old_context_list and update_context_list in module ntnx_acps [[\#475](https://github.com/nutanix/nutanix.ansible/issues/475)]]
- ntnx_prism_vm_inventory - [Bug] API failure is not in shown while creating dynamic inventory [[\#421](https://github.com/nutanix/nutanix.ansible/issues/421)]
- ntnx_prism_vm_inventory - [Bug] Results of VMs is not more then 500 by default in module inventory [[\#354](https://github.com/nutanix/nutanix.ansible/issues/354)]
- ntnx_prism_vm_inventory - [Bug] galaxy.ansible doc for ntnx_prism_vm_inventory is having Documentation Syntax Error. [[\#453](https://github.com/nutanix/nutanix.ansible/issues/453)]
- ntnx_protection_rules - [Bug] Fix invalid OU check in user_groups module [[\#481](https://github.com/nutanix/nutanix.ansible/issues/481)]
- ntnx_security_rules - [Bug] Purpose field mandatory to update the security policy from Ansible in module ntnx_security_rules [[\#485](https://github.com/nutanix/nutanix.ansible/issues/485)]
- ntnx_vmm - [Bug] "not enough positional arguments" in module plugins/modules/ntnx_vmy.py, line 881 [[\#465](https://github.com/nutanix/nutanix.ansible/issues/465)]
- ntnx_vms - [Bug] Attaching image to existing disk in module ntnx_vms [[\#454](https://github.com/nutanix/nutanix.ansible/issues/454)]
- ntnx_vms - [Bug] Cannot assign IP address on an unmanaged network in module ntnx_vms [[\#593](https://github.com/nutanix/nutanix.ansible/issues/593)]
- ntnx_vms_info_v2 - [Bug] Can't fetch all VMs [[\#662](https://github.com/nutanix/nutanix.ansible/issues/662)]
- ntnx_vms_v2 - [Bug] No disk resizing in module ntnx_vms_v2 [[\#578](https://github.com/nutanix/nutanix.ansible/issues/578)]
- ntnx_vms_v2 - [Bug] state absent does not respect --check mode in module nutanix_vms [[\#534](https://github.com/nutanix/nutanix.ansible/issues/534)]
- recovery_plans - [Bug] recovery_plan fails to create in module plugin_modules/prism/recovery_plans.py [[\#515](https://github.com/nutanix/nutanix.ansible/issues/515)]
- v3 modules - [Bug] "Failed to convert API response into JSON" in all modules of Nutanix.ncp ansible collection [[\#490](https://github.com/nutanix/nutanix.ansible/issues/490)]

New Modules
-----------

- nutanix.ncp.ntnx_object_stores_certificate_info_v2 - Fetch information about object stores certificates in Nutanix Prism Central.
- nutanix.ncp.ntnx_object_stores_certificate_v2 - Create, Update and Delete object stores certificates in Nutanix Prism Central.
- nutanix.ncp.ntnx_object_stores_info_v2 - Fetch information about object stores in Nutanix Prism Central.
- nutanix.ncp.ntnx_object_stores_v2 - Create, Update and Delete object stores in Nutanix Prism Central.
- nutanix.ncp.ntnx_users_api_key_info_v2 - Fetch API key information for a Service account user in Nutanix Prism Central.
- nutanix.ncp.ntnx_users_api_key_v2 - Generate or Delete API key for a Service account user in Nutanix Prism Central.
- nutanix.ncp.ntnx_users_revoke_api_key_v2 - Revoke API key for a Service account user in Nutanix Prism Central.
- nutanix.ncp.ntnx_users_v2 - Create Service account in Nutanix Prism Central using ntnx_users_v2 module.

v2.1.1
======

Release Summary
---------------

Releasing this to make it inline with guidelines of Redhat by removing version cap or fixed version from requirements.txt

Bugfixes
--------

- requirements file - [Bug] The entries in the requirements file MUST NOT have a version cap or be fixed [[\#631](https://github.com/nutanix/nutanix.ansible/issues/631)]

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

- nutanix.ncp.ntnx_lcm_config_info_v2 - Fetch LCM Configuration
- nutanix.ncp.ntnx_lcm_config_v2 - Update LCM Configuration
- nutanix.ncp.ntnx_lcm_entities_info_v2 - Fetch LCM Entities Info
- nutanix.ncp.ntnx_lcm_inventory_v2 - Perform Inventory
- nutanix.ncp.ntnx_lcm_prechecks_v2 - Perform LCM Prechecks
- nutanix.ncp.ntnx_lcm_status_info_v2 - Get the LCM framework status.
- nutanix.ncp.ntnx_lcm_upgrades_v2 - Perform LCM upgrades
- nutanix.ncp.ntnx_pc_backup_target_info_v2 - Get PC backup targets info
- nutanix.ncp.ntnx_pc_backup_target_v2 - Create, Update and Delete a PC backup target.
- nutanix.ncp.ntnx_pc_config_info_v2 - Get PC Configuration info
- nutanix.ncp.ntnx_pc_deploy_v2 - Deploys a Prism Central using the provided details
- nutanix.ncp.ntnx_pc_restorable_domain_managers_info_v2 - Fetch restorable domain managers info
- nutanix.ncp.ntnx_pc_restore_points_info_v2 - Fetch pc restore points info
- nutanix.ncp.ntnx_pc_restore_source_info_v2 - Get PC restore source info
- nutanix.ncp.ntnx_pc_restore_source_v2 - Creates or Deletes a restore source pointing to a cluster or object store to restore the domain manager.
- nutanix.ncp.ntnx_pc_restore_v2 - Restores a domain manager(PC) from a cluster or object store backup location based on the selected restore point.
- nutanix.ncp.ntnx_pc_unregistration_v2 - Unregister a PC-PC setup connected using availability zone.
- nutanix.ncp.ntnx_promote_protected_resources_v2 - Module to promote a protected resource in Nutanix Prism Central.
- nutanix.ncp.ntnx_protected_resources_info_v2 - Module to fetch protected resource in Nutanix Prism Central.
- nutanix.ncp.ntnx_protection_policies_info_v2 - Fetch protection policies info in Nutanix Prism Central
- nutanix.ncp.ntnx_protection_policies_v2 - Create, Update, Delete protection policy in Nutanix Prism Central
- nutanix.ncp.ntnx_restore_protected_resources_v2 - Module to restore a protected resource in Nutanix Prism Central.
- nutanix.ncp.ntnx_volume_groups_categories_v2 - Module to associate or disassociate categories with a volume group in Nutanix Prism Central.

v2.0.0
======

Release Summary
---------------

Releasing new modules using PC GA v4 sdks

New Modules
-----------

- nutanix.ncp.ntnx_address_groups_info_v2 - Get address groups info
- nutanix.ncp.ntnx_address_groups_v2 - Create, Update, Delete address groups
- nutanix.ncp.ntnx_authorization_policies_info_v2 - Fetch Authorization policies info from Nutanix PC.
- nutanix.ncp.ntnx_authorization_policies_v2 - Manage Nutanix PC IAM authorization policies
- nutanix.ncp.ntnx_categories_info_v2 - Nutanix PC categories info module
- nutanix.ncp.ntnx_categories_v2 - Manage categories in Nutanix Prism Central
- nutanix.ncp.ntnx_clusters_info_v2 - Retrieve information about Nutanix clusters from PC
- nutanix.ncp.ntnx_clusters_nodes_v2 - Add or Remove nodes from cluster using Nutanix PC
- nutanix.ncp.ntnx_clusters_v2 - Manage Nutanix clusters in Prism Central
- nutanix.ncp.ntnx_directory_services_info_v2 - Fetch directory services info
- nutanix.ncp.ntnx_directory_services_v2 - Module to create, update and delete directory services in Nutanix PC.
- nutanix.ncp.ntnx_discover_unconfigured_nodes_v2 - Discover unconfigured nodes from Nutanix Prism Central
- nutanix.ncp.ntnx_floating_ips_info_v2 - floating_ip info module
- nutanix.ncp.ntnx_floating_ips_v2 - floating_ips module which supports floating_ip CRUD operations
- nutanix.ncp.ntnx_hosts_info_v2 - Retrieve information about Nutanix hosts from PC.
- nutanix.ncp.ntnx_image_placement_policies_info_v2 - Fetches information about Nutanix PC image placement policies.
- nutanix.ncp.ntnx_image_placement_policies_v2 - Manage image placement policies in Nutanix Prism Central
- nutanix.ncp.ntnx_images_info_v2 - Fetch information about Nutanix images
- nutanix.ncp.ntnx_images_v2 - Manage Nutanix Prism Central images.
- nutanix.ncp.ntnx_nodes_network_info_v2 - Get network information for unconfigured cluster nodes
- nutanix.ncp.ntnx_operations_info_v2 - Module to fetch IAM operations info (previously `permissions`)
- nutanix.ncp.ntnx_pbrs_info_v2 - Routing Policies info module
- nutanix.ncp.ntnx_pbrs_v2 - Module for create, update and delete of Policy based routing.
- nutanix.ncp.ntnx_pc_registration_v2 - Registers a domain manager (Prism Central) instance to other entities like PE and PC
- nutanix.ncp.ntnx_recovery_point_replicate_v2 - Replicate recovery points
- nutanix.ncp.ntnx_recovery_point_restore_v2 - Restore recovery points, Creates a clone of the VM/VG from the selected recovery point
- nutanix.ncp.ntnx_recovery_points_info_v2 - Get recovery points info
- nutanix.ncp.ntnx_recovery_points_v2 - Create, Update, Delete  recovery points
- nutanix.ncp.ntnx_roles_info_v2 - Get roles info
- nutanix.ncp.ntnx_roles_v2 - Create, update, and delete roles.
- nutanix.ncp.ntnx_route_tables_info_v2 - Route tables info module
- nutanix.ncp.ntnx_routes_info_v2 - Routes info module
- nutanix.ncp.ntnx_routes_v2 - Module to create, update, and delete routes in route table in VPC
- nutanix.ncp.ntnx_saml_identity_providers_info_v2 - Fetch SAML identity providers from Nutanix PC
- nutanix.ncp.ntnx_saml_identity_providers_v2 - Manage SAML identity providers in Nutanix PC
- nutanix.ncp.ntnx_security_rules_info_v2 - Fetch network security policies info from Nutanix PC.
- nutanix.ncp.ntnx_security_rules_v2 - Manage network security policies in Nutanix Prism Central
- nutanix.ncp.ntnx_service_groups_info_v2 - service_group info module
- nutanix.ncp.ntnx_service_groups_v2 - Create, Update, Delete service groups
- nutanix.ncp.ntnx_storage_containers_info_v2 - Retrieve information about Nutanix storage container from PC
- nutanix.ncp.ntnx_storage_containers_stats_v2 - Retrieve stats about Nutanix storage container from PC
- nutanix.ncp.ntnx_storage_containers_v2 - Manage storage containers in Nutanix Prism Central
- nutanix.ncp.ntnx_subnets_info_v2 - subnet info module
- nutanix.ncp.ntnx_subnets_v2 - subnets module which supports Create, Update, Delete subnets
- nutanix.ncp.ntnx_templates_deploy_v2 - Deploy Nutanix templates
- nutanix.ncp.ntnx_templates_guest_os_v2 - Manage guest OS updates for Nutanix AHV templates.
- nutanix.ncp.ntnx_templates_info_v2 - template info module
- nutanix.ncp.ntnx_templates_v2 - Manage Nutanix AHV template resources
- nutanix.ncp.ntnx_templates_version_v2 - Manage Nutanix template versions
- nutanix.ncp.ntnx_templates_versions_info_v2 - Fetches information about Nutanix template versions.
- nutanix.ncp.ntnx_user_groups_info_v2 - Fetch user groups
- nutanix.ncp.ntnx_user_groups_v2 - Create and Delete user groups
- nutanix.ncp.ntnx_users_info_v2 - Get users info
- nutanix.ncp.ntnx_users_v2 - Module to create and update users from Nutanix PC.
- nutanix.ncp.ntnx_vm_recovery_point_info_v2 - Get VM recovery point info
- nutanix.ncp.ntnx_vm_revert_v2 - Revert VM from recovery point
- nutanix.ncp.ntnx_vms_categories_v2 - Associate or disassociate categories to a VM in AHV Nutanix.
- nutanix.ncp.ntnx_vms_cd_rom_info_v2 - Fetch information about Nutanix VM's CD ROM
- nutanix.ncp.ntnx_vms_cd_rom_iso_v2 - Insert or Eject ISO from CD ROM of Nutanix VMs
- nutanix.ncp.ntnx_vms_cd_rom_v2 - Manage CDROM for Nutanix AHV VMs
- nutanix.ncp.ntnx_vms_clone_v2 - Clone a virtual machine in Nutanix AHV.
- nutanix.ncp.ntnx_vms_disks_info_v2 - Fetch information about Nutanix VM's disks
- nutanix.ncp.ntnx_vms_disks_v2 - Manage disks for Nutanix AHV VMs
- nutanix.ncp.ntnx_vms_info_v2 - Fetch information about Nutanix AHV based PC VMs
- nutanix.ncp.ntnx_vms_ngt_info_v2 - Get Nutanix Guest Tools (NGT) current config for a virtual machine.
- nutanix.ncp.ntnx_vms_ngt_insert_iso_v2 - Insert Nutanix Guest Tools (NGT) ISO into a virtual machine.
- nutanix.ncp.ntnx_vms_ngt_update_v2 - Update Nutanix Guest Tools (NGT) configuration for a VM.
- nutanix.ncp.ntnx_vms_ngt_upgrade_v2 - Upgrade Nutanix Guest Tools on a VM
- nutanix.ncp.ntnx_vms_ngt_v2 - Install or uninstall Nutanix Guest Tools (NGT) on a VM.
- nutanix.ncp.ntnx_vms_nics_info_v2 - Fetch information about Nutanix VM's NICs
- nutanix.ncp.ntnx_vms_nics_ip_v2 - Assign/Release IP to/from Nutanix VM NICs.
- nutanix.ncp.ntnx_vms_nics_v2 - Manage NICs of Nutanix VMs
- nutanix.ncp.ntnx_vms_serial_port_info_v2 - Fetch information about Nutanix VM's serial ports
- nutanix.ncp.ntnx_vms_serial_port_v2 - VM Serial Port module which supports VM serial port CRUD states
- nutanix.ncp.ntnx_vms_stage_guest_customization_v2 - Stage guest customization configuration for a Nutanix VM
- nutanix.ncp.ntnx_vms_v2 - Create, Update and delete VMs in Nutanix AHV based PC
- nutanix.ncp.ntnx_volume_groups_disks_info_v2 - Fetch information about Nutanix PC Volume group disks.
- nutanix.ncp.ntnx_volume_groups_disks_v2 - Manage Nutanix volume group disks
- nutanix.ncp.ntnx_volume_groups_info_v2 - Fetch information about Nutanix PC Volume groups.
- nutanix.ncp.ntnx_volume_groups_iscsi_clients_info_v2 - Fetch ISCSI clients info.
- nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2 - Manage Nutanix volume groups iscsi clients in Nutanix PC.
- nutanix.ncp.ntnx_volume_groups_v2 - Manage Nutanix volume group in PC
- nutanix.ncp.ntnx_volume_groups_vms_v2 - Attach/Detach volume group to AHV VMs in Nutanix PC
- nutanix.ncp.ntnx_vpcs_info_v2 - vpc info module
- nutanix.ncp.ntnx_vpcs_v2 - vpcs module which supports vpc CRUD operations

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

- nutanix.ncp.ntnx_karbon_clusters_node_pools - Create,Update and Delete a worker node pools with the provided configuration.
- nutanix.ncp.ntnx_ndb_tags_info - info module for ndb tags info

v1.8.0
======

New Modules
-----------

- nutanix.ncp.ntnx_ndb_authorize_db_server_vms - module for authorizing db server vm
- nutanix.ncp.ntnx_ndb_clones_info - info module for database clones
- nutanix.ncp.ntnx_ndb_clusters - Create, Update and Delete NDB clusters
- nutanix.ncp.ntnx_ndb_clusters_info - info module for ndb clusters info
- nutanix.ncp.ntnx_ndb_database_clone_refresh - module for database clone refresh.
- nutanix.ncp.ntnx_ndb_database_clones - module for create, update and delete of ndb database clones
- nutanix.ncp.ntnx_ndb_database_log_catchup - module for performing log catchups action
- nutanix.ncp.ntnx_ndb_database_restore - module for restoring database instance
- nutanix.ncp.ntnx_ndb_database_scale - module for scaling database instance
- nutanix.ncp.ntnx_ndb_database_snapshots - module for creating, updating and deleting database snapshots
- nutanix.ncp.ntnx_ndb_databases - Module for create, update and delete of single instance database. Currently, postgres type database is officially supported.
- nutanix.ncp.ntnx_ndb_databases_info - info module for ndb database instances
- nutanix.ncp.ntnx_ndb_db_server_vms - module for create, delete and update of database server vms
- nutanix.ncp.ntnx_ndb_db_servers_info - info module for ndb db server vms info
- nutanix.ncp.ntnx_ndb_linked_databases - module to manage linked databases of a database instance
- nutanix.ncp.ntnx_ndb_maintenance_tasks - module to add and remove maintenance related tasks
- nutanix.ncp.ntnx_ndb_maintenance_window - module to create, update and delete maintenance window
- nutanix.ncp.ntnx_ndb_maintenance_windows_info - module for fetching maintenance windows info
- nutanix.ncp.ntnx_ndb_profiles - module for create, update and delete of profiles
- nutanix.ncp.ntnx_ndb_profiles_info - info module for ndb profiles
- nutanix.ncp.ntnx_ndb_register_database - module for database instance registration
- nutanix.ncp.ntnx_ndb_register_db_server_vm - module for registration of database server vm
- nutanix.ncp.ntnx_ndb_replicate_database_snapshots - module for replicating database snapshots across clusters of time machine
- nutanix.ncp.ntnx_ndb_slas - module for creating, updating and deleting slas
- nutanix.ncp.ntnx_ndb_slas_info - info module for ndb slas
- nutanix.ncp.ntnx_ndb_snapshots_info - info module for ndb snapshots info
- nutanix.ncp.ntnx_ndb_stretched_vlans - Module for create, update and delete of stretched vlan.
- nutanix.ncp.ntnx_ndb_tags - module for create, update and delete of tags
- nutanix.ncp.ntnx_ndb_time_machine_clusters - Module for create, update and delete for data access management in time machines.
- nutanix.ncp.ntnx_ndb_time_machines_info - info module for ndb time machines
- nutanix.ncp.ntnx_ndb_vlans - Module for create, update and delete of ndb vlan.
- nutanix.ncp.ntnx_ndb_vlans_info - info module for ndb vlans

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

- nutanix.ncp.ntnx_karbon_clusters - v4 sdks based module for karbon clusters
- nutanix.ncp.ntnx_karbon_clusters_info - Nutanix info module for karbon clusters with kubeconifg and ssh config
- nutanix.ncp.ntnx_karbon_registries - v4 sdks based module for karbon private registry
- nutanix.ncp.ntnx_karbon_registries_info - Nutanix info module for karbon private registry

v1.5.0
======

New Modules
-----------

- nutanix.ncp.ntnx_protection_rules - v4 sdks based module for protection rules
- nutanix.ncp.ntnx_protection_rules_info - Nutanix info module for protection rules
- nutanix.ncp.ntnx_recovery_plan_jobs - v4 sdks based module for recovery plan jobs
- nutanix.ncp.ntnx_recovery_plan_jobs_info - Nutanix info module for protection
- nutanix.ncp.ntnx_recovery_plans - v4 sdks based module for recovery plan
- nutanix.ncp.ntnx_recovery_plans_info - Nutanix info module for recovery plan

v1.4.0
======

Bugfixes
--------

- Fix examples of info modules [\#226](https://github.com/nutanix/nutanix.ansible/issues/226)

New Modules
-----------

- nutanix.ncp.ntnx_acps - acp module which suports acp Create, update and delete operations
- nutanix.ncp.ntnx_acps_info - acp info module
- nutanix.ncp.ntnx_address_groups - module which supports address groups CRUD operations
- nutanix.ncp.ntnx_address_groups_info - address groups info module
- nutanix.ncp.ntnx_categories - category module which supports pc category management CRUD operations
- nutanix.ncp.ntnx_categories_info - categories info module
- nutanix.ncp.ntnx_clusters_info - cluster info module
- nutanix.ncp.ntnx_hosts_info - host  info module
- nutanix.ncp.ntnx_permissions_info - permissions info module
- nutanix.ncp.ntnx_projects - module for create, update and delete pc projects
- nutanix.ncp.ntnx_projects_info - projects info module
- nutanix.ncp.ntnx_roles - module which supports role CRUD operations
- nutanix.ncp.ntnx_roles_info - role info module
- nutanix.ncp.ntnx_service_groups - service_groups module which suports service_groups CRUD operations
- nutanix.ncp.ntnx_service_groups_info - service_group info module
- nutanix.ncp.ntnx_user_groups - user_groups module which supports pc user_groups management create delete operations
- nutanix.ncp.ntnx_user_groups_info - User Groups info module
- nutanix.ncp.ntnx_users - users module which supports pc users management create delete operations
- nutanix.ncp.ntnx_users_info - users info module

v1.3.0
======

New Modules
-----------

- nutanix.ncp.ntnx_image_placement_policies_info - image placement policies info module
- nutanix.ncp.ntnx_image_placement_policy - image placement policy module which supports Create, update and delete operations
- nutanix.ncp.ntnx_images - images module which supports pc images management CRUD operations
- nutanix.ncp.ntnx_images_info - images info module
- nutanix.ncp.ntnx_security_rules - security_rule module which suports security_rule CRUD operations
- nutanix.ncp.ntnx_security_rules_info - security_rule info module
- nutanix.ncp.ntnx_static_routes - vpc static routes
- nutanix.ncp.ntnx_static_routes_info - vpc static routes info module

v1.2.0
======

Minor Changes
-------------

- VM's update functionality

New Modules
-----------

- nutanix.ncp.ntnx_floating_ips_info - Nutanix info module for floating Ips
- nutanix.ncp.ntnx_pbrs_info - Nutanix info module for policy based routing
- nutanix.ncp.ntnx_subnets_info - Nutanix info module for subnets
- nutanix.ncp.ntnx_vms_clone - VM module which supports VM clone operations
- nutanix.ncp.ntnx_vms_info - Nutanix info module for vms
- nutanix.ncp.ntnx_vms_ova - VM module which supports ova creation
- nutanix.ncp.ntnx_vpcs_info - Nutanix info module for vpcs

v1.1.0
======

Minor Changes
-------------

- Added integration tests for foundation and foundation central

New Modules
-----------

- nutanix.ncp.ntnx_foundation - Nutanix module to image nodes and optionally create clusters
- nutanix.ncp.ntnx_foundation_bmc_ipmi_config - Nutanix module which configures IPMI IP address on BMC of nodes.
- nutanix.ncp.ntnx_foundation_central - Nutanix module to imaged Nodes and optionally create cluster
- nutanix.ncp.ntnx_foundation_central_api_keys - Nutanix module which creates api key for foundation central
- nutanix.ncp.ntnx_foundation_central_api_keys_info - Nutanix module which returns the api key
- nutanix.ncp.ntnx_foundation_central_imaged_clusters_info - Nutanix module which returns the imaged clusters within the Foundation Central
- nutanix.ncp.ntnx_foundation_central_imaged_nodes_info - Nutanix module which returns the imaged nodes within the Foundation Central
- nutanix.ncp.ntnx_foundation_discover_nodes_info - Nutanix module which returns nodes discovered by Foundation
- nutanix.ncp.ntnx_foundation_hypervisor_images_info - Nutanix module which returns the hypervisor images uploaded to Foundation
- nutanix.ncp.ntnx_foundation_image_upload - Nutanix module which uploads hypervisor or AOS image to foundation vm.
- nutanix.ncp.ntnx_foundation_node_network_info - Nutanix module which returns node network information discovered by Foundation

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
- Fix error messages for get_uuid() reponse [\#47](https://github.com/nutanix/nutanix.ansible/pull/47)
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

- nutanix.ncp.ntnx_floating_ips - v4 sdks based module for floating Ips
- nutanix.ncp.ntnx_pbrs - v4 sdks based module for policy based routing
- nutanix.ncp.ntnx_subnets - v4 sdks based module for subnets
- nutanix.ncp.ntnx_vms - v4 sdks based module for vms
- nutanix.ncp.ntnx_vpcs - v4 sdks based module for vpcs
