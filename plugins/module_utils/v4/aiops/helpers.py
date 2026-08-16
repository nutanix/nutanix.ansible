# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_entity_descriptors(module, api_instance, source_ext_id, **kwargs):
    """
    Return the list of entity descriptors for a source.

    Wraps `StatsApi.get_entity_descriptors_v4` and translates SDK exceptions
    into an Ansible-friendly failure.

    Args:
        module (AnsibleModule): the invoking Ansible module.
        api_instance (StatsApi): aiops Stats API instance.
        source_ext_id (str): UUID (or well-known name like ``"nutanix"``)
            identifying the source to fetch descriptors for.
        **kwargs: additional query parameters (``_page``, ``_limit``,
            ``_filter``) forwarded to the SDK method.

    Returns:
        EntityDescriptorListApiResponse: the raw SDK response.
    """
    try:
        return api_instance.get_entity_descriptors_v4(
            sourceExtId=source_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching entity descriptors for source "
                "'{0}'".format(source_ext_id)
            ),
        )
