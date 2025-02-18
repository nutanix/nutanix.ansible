## Playbook description
The above playbooks are used for creata a local user with access to certain permissions. Then we can create AHV VM using that local user credentials.

Tested with:
- Nutanix ansible provider: v2.0
- Prism Central: v2024.3

Sequence to run:
1. Run with user having required permissions: create_local_user_and_entities.yml
2. Check and update cloud_init.yml
3. Run with user created in step 1: create_vm_using_local_user.yml
