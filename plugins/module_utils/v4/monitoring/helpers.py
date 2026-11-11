# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_alert(module, api_instance, ext_id, expand=None):
    """
    Fetch an alert by external ID.
    """
    try:
        kwargs = {}
        if expand is not None:
            kwargs["_expand"] = expand
        return api_instance.get_alert_by_id(extId=ext_id, **kwargs).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching alert info",
        )


def get_alert_email_configuration(module, api_instance):
    """
    Fetch alert email configuration.
    """
    try:
        return api_instance.get_alert_email_configuration().data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching alert email configuration",
        )


def get_audit(module, api_instance, ext_id):
    """
    Fetch an audit by external ID.
    """
    try:
        return api_instance.get_audit_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching audit info",
        )


def get_event(module, api_instance, ext_id):
    """
    Fetch an event by external ID.
    """
    try:
        return api_instance.get_event_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching event info",
        )


def get_sda_policy(module, api_instance, ext_id):
    """
    Fetch a System-Defined Alert policy by external ID.
    """
    try:
        return api_instance.get_sda_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching system-defined policy info",
        )


def get_cluster_config(module, api_instance, system_defined_policy_ext_id, ext_id):
    """
    Fetch cluster-specific configuration for a System-Defined Alert policy.
    """
    try:
        return api_instance.get_cluster_config_by_id(
            systemDefinedPolicyExtId=system_defined_policy_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching system-defined policy cluster config",
        )


def get_uda_policy(module, api_instance, ext_id):
    """
    Fetch a User-Defined Alert policy by external ID.
    """
    try:
        return api_instance.get_uda_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching user-defined policy info",
        )
