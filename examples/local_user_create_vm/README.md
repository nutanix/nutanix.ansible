## Playbook description
Below is the flow for playbooks:
1. Upload image from local to PC.
2. Create category key-value pair.
3. Create local user.
4. Create authorization policy.
5. Create VM using local user, with image uploaded and guest customization.
6. Power ON the VM.

Tested with:
- Nutanix ansible provider: v2.0
- Prism Central: v2024.3

Sequence to run:
1. Run with user having required permissions: create_local_user_and_entities.yml
2. Check and update cloud_init.yml
3. Run with user created in step 1: create_vm_using_local_user.yml
