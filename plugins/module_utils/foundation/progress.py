# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

import time

from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.foundation import (
    Foundation,
)

__metaclass__ = type


class Progress(Foundation):
    def __init__(self, module):
        resource_type = "/progress"
        super(Progress, self).__init__(module, resource_type=resource_type)

    def get(self, uuid):
        query = {"session_id": uuid}
        resp = self.read(query=query)
        return resp

    def wait_for_completion(self, uuid):
        state = ""
        delay = 30
        timeout = time.time() + (max(3600, self.module.params["timeout"]))
        while state != "COMPLETED":
            response = self.get(uuid)
            stopped = response.get("imaging_stopped", False)
            aggregate_percent_complete = response.get("aggregate_percent_complete", -1)
            if stopped:
                if aggregate_percent_complete < 100:
                    status = self._get_progress_error_status(response)
                    return response, status
                state = "COMPLETED"
            else:
                state = "PENDING"
                if time.time() > timeout:
                    return (
                        None,
                        "Failed to poll on image node progress. Reason: Timeout",
                    )
                time.sleep(delay)
        return response, None

    def _get_progress_error_status(self, progress):
        return "Imaging stopped before completion.\nClusters: {}\nNodes: {}".format(
            self._get_progress_messages(progress, "clusters", "cluster_name"),
            self._get_progress_messages(progress, "nodes", "cvm_ip"),
        )

    def _get_progress_messages(self, progress, entity_type, entity_name):
        res = ""
        clusters = progress.get(entity_type)
        if clusters:
            for c in clusters:
                res += "cluster: {}\n".format(c.get(entity_name))
                res += "messages:\n{}\n".join(c.get("messages", []))
        return res
