# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception


def list_sources(module, api_instance):
    """
    Fetch the full list of available aiops sources.

    The aiops SDK exposes only a listing endpoint (no server-side pagination
    or filter parameters), so this helper wraps that call and surfaces any
    SDK exception through the standard `raise_api_exception` path.

    Args:
        module (AnsibleModule): Ansible module instance.
        api_instance: aiops StatsApi instance.

    Returns:
        aiops.v4.config.SourceListApiResponse: the raw SDK response object,
        `response.data` is the list of `Source` objects.
    """
    try:
        return api_instance.get_sources_v4()
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching sources v4 list",
        )


def get_source_by_ext_id(module, api_instance, ext_id):
    """
    Return a single aiops Source matching the given external ID.

    The aiops SDK does not expose a `GetSourceById` endpoint — the sources
    catalog is a singleton listing. To provide a `get_by_id`-style behaviour
    for the info module, list all sources and filter client-side. If no
    source matches the given `ext_id`, `module.fail_json` is called with a
    descriptive error including the ext_id that was not found.

    Args:
        module (AnsibleModule): Ansible module instance.
        api_instance: aiops StatsApi instance.
        ext_id (str): External ID of the source to fetch.

    Returns:
        aiops.v4.config.Source: the matching Source SDK object.
    """
    resp = list_sources(module, api_instance)
    sources = resp.data if resp is not None else None
    if not sources:
        module.fail_json(
            msg=(
                "Failed to find aiops source with ext_id '{0}': "
                "the sources listing returned no data.".format(ext_id)
            )
        )
    for source in sources:
        if getattr(source, "ext_id", None) == ext_id:
            return source
    module.fail_json(msg="No aiops source found with ext_id '{0}'.".format(ext_id))
