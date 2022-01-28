# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from .prism import Prism


class Project(Prism):
    def __init__(self, module):
        resource_type = "/projects"
        super().__init__(module, resource_type=resource_type)
