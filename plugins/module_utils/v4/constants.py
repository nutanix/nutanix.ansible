# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class NutanixFiles:

    API_REQUEST_TIMEOUT_SECS = 30


class Tasks:
    TASK_SERVICE = "ergon"

    class RelEntityType:
        """Relation Entity Types for the task entities affected"""

        FLOATING_IPS = "networking:config:floating-ips"
        VM = "vmm:ahv:config:vm"
        IMAGES = "vmm:content:image"
        IMAGE_PLACEMENT_POLICY = "vmm:images:config:placement-policy"
        TEMPLATES = "vmm:content:template"
        VOLUME_GROUP = "volumes:config:volume-group"
        VOLUME_GROUP_DISK = "volumes:config:volume-group:disk"
        ISCSI_CLIENT = "volumes:config:iscsi-client"
        VPC = "networking:config:vpc"
        SUBNET = "networking:config:subnet"
        FLOATING_IP = "networking:config:floating-ip"
        PBRS = "networking:config:routing-policy"
        SECURITY_POLICY = "microseg:config:policy"
        SERVICE_GROUP = "microseg:config:service-group"
        ADDRESS_GROUP = "microseg:config:address-group"
        VM_DISK = "vmm:ahv:config:vm:disk"
        CD_ROM = "vmm:ahv:config:vm:cdrom"
        SERIAL_PORT = "vmm:ahv:config:vm:serialport"
        VM_NIC = "vmm:ahv:config:vm:nic"
        RECOVERY_POINT = "dataprotection:config:recovery-point"
        VM_RECOVERY_POINT = "dataprotection:config:vm-recovery-point"
        STORAGE_CONTAINER = "clustermgmt:config:storage-containers"
        ROUTE = "networking:config:route"
        OBJECTS = "objects:config:object-store"
        OVA = "vmm:content:ova"
        STORAGE_POLICY = "datapolicies:config:storage-policy"
        KMS = "security:encryption:key-management-server"
        CLUSTER_PROFILE = "clustermgmt:config:cluster-profile"
        NETWORK_FUNCTION = "Networking:config:network-function"
        ENTITY_GROUP = "microseg:config:entity-group"

    class CompletetionDetailsName:
        """Completion details name for the task entities affected"""

        RECOVERY_POINT = "recoveryPointExtId"
        VM_EXT_IDS = "vmExtIds"
        VG_EXT_IDS = "volumeGroupExtIds"
        PROTECTION_POLICY = "protectionPolicyExtId"
