class DatabaseEngine:
    _type = ""

    def __init__(self, module):
        self.module = module

    def build_spec_db_instance_provision_action_arguments(self, payload, config):
        return (
            None,
            "Build spec method for Database instance provision action arguments is not implemented",
        )

    def build_spec_db_params_profile_properties(self, params, curr_properties=None):
        return (
            None,
            "Build spec method for Database Parameter profile's properties is not implemented",
        )

    def get_type(self):
        return self._type
