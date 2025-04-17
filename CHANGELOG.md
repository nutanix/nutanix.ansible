## v2.0.0 (7 Jan 2025)

Releasing new modules using PC GA v4 sdks

**New modules:**

Networks:
- ntnx_floating_ips_info_v2
- ntnx_floating_ips_v2
- ntnx_pbrs_v2
- ntnx_pbrs_info_v2
- ntnx_subnets_v2
- ntnx_subnets_info_v2
- ntnx_vpcs_info_v2
- ntnx_vpcs_v2
- ntnx_routes_v2
- ntnx_routes_info_v2
- ntnx_route_tables_info_v2

IAM:
- ntnx_permissions_info_v2
- ntnx_roles_info_v2
- ntnx_roles_v2
- ntnx_roles_v2
- ntnx_roles_info_v2
- ntnx_directory_services_v2
- ntnx_directory_services_info_v2
- ntnx_saml_identity_providers_v2
- ntnx_saml_identity_providers_info_v2
- ntnx_user_groups_v2
- ntnx_user_groups_info_v2
- ntnx_users_v2
- ntnx_users_info_v2
- ntnx_operations_info_v2
- ntnx_authorization_policies_v2
- ntnx_authorization_policies_info_v2

VMM:
- ntnx_images_v2
- ntnx_images_info_v2
- ntnx_image_placement_policies_v2
- ntnx_image_placement_policies_info_v2
- ntnx_vms_ngt_v2
- ntnx_vms_ngt_update_v2
- ntnx_vms_ngt_upgrade_v2
- ntnx_vms_ngt_insert_iso_v2
- ntnx_vms_ngt_info_v2
- ntnx_vms_disks_v2
- ntnx_vms_disks_info_v2
- ntnx_vms_v2
- ntnx_vms_info_v2
- ntnx_vms_categories_v2
- ntnx_vms_nics_v2
- ntnx_vms_nics_info_v2
- ntnx_vms_nics_ip_v2
- ntnx_vms_nics_migrate_v2
- ntnx_vms_cd_rom_v2
- ntnx_vms_cd_rom_info_v2
- ntnx_vms_cd_rom_iso_v2
- ntnx_vms_stage_guest_customization_v2
- ntnx_vms_serial_port_v2
- ntnx_vms_serial_port_info_v2
- ntnx_templates_deploy_v2
- ntnx_templates_guest_os_v2
- ntnx_templates_v2
- ntnx_templates_info_v2
- ntnx_templates_version_v2
- ntnx_templates_versions_info_v2
- ntnx_vms_clone_v2
- ntnx_vms_power_actions_v2
- ntnx_gpus_v2
- ntnx_gpus_info_v2

Prism:
- ntnx_categories_v2
- ntnx_categories_info_v2

Volumes:
- ntnx_volume_groups_v2
- ntnx_volume_groups_info_v2
- ntnx_volume_groups_disks_v2
- ntnx_volume_groups_disks_info_v2
- ntnx_volume_groups_vms_v2
- ntnx_volume_groups_iscsi_clients_v2
- ntnx_volume_groups_iscsi_clients_info_v2

Flow:
- ntnx_security_rules_v2
- ntnx_security_rules_info_v2
- ntnx_service_groups_v2
- ntnx_service_groups_info_v2
- ntnx_address_groups_v2
- ntnx_address_groups_info_v2

Clusters:
- ntnx_clusters_v2
- ntnx_clusters_info_v2
- ntnx_hosts_info_v2
- ntnx_clusters_nodes_v2
- ntnx_nodes_network_info_v2
- ntnx_pc_registration_v2
- ntnx_discover_unconfigured_nodes_v2
- ntnx_storage_containers_stats_v2
- ntnx_storage_containers_info_v2
- ntnx_storage_containers_v2

Data Protection:
- ntnx_recovery_points_info_v2
- ntnx_vm_recovery_point_info_v2
- ntnx_recovery_points_v2
- ntnx_recovery_point_restore_v2
- ntnx_vm_revert_v2
- ntnx_recovery_point_replicate_v2

**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.9.2...v2.0.0)


## v1.9.2 (30 May 2024)


**Breaking Changes:**

- nutanix.ncp collection - Due to all versions of ansible-core less than v2.15.0 are EOL, we are also deprecating support for same and minimum version to use this collection is ansible-core==2.15.0
                            [[\#479](https://github.com/nutanix/nutanix.ansible/issues/479)]

**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.9.1...v1.9.2)


## v1.9.1 (09 November 2023)


**Improvements:**

- docs - [Imprv] add doc regarding running integration tests locally [[\#435](https://github.com/nutanix/nutanix.ansible/issues/435)]
- info modules - [Imprv] add examples for custom_filter  [[\#416](https://github.com/nutanix/nutanix.ansible/issues/416)]
- ndb clones - [Imprv] Enable database clones and clone refresh using latest snapshot flag [[\#391](https://github.com/nutanix/nutanix.ansible/issues/391)]
- ndb clones - [Imprv] add examples for NDB database clone under examples folder [[\#386](https://github.com/nutanix/nutanix.ansible/issues/386)]
- ntnx_prism_vm_inventory - Add support for PC Categories [[\#405](https://github.com/nutanix/nutanix.ansible/issues/405)]
- ntnx_prism_vm_inventory - [Imprv] add examples for dynamic inventory using ntnx_prism_vm_inventory  [[\#401](https://github.com/nutanix/nutanix.ansible/issues/401)]
- ntnx_vms - [Imprv] add possibility to specify / modify vm user ownership and project [[\#378](https://github.com/nutanix/nutanix.ansible/issues/378)]
- ntnx_vms - owner association upon vm creation module [[\#359](https://github.com/nutanix/nutanix.ansible/issues/359)]
- ntnx_vms_info - [Imprv] add examples with guest customization for module ntnx_vms [[\#395](https://github.com/nutanix/nutanix.ansible/issues/395)]

**Bugs:**

- ntnx_foundation - [Bug] Error when Clusters Block is missing in module ntnx_foundation [[\#397](https://github.com/nutanix/nutanix.ansible/issues/397)]
- ntnx_ndb_time_machines_info - [Bug] ntnx_ndb_time_machines_info not fetching all attributes when name is used for fetching [[\#418](https://github.com/nutanix/nutanix.ansible/issues/418)]
- ntnx_security_rules - Fix Syntax Errors in Create App Security Rule Example [[\#394](https://github.com/nutanix/nutanix.ansible/pull/394/files)]
- ntnx_vms - [Bug] Error when updating size_gb using the int filter in module ntnx_vms [[\#400](https://github.com/nutanix/nutanix.ansible/issues/400)]
- ntnx_vms - [Bug] hard_poweroff has been moved to state from operation [[\#415](https://github.com/nutanix/nutanix.ansible/issues/415)]
- ntnx_vms_clone - [Bug] cannot change boot_config when cloning in module ntnx_vms_clone [[\#360](https://github.com/nutanix/nutanix.ansible/issues/359)]
- website - [Bug] Github page deployment action is failing. [[\#483](https://github.com/nutanix/nutanix.ansible/issues/483)]

**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.9.0...v1.9.1)

## v1.9.0 (11 July 2023)


**Improvements:**

- ntnx_profiles_info - [Impr] Develop ansible module for getting available IPs for given network profiles in NDB [\#345](https://github.com/nutanix/nutanix.ansible/issues/345)
- ntnx_security_rules - [Imprv] Flow Network Security Multi-Tier support in Security Policy definition [\#319](https://github.com/nutanix/nutanix.ansible/issues/319)

**Bugs:**

- info modules - [Bug] Multiple filters params are not considered for fetching entities in PC based info modules [[\#352](https://github.com/nutanix/nutanix.ansible/issues/352)]
- ntnx_foundation - [Bug] clusters parameters not being passed to Foundation Server in module nutanix.ncp.ntnx_foundation [[\#307](https://github.com/nutanix/nutanix.ansible/issues/307)]
- ntnx_karbon_clusters - [Bug] error in sample karbon/create_k8s_cluster.yml [[\#349](https://github.com/nutanix/nutanix.ansible/issues/349)]
- ntnx_karbon_clusters - [Bug] impossible to deploy NKE cluster with etcd using disk smaller than 120GB [[\#350](https://github.com/nutanix/nutanix.ansible/issues/350)]
- ntnx_subnets - [Bug] wrong virtual_switch selected in module ntnx_subnets [\#328](https://github.com/nutanix/nutanix.ansible/issues/328)

**New Modules:**

- ntnx_karbon_clusters_node_pools - Create,Update and Delete worker node pools with the provided configuration.
- ntnx_ndb_tags_info - info module for ndb tags info

**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.8.0...v1.9.0)


## v1.8.0 (28 Feb 2023)

**Features**

**Nutanix Database Service (Formerly Era)**

  - Ansible module for clusters info
  - Ansible module for clusters
  - Ansible module for vlans
  - Ansible module for vlans info
  - Ansible module for stretched vlans
  - Ansible module for profiles
  - Ansible module for profiles info
  - Ansible module for slas
  - Ansible module for slas info
  - Ansible module for tags
  - Ansible module for database instances
  - Ansible module for database instance registration
  - Ansible module for database instances info
  - Ansible module for database server vms
  - Ansible module for database server vms info
  - Ansible module for database server vm registration
  - Ansible module for time machine clusters
  - Ansible module for time machines info
  - Ansible module for authorization of database server vm with time machines
  - Ansible module for database clones
  - Ansible module for database clones info
  - Ansible module for database clones refresh
  - Ansible module for snapshots info
  - Ansible module for database snapshots
  - Ansible module for replicating database snapshots
  - Ansible module for log catchups
  - Ansible module for database restore
  - Ansible module for database scale
  - Ansible module for linked databases
  - Ansible module for maintenance windows
  - Ansible module for maintenance windows info
  - Ansible module for maintenance tasks

**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.7.0...v1.8.0)

## v1.8.0-beta.1 (20 Oct 2022)

**Features**

**Nutanix Database Service (Era)**
- Ansible module for Single Instance Databases
- Ansible info module for Database Instances
- Ansible info module for NDB Clusters
- Ansible info module for DB server VMs
- Ansible info module for Profiles
- Ansible info module for SLAs
- Ansible info module for Time Machines
- Ansible info module for Database Clones

**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.7.0...v1.8.0-beta.1)

## v1.7.0 (30 Sep 2022)

**Feature:**
- ntnx_projects - [Feat] Add capability to configure role mappings with collaboration on/off in ntnx_projects [\#252](https://github.com/nutanix/nutanix.ansible/issues/252)

**Bugs:**
- ntnx_projects - [Bug] Clusters and subnets configured in project are not visible in new projects UI [\#283](https://github.com/nutanix/nutanix.ansible/issues/283)
- ntnx_vms - Subnet Name --> UUID Lookup should be PE Cluster Aware [\#260](https://github.com/nutanix/nutanix.ansible/issues/260)
- nutanix.ncp.ntnx_prism_vm_inventory - [Bug] Inventory does not fetch more than 500 Entities [\#228](https://github.com/nutanix/nutanix.ansible/issues/228)

**Improvements:**
- examples - [Imprv] Add version related notes to examples [\#279](https://github.com/nutanix/nutanix.ansible/issues/279)
- examples - [Imprv] Fix IaaS example [\#250](https://github.com/nutanix/nutanix.ansible/issues/250)
- examples - [Imprv] add examples of Images and Static Routes Module [\#256](https://github.com/nutanix/nutanix.ansible/issues/256)
- ntnx_projects - [Imprv] add vpcs and overlay subnets configure capability to module ntnx_projects [\#289](https://github.com/nutanix/nutanix.ansible/issues/289)
- ntnx_vms - [Imprv] add functionality to set network mac_address to module ntnx_vms [\#201](https://github.com/nutanix/nutanix.ansible/issues/201)
- nutanix.ncp.ntnx_prism_vm_inventory - [Imprv] add functionality constructed to module inventory [\#235](https://github.com/nutanix/nutanix.ansible/issues/235)


**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.6.0...v1.7.0)

## v1.6.0 (9 Sep 2022)

**Features**

**Karbon**
- Ansible module for Karbon Clusters
- Ansible info module for Karbon Clusters (with kubeconfig and ssh config)
- Ansible module for Karbon Private Registry
- Ansible info module Karbon Private Registry

**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.5.0...v1.6.0)

## v1.5.0 (26 Aug 2022)

**Features**

**Prism Central Disaster Recovery**
- Ansible module for Protection Rules
- Ansible info module for Protection Rules
- Ansible module for Recovery Plans
- Ansible info module Recovery Plans
- Ansible module for Recovery Plan Jobs
- Ansible info module Recovery Plan Jobs

**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.4.0...v1.5.0)

## v1.4.0 (28 July 2022)

**Features**

**Prism Central**
- Ansible module for Access Control Policy (ACPs)
- Ansible info module for Access Control Policy (ACPs)
- Ansible module for Projects
- Ansible info module for Projects
- Ansible module for Roles
- Ansible info module for Roles
- Ansible info module for Permissions
- Ansible module for Categories
- Ansible info module for Categories
- Ansible module for Address Groups
- Ansible info module for Address Groups
- Ansible module for Service Groups
- Ansible info module for Service Groups
- Ansible module for Users
- Ansible info module for Users
- Ansible module for User Groups
- Ansible info module for User Groups
- Ansible info module for Hosts
- Ansible info module for Clusters

**Bugs**
- Fix examples of info modules [\#226](https://github.com/nutanix/nutanix.ansible/issues/226)

**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.3.0...v1.4.0)

## v1.3.0 (4 July 2022)

**Features**

**Prism Central**
- Ansible module for Image Management
- Ansible info module for Image Management
- Ansible module for Image Placement Policy
- Ansible info module for Image Placement Policies
- Ansible module for Network Security Rules
- Ansible info module for Network Security Rules
- Ansible module for VPC Static Routes
- Ansible info module for VPC Static Routes

## v1.2.0 (3 June 2022)

**Features**

**Prism Central**
- Ansible info module for VM
- Ansible info module for VPC
- Ansible info module for PBR
- Ansible info module for Subnet
- Ansible info module for Floating IPs
- VM's update functionality
- VM's clone functionality
- VM's create OVA image functionality

## v1.1.0 (11 May 2022)

**Features**

**Foundation Cetral**:
- Ansible module for Foundation Central
- Ansible module for API Keys to authenticate with FC
- Ansible info module for API Keys
- Ansible info module for Imaged Clusters
- Ansible info module for Imaged Nodes

**Foundation**:
- Ansible module for Foundation
- Ansible module for BMC IPMI Configuration
- Ansible info module for AOS Packages
- Ansible info module for Discovery Nodes
- Ansible info module for Hypervisor images
- Ansible module for image upload
- Ansible info module for node network

**Automation**:
- Integration tests for Foundation modules
- Integration tests for Foundation Central modules

## v1.1.0-beta.2 (28 Apr 2022)

**Features**

- Ansible module for Foundation Central
- Ansible module for API Keys to authenticate with FC
- Ansible info module for API Keys
- Ansible info module for Imaged Clusters
- Ansible info module for Imaged Nodes

## v1.1.0-beta.1 (11 Apr 2022)

**Features**

- Ansible module for Foundation
- Ansible module for BMC IPMI Configuration
- Ansible info module for AOS Packages
- Ansible info module for Discovery Nodes
- Ansible info module for Hypervisor images
- Ansible module for image upload
- Ansible info module for node network


## v1.0.0 (2nd Mar 2022)

**Improvements**

- Allow environment variables for nutanix connection parameters #128
- Add meta file for collection #134

**Bugs**

- Creating a VM based on a disk_image without specifying the size_gb #127
- icmp "any" code value in module PBR #138


**Full Changelog** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.0.0-beta.2...v1.0.0)


## v1.0.0-beta.2 (22 Feb 2022)

**Features:**

- Feat/VPCs [\#84](https://github.com/nutanix/nutanix.ansible/pull/84)
- Feat/Subnets [\#63](https://github.com/nutanix/nutanix.ansible/pull/63)
- Feat/Floating ips [\#92](https://github.com/nutanix/nutanix.ansible/pull/92)
- Feat/PBRs [\#100](https://github.com/nutanix/nutanix.ansible/pull/100)
- Feat/codegen [\#254](https://github.com/nutanix/nutanix.ansible/pull/119)

**Improvements:**

- Imprv/vpcs network prefix [\#81](https://github.com/nutanix/nutanix.ansible/pull/81)
- Imprv cluster uuid [\#75](https://github.com/nutanix/nutanix.ansible/pull/75)
- Imprv/code coverage [\#97](https://github.com/nutanix/nutanix.ansible/pull/97)

**Bugs:**

- Sanity and python fix [\#46](https://github.com/nutanix/nutanix.ansible/pull/46)
- code cleanup: fix github issue#59 [\#60](https://github.com/nutanix/nutanix.ansible/pull/60)
- Bug/cluster UUID issue68 [\#72](https://github.com/nutanix/nutanix.ansible/pull/72)
- fixed variables names issue74 [\#77](https://github.com/nutanix/nutanix.ansible/pull/77)
- Fix/integ [\#96](https://github.com/nutanix/nutanix.ansible/pull/96)
- fix project name [\#107](https://github.com/nutanix/nutanix.ansible/pull/107)
- Task/fix failing sanity [\#117](https://github.com/nutanix/nutanix.ansible/pull/117)
- clean up pbrs.py [\#113](https://github.com/nutanix/nutanix.ansible/pull/113)

**Full Changelog:** [here](https://github.com/nutanix/nutanix.ansible/compare/v1.0.0-beta.1...v1.0.0-beta.2)


## v1.0.0-beta.1 (28 Jan 2022)

**Features:**

- Ansible module for VMs [\#11](https://github.com/nutanix/nutanix.ansible/pull/11)
- CICD pipeline using GitHub actions [\#22](https://github.com/nutanix/nutanix.ansible/pull/22)

**Bugs:**

- fixes to get spec from collection [\#17](https://github.com/nutanix/nutanix.ansible/pull/17)
- updates for guest customization spec [\#20](https://github.com/nutanix/nutanix.ansible/pull/20)
- clear unused files and argument [\#29](https://github.com/nutanix/nutanix.ansible/pull/29)
- black fixes [\#30](https://github.com/nutanix/nutanix.ansible/pull/30)
- black fixes [\#32](https://github.com/nutanix/nutanix.ansible/pull/32)
- solve python 2.7 issues [\#41](https://github.com/nutanix/nutanix.ansible/pull/41)
- device index calculation fixes, updates for get by name functionality[\#254](https://github.com/nutanix/nutanix.ansible/pull/42)
- Client SDK with inventory [\#45](https://github.com/nutanix/nutanix.ansible/pull/45)
- Fix error messages for get_uuid() reponse [\#47](https://github.com/nutanix/nutanix.ansible/pull/47)

**Full Changelog**: [here](https://github.com/nutanix/nutanix.ansible/commits/v1.0.0-beta.1)
