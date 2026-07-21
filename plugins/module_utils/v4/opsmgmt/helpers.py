# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_report_artifact_by_ext_id(module, api_instance, ext_id):
    """
    Fetch a single :class:`ReportArtifact` by its external ID.

    The opsmgmt v4 ``ReportArtifactsApi`` does not expose a dedicated
    "get-by-id" endpoint. Instead we use the list API with an OData
    ``$filter=extId eq '<uuid>'`` (which is what the Prism UI also does)
    and return the first match.

    Args:
        module (AnsibleModule): the calling Ansible module — used only
            to route SDK errors through :func:`raise_api_exception`.
        api_instance (ntnx_opsmgmt_py_client.ReportArtifactsApi): SDK
            client built by :func:`get_report_artifacts_api_instance`.
        ext_id (str): the ``extId`` (UUID) of the report artifact to
            retrieve. Must not be ``None`` — the caller is expected to
            validate presence before invoking this helper.

    Returns:
        ntnx_opsmgmt_py_client.models.opsmgmt.v4.content.ReportArtifact | None:
        the matching artifact object, or ``None`` if the list call
        succeeded but no artifact has the requested ``ext_id``.
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
        return None

    data = getattr(resp, "data", None) or []
    for item in data:
        if getattr(item, "ext_id", None) == ext_id:
            return item
    return None
