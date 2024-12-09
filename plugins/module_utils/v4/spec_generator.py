# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy


class SpecGenerator(object):
    module = None

    def __init__(self, module):
        self.module = module

    def generate_spec(self, obj, attr=None, **kwargs):
        """
        This method will populate spec obj as per input attrs
        Args:
            obj (object): spec object
            attr (dict): Optional params for generating spec. By default module.params will be used
            kwargs (dict): Keyword arguments
        Returns:
            spec (object): spec object
            error (str): error string if any
        """

        if not isinstance(obj, object):
            return None, "Spec object is of invalid type"

        module_args = kwargs.get(
            "module_args", self.module.argument_spec_with_extra_keys
        )

        if not attr:
            attr = copy.deepcopy(self.module.params)

        # Resolve each input param w.r.t its module argument spec
        for key, schema in module_args.items():

            if key in attr and hasattr(obj, key):

                attr_type = schema.get("type")
                if not attr_type:
                    return (
                        None,
                        "Invalid module argument: 'type' is required parameter for attribute {0}".format(
                            key
                        ),
                    )

                options = schema.get("options")
                kwargs["module_args"] = options

                _obj = schema.get("obj")

                # for attributes with dynamic obj
                if type(_obj) is dict:

                    for dynamic_obj_key, dynamic_obj_value in attr[key].items():

                        _obj = _obj.get(dynamic_obj_key)
                        attr[key] = dynamic_obj_value
                        kwargs["module_args"] = options.get(dynamic_obj_key).get(
                            "options"
                        )
                        break

                elements = schema.get("elements")

                # for dict type attribute, recursively create spec objects
                if attr_type == "dict" and options is not None and _obj is not None:

                    # check if spec obj exist else create a new obj to populate spec
                    o = getattr(obj, key)
                    if not o:
                        o = _obj()

                    s, err = self.generate_spec(obj=o, attr=attr[key], **kwargs)
                    if err:
                        return None, err
                    setattr(obj, key, s)

                # for list type attribute, create list of spec objects recursively
                elif (
                    attr_type == "list"
                    and elements == "dict"
                    and options is not None
                    and _obj is not None
                ):
                    lst = []
                    for item in attr[key]:
                        s, err = self.generate_spec(obj=_obj(), attr=item, **kwargs)
                        if err:
                            return None, err
                        lst.append(s)
                    setattr(obj, key, lst)

                # for other types directly assign
                else:
                    setattr(obj, key, attr[key])

        return obj, None

    def get_info_spec(self, attr=None, extra_params=None):

        if not attr:
            attr = copy.deepcopy(self.module.params)
        spec = {}
        all_params = ["page", "limit", "filter", "orderby", "select"]
        if extra_params is None:
            extra_params = []
        all_params.extend(extra_params)
        if attr.get("name"):
            _filter = attr.get("filter")
            if _filter:
                _filter += f"""and name eq '{attr["name"]}'"""
            else:
                _filter = f"""name eq '{attr["name"]}'"""
            attr["filter"] = _filter
        for key, val in attr.items():
            if key in all_params:
                spec[f"_{key}"] = val
        return spec, None

    def get_stats_spec(self, attr=None):
        attribute_map = {
            "start_time": "_startTime",
            "end_time": "_endTime",
            "sampling_interval": "_samplingInterval",
            "stat_type": "_statType",
        }
        if not attr:
            attr = copy.deepcopy(self.module.params)
        spec = {}
        for key, val in attr.items():
            if key in attribute_map:
                spec[attribute_map[key]] = val
        return spec, None

    def map_bytes_to_mb(self, mb, byte):
        if self.module.params.get(mb):
            self.module.params[byte] = self.module.params[mb] * 1024 * 1024
