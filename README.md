# Nutanix Ansible
Official nutanix ansible collection

# About
Nutanix ansible collection <font color=rolyalblue>nutanix.ncp</font> is the official Nutanix ansible collection to automate Nutanix Cloud Platform (ncp).

It is designed keeping simplicity as the core value. Hence it is
1. Easy to use
2. Easy to develop

# Ansible version compatibility
This collection has been tested against following Ansible versions: >=2.12.2.

# Python version compatibility
This collection requires Python 2.7 or greater

# Installing the collection
**Prerequisite**

Ansible should be pre-installed. If not, please follow official ansible [install guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) .

For <font color=royalblue>Developers</font>, please follow [this install guide](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html) for setting up dev environment.

**1. Clone the GitHub repository to a local directory**

```git clone https://github.com/nutanix/nutanix.ansible.git```

**2. Git checkout release version**

```git checkout <release_version> -b <release_version>```

**3. Build the collection**

```ansible-galaxy collection build```

**4. Install the collection**

```ansible-galaxy collection install nutanix-ncp-<version>.tar.gz```

**Note** Add <font color=red>`--force`</font> option for rebuilding or reinstalling to overwrite existing data

# Using this collection
You can either call modules by their Fully Qualified Collection Namespace (FQCN), such as<font color=royalblue> nutanix.ncp.ntnx_vms</font>, or you can call modules by their short name if you list the <font color=royalblue>nutanix.ncp </font>collection in the playbook's ```collections:``` keyword

For example, the playbook for iaas.yml is as follows:
```yaml
---
- name: IaaS Provisioning
  hosts: localhost
  gather_facts: false
  collections:
    - nutanix.ncp
  module_defaults:
    group/nutanix.ncp.ntnx:
      nutanix_host: <host_ip>
      nutanix_username: <user>
      nutanix_password: <pass>
      validate_certs: true
  tasks:
    - include_role:
        name: external_subnet
    - include_role:
        name: vpc
    - include_role:
        name: overlay_subnet
    - include_role:
        name: vm
    - include_role:
        name: fip
```
To run this playbook, use <font color=royalblue>ansible-playbook</font> command as follows:
```
ansible-playbook <playbook_name>
ansible-playbook examples/iaas/iaas.yml
```

# Included Content

## Modules

| Name | Description |
| --- | --- |
| ntnx_vms | Create or delete a VM. |
| ntnx_vpcs | Create or delete a VPC. |
| ntnx_subnets | Create or delete a Subnet. |
| ntnx_floating_ips | Create or delete a Floating Ip. |
| ntnx_pbrs | Create or delete a PBR. |
| ntnx_foundation | Image nodes and create new cluster. |
| ntnx_foundation_bmc_ipmi_config | Configure IPMI IP address on BMC of nodes. |
| ntnx_foundation_aos_packages_info | List the AOS packages uploaded to Foundation. |
| ntnx_foundation_discover_nodes_info | List the nodes discovered by Foundation. |
| ntnx_foundation_hypervisor_images_info | List the hypervisor images uploaded to Foundation. |
| ntnx_foundation_image_upload | Upload hypervisor or AOS image to Foundation VM. |
| ntnx_foundation_node_network_info | Get node network information discovered by Foundation. |

## Inventory Plugins

| Name | Description |
| --- | --- |
| ntnx_vms_inventory | Nutanix VMs inventory source |

# Module documentation and examples
```
ansible-doc nutanix.ncp.<module_name>
```

# How to contribute

We glady welcome contributions from the community. From updating the documentation to adding more functions for Ansible, all ideas are welcome. Thank you in advance for all of your issues, pull requests, and comments!

* [Contributing Guide](CONTRIBUTING.md)
* [Code of Conduct](CODE_OF_CONDUCT.md)

# Examples
## Playbook for IaaS provisioning on Nutanix

**Refer to [`examples/iaas`](https://github.com/nutanix/nutanix.ansible/tree/main/examples/iaas) for full implementation**

```yaml
---
- name: IaaS Provisioning
  hosts: localhost
  gather_facts: false
  collections:
    - nutanix.ncp
  vars:
      nutanix_host: <host_ip>
      nutanix_username: <user>
      nutanix_password: <pass>
      validate_certs: true
  tasks:
    - name: Inputs for external subnets task
      include_tasks: external_subnet.yml
      with_items:
        - { name: Ext-Nat, vlan_id: 102, ip: 10.44.3.192, prefix: 27, gip: 10.44.3.193, sip: 10.44.3.198, eip: 10.44.3.207, eNat: True }

    - name: Inputs for vpcs task
      include_tasks: vpc.yml
      with_items:
      - { name: Prod, subnet_name: Ext-Nat}
      - { name: Dev, subnet_name: Ext-Nat}

    - name: Inputs for overlay subnets
      include_tasks: overlay_subnet.yml
      with_items:
        - { name: Prod-SubnetA, vpc_name: Prod , nip: 10.1.1.0, prefix: 24, gip: 10.1.1.1, sip: 10.1.1.2, eip: 10.1.1.5,
            domain_name: "calm.nutanix.com", dns_servers : ["8.8.8.8","8.8.8.4"], domain_search: ["calm.nutanix.com","eng.nutanix.com"] }
        - { name: Prod-SubnetB, vpc_name: Prod , nip: 10.1.2.0, prefix: 24, gip: 10.1.2.1, sip: 10.1.2.2, eip: 10.1.2.5,
            domain_name: "calm.nutanix.com", dns_servers : ["8.8.8.8","8.8.8.4"], domain_search: ["calm.nutanix.com","eng.nutanix.com"] }
        - { name: Dev-SubnetA, vpc_name:  Dev , nip: 10.1.1.0, prefix: 24, gip: 10.1.1.1, sip: 10.1.1.2, eip: 10.1.1.5,
            domain_name: "calm.nutanix.com", dns_servers : ["8.8.8.8","8.8.8.4"], domain_search: ["calm.nutanix.com","eng.nutanix.com"] }
        - { name: Dev-SubnetB, vpc_name:  Dev , nip: 10.1.2.0, prefix: 24, gip: 10.1.2.1, sip: 10.1.2.2, eip: 10.1.2.5,
            domain_name: "calm.nutanix.com", dns_servers : ["8.8.8.8","8.8.8.4"], domain_search: ["calm.nutanix.com","eng.nutanix.com"] }

    - name: Inputs for vm task
      include_tasks: vm.yml
      with_items:
       - {name: "Prod-Wordpress-App", desc: "Prod-Wordpress-App", is_connected: True , subnet_name: Prod-SubnetA, image_name: "wordpress-appserver", private_ip: ""}
       - {name: "Prod-Wordpress-DB", desc: "Prod-Wordpress-DB", is_connected: True , subnet_name: Prod-SubnetB, image_name: "wordpress-db", private_ip: 10.1.2.5}
       - {name: "Dev-Wordpress-App", desc: "Dev-Wordpress-App", is_connected: True , subnet_name: Dev-SubnetA, image_name: "wordpress-appserver", private_ip: ""}
       - {name: "Dev-Wordpress-DB", desc: "Dev-Wordpress-DB", is_connected: True , subnet_name: Dev-SubnetB, image_name: "wordpress-db",private_ip: 10.1.2.5}

    - name: Inputs for Floating IP task
      include_tasks: fip.yml
      with_items:
        - {vm_name: "Prod-Wordpress-App"}
        - {vm_name: "Dev-Wordpress-App"}

```
