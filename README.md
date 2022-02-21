# Nutanix Ansible Collection - nutanix.ncp
Ansible collections to automate Nutanix Cloud Platform (ncp).

# Building and installing the collection locally
```
ansible-galaxy collection build
ansible-galaxy collection install nutanix-ncp-1.0.0.tar.gz
```
_Add `--force` option for rebuilding or reinstalling to overwrite existing data_

# Included Content

## Modules

| Name | Description |
| --- | --- |
| ntnx_vms | Create or delete a VM. |
| ntnx_vpcs | Create or delete a VPC. |
| ntnx_subnets | Create or delete a Subnet. |
| ntnx_floating_ips | Create or delete a Floating Ip. |
| ntnx_pbrs | Create or delete a PBR. |

## Inventory Plugins

| Name | Description |
| --- | --- |
| ntnx_vms_inventory | Nutanix VMs inventory source |

# Module documentation and examples
```
ansible-doc nutanix.ncp.<module_name>
```

# Documentation

# How to contribute

# Examples
## Playbook to print name of vms in PC
```
- hosts: localhost
  collections:
  - nutanix.ncp
  tasks:
  - ntnx_vms:
      nutanix_host: '{{config.ip_address}}'
      nutanix_username: '{{credentials.username}}'
      nutanix_password: '{{credentials.password}}'
      validate_certs: False
    register: result
  - debug:
      msg: "{{ result.vms }}"
```
