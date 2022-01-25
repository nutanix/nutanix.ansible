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
To Run The Playbook you need Change All Values in vars :

## Playbook to Create Different Vm's
```
---
  - hosts: localhost
    become: true
    collections:
      - nutanix.ncp
    vars:
      credentials:
        username: UserName
        password: Password
      config:
        ip_address: xxx.xxx.xxx.xxx
        port: 9440
      cluster:
        uuid: "0005d632-6a07-32eb-0a75-50a487bc911e"
      networks:
        mannaged:
          name: "test"
          uuid: "ca7fab15-83be-4cca-bc28-88b0b8db293d"
          ip: "10.50.0.11"
      storage_config:
        uuid: "6e78251f-9cf9-45d7-ad16-59274e6f2ea2"
    tasks:
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
              subnet_name: "{{networks.mannaged.name}}"
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