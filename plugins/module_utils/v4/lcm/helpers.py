# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_lcm_status(module, api_instance, cluster_ext_id=None):
    """
    This method will return LCM status info.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM status api instance
        cluster_ext_id (str): External id of cluster
    Returns:
        lcm_status_info (dict): LCM status info
    """
    try:
        return api_instance.get_status(X_Cluster_Id=cluster_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM status info",
        )


def get_lcm_config(module, api_instance, cluster_ext_id=None):
    """
    This method will return LCM config info.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM config api instance
        cluster_ext_id (str): External id of cluster
    Returns:
        lcm_config_info (dict): LCM config info
    """
    try:
        return api_instance.get_config(X_Cluster_Id=cluster_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM config info",
        )


def get_lcm_entity(module, api_instance, ext_id):
    """
    This method will return entity info using external identifier of the entity.
    Args:
        module (object): Ansible module object
        api_instance (object): Entity api instance
        ext_id (str): External id of entity
    Returns:
        entity_info (dict): Entity info
    """
    try:
        return api_instance.get_entity_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching entity info using external identifier of the entity",
        )


def get_lcm_recommendation(module, api_instance, ext_id):
    """
    This method will return an LCM recommendation using its external identifier.
    Args:
        module (object): Ansible module object
        api_instance (object): LCM recommendations api instance
        ext_id (str): External id of the LCM recommendation resource
    Returns:
        recommendation (object): LCM recommendation info object
    """
    try:
        return api_instance.get_recommendation_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM recommendation info "
            "using external identifier '{0}'".format(ext_id),
        )


def build_recommendation_spec(module, sdk_module):
    """
    Build the RecommendationSpec body from module parameters.

    RecommendationSpec has a single OneOf field ``recommendation_spec`` whose
    value must be a list of one of:
        * lifecycle.v4.common.EntityType  (enum string, e.g. SOFTWARE / FIRMWARE)
        * lifecycle.v4.resources.TargetEntity
        * lifecycle.v4.common.EntityUpdateSpec
        * lifecycle.v4.common.EntityDeploySpec

    The module exposes the four flavours as mutually exclusive top-level
    parameters. Exactly one must be provided by the user; this helper picks
    the one that was supplied, builds the SDK objects, and populates
    ``RecommendationSpec.recommendation_spec`` with the resulting list.

    Args:
        module (object): Ansible module object.
        sdk_module (module): The ``ntnx_lifecycle_py_client`` SDK (or its mock)
            imported by the calling module — used so the caller keeps
            SDK-import handling in one place.

    Returns:
        Tuple[object, str | None]: The ``RecommendationSpec`` object and an
        optional error message. On error, the spec object is ``None``.
    """
    entity_types = module.params.get("entity_types")
    target_entities = module.params.get("target_entities")
    entity_update_specs = module.params.get("entity_update_specs")
    entity_deploy_specs = module.params.get("entity_deploy_specs")

    provided = [
        p
        for p in (
            entity_types,
            target_entities,
            entity_update_specs,
            entity_deploy_specs,
        )
        if p
    ]
    if not provided:
        return (
            None,
            "One of 'entity_types', 'target_entities', 'entity_update_specs' or "
            "'entity_deploy_specs' must be provided for computing LCM recommendations.",
        )

    spec = sdk_module.RecommendationSpec()

    if entity_types:
        spec.recommendation_spec = list(entity_types)
    elif target_entities:
        spec.recommendation_spec = [
            _build_target_entity(sdk_module, item) for item in target_entities
        ]
    elif entity_update_specs:
        spec.recommendation_spec = [
            _build_entity_update_spec(sdk_module, item) for item in entity_update_specs
        ]
    else:
        spec.recommendation_spec = [
            _build_entity_deploy_spec(sdk_module, item) for item in entity_deploy_specs
        ]

    return spec, None


def _build_location_info(sdk_module, item):
    if not item:
        return None
    kwargs = {k: v for k, v in item.items() if v is not None}
    return sdk_module.LocationInfo(**kwargs)


def _build_target_entity(sdk_module, item):
    location_info = _build_location_info(sdk_module, item.get("location_info"))
    kwargs = {
        k: v for k, v in item.items() if k not in ("location_info",) and v is not None
    }
    if location_info is not None:
        kwargs["location_info"] = location_info
    return sdk_module.TargetEntity(**kwargs)


def _build_entity_update_spec(sdk_module, item):
    kwargs = {k: v for k, v in item.items() if v is not None}
    return sdk_module.EntityUpdateSpec(**kwargs)


def _build_entity_deploy_spec(sdk_module, item):
    ident = item.get("entity_identifier") or {}
    ident_kwargs = {k: v for k, v in ident.items() if v is not None}
    entity_identifier = sdk_module.EntityBaseModel(**ident_kwargs)
    return sdk_module.EntityDeploySpec(entity_identifier=entity_identifier)
