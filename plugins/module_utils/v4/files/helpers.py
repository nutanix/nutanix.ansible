# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_tiering_configuration(module, api_instance, file_server_ext_id, ext_id):
    """
    This method will return tiering configuration info using its file server ext_id and tiering configuration ext_id.
    Args:
        module: Ansible module
        api_instance: TierApi instance from ntnx_files_py_client sdk
        file_server_ext_id (str): file server external ID
        ext_id (str): tiering configuration external ID
    return:
        info (object): tiering configuration info
    """
    try:
        return api_instance.get_tiering_configuration_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching tiering configuration info using ext_id",
        )


def list_tiering_configurations(module, api_instance, file_server_ext_id, **kwargs):
    """
    This method will list tiering configurations for a file server.
    Args:
        module: Ansible module
        api_instance: TierApi instance from ntnx_files_py_client sdk
        file_server_ext_id (str): file server external ID
        kwargs: Additional query params (e.g. _page, _limit, _filter, _orderby)
    return:
        info (object): list tiering configurations api response
    """
    try:
        return api_instance.list_tiering_configurations(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching tiering configurations info",
        )
