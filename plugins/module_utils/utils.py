# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def remove_param_with_none_value(d):
    for k, v in d.copy().items():
        if v is None:
            d.pop(k)
        elif isinstance(v, dict):
            remove_param_with_none_value(v)
        elif isinstance(v, list):
            for e in v:
                if isinstance(e, dict):
                    remove_param_with_none_value(e)


def strip_extra_attrs(spec1, spec2, deep=True):
    """
    This routine strip extra attributes from spec1 as per spec2.
    If 'deep' is True then attributes are checked in all levels of
    dictionary, else only first level of dict is checked.
    """
    for k, v in spec1.copy().items():
        if k not in spec2:
            spec1.pop(k)
        elif isinstance(v, dict) and deep:
            strip_extra_attrs(spec1[k], spec2[k])
        elif isinstance(v, list) and v and isinstance(v[0], dict) and deep:
            for i in range(len(v)):
                try:
                    strip_extra_attrs(spec1[k][i], spec2[k][i])
                except IndexError:
                    spec1[k] = spec2[k]
                    break


def intersection(first_obj, second_obj):
    if isinstance(first_obj, dict):
        for key, value in first_obj.items():
            if key in second_obj and second_obj[key] == value:
                second_obj.pop(key)
            if isinstance(value, (dict, list)):
                intersection(value, second_obj)
        if not second_obj:
            return True
    elif isinstance(first_obj, list):
        for item in first_obj:
            intersection(item, second_obj)
    return False


def convert_to_secs(value, unit):
    """
    This routine converts given value to time interval into seconds as per unit
    """
    conversion_multiplier = {
        "MINUTE": 60,
        "HOUR": 3600,
        "DAY": 86400,
        "WEEK": 604800,
    }
    if unit not in conversion_multiplier:
        return None, "Invalid unit given for interval conversion to seconds"

    return value * conversion_multiplier[unit], None


def extract_uuids_from_references_list(reference_lists):
    """
    This routine extracts uuids from list of references to entities
    returns: set of uuids
    """
    uuids = set()
    for spec in reference_lists:
        uuids.add(spec["uuid"])
    return uuids


def list_to_string(lst):
    """
    This routine create comma seperated string from list of strings
    """
    return ",".join(lst)


def format_filters_map(filters, except_keys=None):
    if filters:
        mapped_filters = {}
        for key, value in filters.items():
            if value is not None:
                if except_keys is None or key not in except_keys:
                    key = key.replace("_", "-")
                mapped_filters.update({key: value})
        filters = mapped_filters
    return filters


def conv_mb_to_bytes(val):
    if not isinstance(val, int):
        return None, "Invalid value type passed for conv_mb_to_bytes"
    return val * 1024 * 1024, None


def create_filter_criteria_string(filters):
    """
    This method creates filter criteria string as per filters map for v3 apis
    example filter criteria format: "name==test_name;cluster_uuid=test_uuid"
    """
    filter_criteria = ""
    if not filters:
        return filter_criteria

    for key, val in filters.items():
        if val:
            filter_criteria = filter_criteria + "{0}=={1};".format(key, val)

    # remove ";" from ending
    filter_criteria = filter_criteria[:-1]

    return filter_criteria


def validate_required_params(module, required_params):
    """
    This routine checks if all required parameters are present in module.params
    and fails if any are missing.

    Args:
        module: AnsibleModule object
        required_params: List of required parameter names
                        Example: ['name', 'type', 'cluster_uuid']

    Returns:
        list: List of missing parameter names (empty if all present)
    """
    missing_params = []

    for param in required_params:
        if param not in module.params or module.params[param] is None:
            missing_params.append(param)

    if missing_params:
        module.fail_json(
            msg=f"Missing required parameter(s): {', '.join(missing_params)}"
        )

    return missing_params
