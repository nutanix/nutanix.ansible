## v1.8.0-beta.1 (20 Oct 2022)

**Features**

**Nutanix Database Service (Era)**
- Ansible module for Single Instance Databases
- Ansible info module Database Instances
- Ansible info module NDB Clusters
- Ansible info module DB server VMs
- Ansible info module Profiles
- Ansible info module SLAs
- Ansible info module Time Machines
- Ansible info module Database Clones

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
