# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

import time

__metaclass__ = type


from ..constants import NDB
from .nutanix_database import NutanixDatabase


class Operation(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/operations"
        super(Operation, self).__init__(module, resource_type=resource_type)

    def wait_for_completion(
        self, uuid, raise_error=True, delay=NDB.OPERATIONS_POLLING_DELAY
    ):
        timeout = time.time() + self.module.params["timeout"]
        resp = None
        while True:
            resp = self.read(uuid)
            status = resp.get("status")
            if status == NDB.StatusCodes.SUCCESS:
                return resp
            elif status == NDB.StatusCodes.FAILURE:
                if not raise_error:
                    break
                self.module.fail_json(
                    msg=resp["message"],
                    response=resp,
                )
            else:
                if time.time() > timeout:
                    self.module.fail_json(
                        msg="Failed to poll on provision database instance operations. Reason: Timeout",
                        response=resp,
                    )
            time.sleep(delay)
        return resp
