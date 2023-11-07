## Design Goals - Simplicity

- Easy to use
- Easy to develop

**Easy to use**

- Don't mimick API spec. Ansible spec should be a simplified version of API spec.
- Goal is to expose *minimum attributes* to create, update or delete the entity
- Keep backward & forward compatibility in mind when creating ansible spec
- Look at the example of ansible spec for VM. Only 13 attributes are exposed from API to cater to 80-90% of use cases.


**Easy to develop**

- Use `scripts/codegen`to automatically generate code for the module development

    ` $python scripts/codegen subnets`

- `scripts/codegen` provides 3 things out of the box

    a. [Client SDK](https://github.com/nutanix/nutanix.ansible/blob/main/plugins/module_utils/prism/subnets.py).

    b. [Ansible module](https://github.com/nutanix/nutanix.ansible/blob/main/plugins/modules/ntnx_subnets.py) plugin with [`run_module()`](https://github.com/nutanix/nutanix.ansible/blob/f5e9c0d1432014ea175b888f81efdfa6be81fb8f/plugins/modules/ntnx_subnets.py#L657) implementation.

    c. [Bootstrap code](https://github.com/nutanix/nutanix.ansible/blob/f5e9c0d1432014ea175b888f81efdfa6be81fb8f/plugins/modules/ntnx_subnets.py#L595) for creating and deleting entity.

- Takes 3 steps to develop the module
    1. Define [Ansible spec & type validator](https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec)

    Example:
    ```python
        def get_module_spec():
            mutually_exclusive = [("name", "uuid")]
            overlay_ipam_spec = dict(...)
            external_subnet_spec = dict(...)
            overlay_subnet_spec = dict(...)

            module_args = dict(
                name=dict(type="str", required=False),
                subnet_uuid=dict(type="str", required=False),
                vlan_subnet=dict(type="dict", options=vlan_subnet_spec),
                external_subnet=dict(type="dict", options=external_subnet_spec),
                overlay_subnet=dict(type="dict", options=overlay_subnet_spec),
            )

            return module_args
    ```

    2. Define <font color="red">`ansible_param`</font> as **key** and <font color="red">`_build_spec_*`</font> method as **value** in <font color="red">`self.build_spec_methods`</font> map.

    Example:
    ```python
    self.build_spec_methods = {
            "name": self._build_spec_name,
            "vlan_subnet": self._build_spec_vlan_subnet,
            "external_subnet": self._build_spec_external_subnet,
            "overlay_subnet": self._build_spec_overlay_subnet,
        }
    ```
    3. Implement <font color=red>`_get_default_spec(self)`</font> and <font color="red">`_build_spec_*(self, payload, config)`</font> methods

    Example:
    ```python
        def _get_default_spec(self):
            return deepcopy(
                {
                    "api_version": "3.1.0",
                    "metadata": {"kind": "subnet"},
                    "spec": {
                        "name": "",
                        "resources": {"ip_config": {}, "subnet_type": None},
                    },
                }
            )

        def _build_spec_name(self, payload, value):
            payload["spec"]["name"] = value
            return payload, None

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
