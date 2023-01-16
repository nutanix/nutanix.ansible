# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


class DatabaseEngine:
    """
    Implement DatabaseEngine for all database engine types
    """

    _type = ""

    def __init__(self, module):
        self.module = module

    def build_spec_db_instance_provision_action_arguments(self, payload, config):
        """
        Implement this method to add db engine specific action arguments for database instance provision
        """
        return payload, None

    def build_spec_db_instance_register_action_arguments(self, payload, config):
        """
        Implement this method to add db engine specific action arguments for database instance registration
        """
        return payload, None

    def build_spec_db_params_profile_properties(self, payload, config):
        """
        Implement this method to add database engine specific properties for creating Database Parameter profiles
        """
        return payload, None

    def build_spec_db_server_vm_register_action_arguments(self, payload, config):
        """
        Implement this method to add database engine specific properties for registeration database server vm
        """
        return payload, None

    def build_spec_db_clone_action_arguments(self, payload, config):
        """
        Implement this method to add database engine specific properties for database clone provisioning
        """
        return payload, None

    def get_type(self):
        return self._type
