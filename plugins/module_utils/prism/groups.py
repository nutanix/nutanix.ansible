# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from .prism import Prism


class Groups(Prism):
    def __init__(self, module):
        resource_type = "/groups"
        super().__init__(module, resource_type=resource_type)

    def get_uuid(self, entity_type, filter):
        data = {"entity_type": entity_type, "filter_criteria": filter}
        resp, _ = self.list(data, use_base_url=True)
        if resp.get("group_results"):
            return resp["group_results"][0]["entity_results"][0]["entity_id"]
        return None
