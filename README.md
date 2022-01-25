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
Make sure to use the correct values that matches your environment for all the variables.

Create playbook.yml with the content as below, and run it using 
```
ansible-playbook playbook.yml
```
## Playbook to Create Different Vm's
```
---
- hosts: localhost
  collections:
    - nutanix.ncp
  vars:
    credentials:
      username: UserName
      password: Password
    config:
      ip_address: XXX.XXX.XXX.XXX
      port: 9440
    cluster:
      uuid: "0005d578-2faf-9fb6-3c07-ac1f6b6f9780"
    networks:
      static:
        name: "static_subnet"
        uuid: "72c5057d-93f7-4389-a01a-2c2f42eae3ef"
        ip: "10.30.30.72"
    storage_config:
      uuid: "4446ca0b-7846-4a6f-b00a-386736432121"
  tasks:
    - name: Create vm from image
      nutanix.ncp.nutanix_vms:
        state: present
        name: image_vm
        timezone: "UTC"
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
        cluster:
          cluster_uuid: "{{cluster.uuid}}"
        disks:
          - type: "DISK"
            clone_image: "CentOS-7-cloudinit"
            bus: "SCSI"
      register: result
      #ignore_errors: True
    - name: VM with Cluster , Network, UTC time zone, one Disk
      nutanix_vms:
        state: present
        name: "Cluster Network and Disk"
        timezone: "UTC"
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
        cluster:
          cluster_uuid: "{{cluster.uuid}}"
        networks:
          - connected: True
            subnet_name: "{{networks.static.name}}"
        disks:
          - type: "DISK"
            size_gb: 5
            bus: "PCI"
      register: result
      ignore_errors: True
    - name: VM with Cluster, different Disks, memory size
      nutanix_vms:
        state: present
        name: "Different disks"
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
        cluster:
          cluster_uuid: "{{cluster.uuid}}"
        disks:
          - type: "DISK"
            size_gb: 4
            bus: "SATA"
          - type: "DISK"
            size_gb: 3
            bus: "SCSI"
        memory_gb: 20
      register: result
      ignore_errors: True
    - name: VM with Cluster, different CDROMS
      nutanix_vms:
        state: present
        name: "CDROM"
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
        cluster:
          cluster_uuid: "{{cluster.uuid}}"
        disks:
          - type: "CDROM"
            bus: "SATA"
          - type: "CDROM"
            bus: "IDE"
        cores_per_vcpu: 1
      register: result
      ignore_errors: True
    - name: delete recently created vm
      nutanix_vms:
        uuid: '{{ result["response"]["metadata"]["uuid"] }}'
        state: absent
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
      register: result
    - name: VM with all specification
      nutanix_vms:
        state: present
        name: "All specification"
        timezone: "GMT"
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
        cluster:
          cluster_uuid: "{{cluster.uuid}}"
        disks:
          - type: "DISK"
            size_gb: 1
            bus: "SCSI"
          - type: "DISK"
            size_gb: 4
            bus: "PCI"
          - type: "DISK"
            size_gb: 16
            bus: "SATA"
          - type: "DISK"
            size_gb: 16
            bus: "SCSI"
          - type: "CDROM"
            size_gb: 4
            bus: "IDE"
        boot_device_order_list:
          - "DISK"
          - "CDROM"
          - "NETWORK"
        vcpus: 20
        cores_per_vcpu: 4
        memory_gb: 6
      register: result
      ignore_errors: True
```