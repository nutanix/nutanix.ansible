# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_report_artifact(module, api_instance, ext_id):
    """
    Fetch a single report artifact by external ID.

    The opsmgmt v4 API does not expose a dedicated ``get_report_artifact_by_id``
    endpoint. This helper emulates the get-by-ID semantics by listing report
    artifacts with an OData ``$filter`` on ``extId`` and returning the first
    match. Returns ``None`` when the artifact is not present.

    Args:
        module (AnsibleModule): The invoking Ansible module object.
        api_instance: A ``ReportArtifactsApi`` SDK client instance.
        ext_id (str): The external ID of the report artifact to fetch.

    Returns:
        The matching ``ReportArtifact`` SDK object or ``None``.
    """
    try:
        resp = api_instance.list_report_artifacts(
            _filter="extId eq '{0}'".format(ext_id)
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching report artifact info using ext_id",
        )

    data = getattr(resp, "data", None)
    if not data:
        return None
    for item in data:
        if getattr(item, "ext_id", None) == ext_id:
            return item
    return data[0] if data else None
