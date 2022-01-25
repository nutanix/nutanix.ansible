# Nutanix Ansible Collection - nutanix.ncp
Ansible collections to automate Nutanix Cloud Platform (ncp).

# Building and installing the collection locally
```
ansible-galaxy collection build
ansible-galaxy collection install nutanix-ncp-1.0.0.tar.gz
```

##or

### Installing the collection from GitHub repository
```
ansible-galaxy collection install git+https://github.com/nutanix/nutanix.ansible.git#nutanix,<branch>
```
_Add `--force` option for rebuilding or reinstalling to overwrite existing data_

# Included modules
```
nutanix_vms
```



# Module documentation and examples
```
ansible-doc nutanix.ncp.<module_name>
```

# Examples
## Playbook to print name of vms in PC
```
- hosts: localhost
  collections:
  - nutanix.ncp
  tasks:
 - name: create VM with Minimum Requiremnts
   nutanix_vms:
      state: present
      name: "MinVm"
      auth:
        credentials: "{{credentials}}"
        url: "{{config.ip_address}}:{{config.port}}"
      cluster:
        cluster_uuid: "{{cluster.uuid}}"
      
   register: result
  - debug:
      msg: "{{ result.response.status.state }}"
```