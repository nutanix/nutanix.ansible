## Design Goals - Simplicity

- Easy to use
- Easy to develop

**Easy to use**

- Don't mimick API spec. Ansible spec should be a simplified version of API spec.
- Goal is to expose *minimum attributes* to create, update or delete the entity.
- Keep backward & forward compatibility in mind when creating ansible spec.

**Easy to develop**

- Three things need to develop a module:

    a. [Module spec](https://github.com/nutanix/nutanix.ansible/blob/main/plugins/modules/ntnx_subnets_v2.py#L606) inside `get_module_spec()`, spec for running the API via sdk.

    Example:
    ```
    def get_module_spec():
        dhcp_spec = dict(...)
        metadata_spec = dict(...)

        module_args = dict(
            ext_id=dict(type="str"),
            name=dict(type="str"),
            description=dict(type="str"),
            subnet_type=dict(type="str", choices=["OVERLAY", "VLAN"]),
            network_id=dict(type="int"),
            dhcp_options=dict(type="dict", options=dhcp_spec, obj=net_sdk.DhcpOptions),
            metadata=dict(type="dict", options=metadata_spec, obj=net_sdk.Metadata),
        )
        return module_args
    ```

    b. [Bootstrap code](https://github.com/nutanix/nutanix.ansible/blob/main/plugins/modules/ntnx_subnets_v2.py#L705) for creating and deleting entity.
    Use v4 sdks which are available on [v4-documentation](https://developers.nutanix.com/api-reference?namespace=networking&version=v4.0) in creation, updation or deletion.

    c. [Ansible module](https://github.com/nutanix/nutanix.ansible/blob/main/plugins/modules/ntnx_subnets_v2.py) plugin with [`run_module()`](https://github.com/nutanix/nutanix.ansible/blob/main/plugins/modules/ntnx_subnets_v2.py#L832) implementation.

    Example:
    ```
    def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            (
                "state",
                "present",
                ("ext_id", "cluster_reference", "vpc_reference"),
                True,
            ),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_subnet(module, result)
        else:
            create_subnet(module, result)
    else:
        delete_subnet(module, result)
    module.exit_json(**result)
    ```

## Spec generator

The `generate_spec` method is designed to populate a specification object (`obj`) based on input attributes (`attr`) and additional keyword arguments (`kwargs`). Here's a brief breakdown of how it works:

1. **Type Check**: Ensures the obj is a valid object.

2. **Module Arguments**: Retrieves module arguments from kwargs or uses a default set.

3. **Attributes**: If attr is not provided, it defaults to a deep copy of self.module.params.

4. **Attribute Processing**: Iterates over each key in module_args and processes it based on its type:
    - **Dynamic Objects**: Handles attributes with dynamic objects.
    
    - **Dict Type**: Recursively creates spec objects for dictionary-type attributes.

    - **List Type**: Recursively creates a list of spec objects for list-type attributes.

    - **Other Types**: Directly assigns the attribute value to the spec object.

**Usage:**

To use the `generate_spec` method, follow these steps:

1. **Create a Spec Object**: Define the spec object that needs to be populated.

2. **Define Attributes**: Prepare the attributes dictionary that contains the values to be assigned to the spec object.

3. **Call the Method**: Invoke the `generate_spec` method with the spec object and attributes.

**Example**

Here's an example of how to use the `generate_spec` method:

For Create Opearation:
```
sg = SpecGenerator(module)
default_spec = net_sdk.Subnet()  // Root Node
spec, err = sg.generate_spec(obj=default_spec)
```
For Update Operation:
```
current_spec = get_subnet(module, subnets, ext_id=ext_id) // Fetch the current spec
sg = SpecGenerator(module)
update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
```

## Workflow

1. Create a github issue with following details
 * **Title** should contain <font color="red">one of</font> the follwoing
    - [Feat] Develop ansible module for \<api_name>
    - [Imprv] Modify ansible module to support \<new_functionality>
    - [Bug] Fix \<summary of issue> bug in \<ansible_module_name>
 * **Labels** should contain <font color="red">one of</font> the following
    - **feature**
    - **enhancement**
    - **bug**
    - **test**

 * **Project** should be selected
 * **Assignees** - assign yourself
 * **Task list** for list of tasks that needs to be developed as part of the fix
    - unit tests
    - integration tests
    - sanity tests
    - documentation

2. Create <font color="red">one of</font> the following git branch from <font color="red">`main`</font> branch. Use `issue#<id>` from 1).
 * `feat/<module_name>_issue#<id>`
 * `imprv/issue#<id>`
 * `bug/issue#<id>`

3. Develop `sanity`, `unit` and `integrtaion` tests.

4. Create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)

5. Ensure <font color="royalblue">85% code coverage</font> on the pull request. Pull request with less than 85% coverage will be <font color="red">rejected</font>.

6. Link the pull request in `issue#<id>`

7. After the pull request is merged, close the `issue#<id>`

