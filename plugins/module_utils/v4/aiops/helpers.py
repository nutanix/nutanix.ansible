# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_entity_types(module, api_instance, source_ext_id):
    """
    Fetch the list of entity types supported by a given AIOps stats source.

    Args:
        module (object): Ansible module object
        api_instance (object): StatsApi instance from ntnx_aiops_py_client sdk
        source_ext_id (str): The external ID (UUID) of the source

    Returns:
        response (object): EntityTypeListApiResponse from the SDK
    """
    try:
        return api_instance.get_entity_types_v4(sourceExtId=source_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching entity types for source "
                "ext_id: {0}".format(source_ext_id)
            ),
        )
