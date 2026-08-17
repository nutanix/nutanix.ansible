# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def get_volume_group(module, api_instance, ext_id):
    """
    Fetch a Volume Group by ext_id using the storage SDK.

    Args:
        module: Ansible module
        api_instance: VolumeGroupApi instance from ntnx_storage_py_client
        ext_id: ext_id of the Volume Group
    Returns:
        The Volume Group model object.
    """
    try:
        return api_instance.get_volume_group_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume group info using ext_id",
        )


def get_category_associations(module, api_instance, ext_id, **kwargs):
    """
    Fetch the list of categories associated with a Volume Group.

    Args:
        module: Ansible module
        api_instance: VolumeGroupApi instance from ntnx_storage_py_client
        ext_id: ext_id of the Volume Group
        kwargs: optional page/limit query parameters (as ``_page`` / ``_limit``)

    Returns:
        The full GetCategoryAssociationsApiResponse object.
    """
    try:
        return api_instance.get_category_associations(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching category associations for Volume group",
        )


def get_associated_category_ext_ids(module, api_instance, ext_id):
    """
    Return the set of category ext_ids currently associated with a VG.

    Pages through the GetCategoryAssociations endpoint so idempotency checks
    do not silently miss categories past the default page size.
    """
    associated = set()
    page = 0
    limit = 100
    while True:
        resp = get_category_associations(
            module, api_instance, ext_id, _page=page, _limit=limit
        )
        data = getattr(resp, "data", None) or []
        for item in data:
            item_ext_id = getattr(item, "ext_id", None)
            if item_ext_id:
                associated.add(item_ext_id)
        if not data or len(data) < limit:
            break
        page += 1
    return associated
