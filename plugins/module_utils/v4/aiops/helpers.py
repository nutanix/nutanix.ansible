# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_scenario(module, api_instance, ext_id):
    """
    Fetch a single capacity planning scenario by external ID.

    Args:
        module: Ansible module
        api_instance: ``ScenariosApi`` instance from ``ntnx_aiops_py_client``
        ext_id (str): scenario external ID
    return:
        info (object): scenario info object (``.data`` from the API response)
    """
    try:
        return api_instance.get_scenario_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching scenario info using ext_id",
        )


def get_simulation(module, api_instance, ext_id):
    """
    Fetch a single simulation by external ID.

    Args:
        module: Ansible module
        api_instance: ``ScenariosApi`` instance from ``ntnx_aiops_py_client``
        ext_id (str): simulation external ID
    return:
        info (object): simulation info object (``.data`` from the API response)
    """
    try:
        return api_instance.get_simulation_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching simulation info using ext_id",
        )


def get_scenario_by_name(module, api_instance, name):
    """
    Best-effort lookup of a scenario by its ``name``.

    The aiops list endpoint does not currently support OData filtering on the
    ``name`` property, so we page through the response server-side and match
    client-side. Used by the CRUD module for idempotency: if the caller
    passes a ``name`` only (no ``ext_id``) and a scenario with that name
    already exists, the module skips the create.

    Args:
        module: Ansible module
        api_instance: ``ScenariosApi`` instance from ``ntnx_aiops_py_client``
        name (str): scenario name
    return:
        scenario (object|None): the first scenario matching the name or
        ``None`` if none was found.
    """
    page = 0
    page_size = 100
    while True:
        try:
            resp = api_instance.list_scenarios(_page=page, _limit=page_size)
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while listing scenarios by name",
            )
        data = getattr(resp, "data", None) or []
        for scenario in data:
            if getattr(scenario, "name", None) == name:
                return scenario
        if len(data) < page_size:
            return None
        page += 1
