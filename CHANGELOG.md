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
