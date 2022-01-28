from plugins.module_utils.prism.vms import VM
from plugins.module_utils.prism.images import Image

import json
from ansible.module_utils.basic import AnsibleModule


class Module:
    def __init__(self):
        self.params = {
            "nutanix_host": "10.46.34.230",
            "nutanix_port": 9440,
            "nutanix_username": "admin",
            "nutanix_password": "Nutanix.123",
        }
        self.tmpdir = "/tmp"

    def jsonify(self, data):
        return json.dumps(data)


def main():
    module = Module()
    vm = VM(module)
    data = {"kind": "vm", "offset": 0, "length": 500}
    print(vm.list(data))


if __name__ == "__main__":
    main()
