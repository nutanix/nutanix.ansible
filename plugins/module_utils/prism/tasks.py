# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import time

from .prism import Prism


class Task(Prism):
    def __init__(self, module):
        resource_type = "/tasks"
        super(Task, self).__init__(module, resource_type=resource_type)

    def create(self, data=None, endpoint=None, query=None, timeout=30):
        raise NotImplementedError("Create not permitted")

    def update(self, data=None, uuid=None, endpoint=None, query=None, timeout=30):
        raise NotImplementedError("Update not permitted")

    def delete(self, uuid=None, endpoint=None, query=None, timeout=30):
        raise NotImplementedError("Delete not permitted")

    def list(self, data=None, endpoint=None, use_base_url=False, timeout=30):
        raise NotImplementedError("List not permitted")

    def get_uuid(self, name):
        raise NotImplementedError("get_uuid not permitted")

    def wait_for_completion(self, uuid):
        state = ""
        while state != "SUCCEEDED":
            time.sleep(2)
            response = self.read(uuid)
            state = response.get("status")
            if state == "FAILED":
                self.module.fail_json(
                    msg=response["error_detail"],
                    status_code=response["error_code"],
                    error=response["error_detail"],
                    response=response,
                )

        return response
