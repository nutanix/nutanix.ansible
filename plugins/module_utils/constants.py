# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ACP:
    class EntityFilterExpressionList:
        PROJECT_ADMIN = [
            {
                "left_hand_side": {"entity_type": "image"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "app_icon"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "category"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "environment"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "marketplace_item"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "user"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "user_group"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "role"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "directory_service"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "identity_provider"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "app_task"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "app_variable"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "vm_recovery_point"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "virtual_network"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
        ]
        DEVELOPER = [
            {
                "left_hand_side": {"entity_type": "image"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "app_icon"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "category"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "environment"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "marketplace_item"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "app_task"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "app_variable"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
        ]
        CONSUMER = [
            {
                "left_hand_side": {"entity_type": "image"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "app_icon"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "category"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "environment"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "marketplace_item"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "app_task"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "app_variable"},
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "left_hand_side": {"entity_type": "vm_recovery_point"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "left_hand_side": {"entity_type": "virtual_network"},
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
            },
        ]
        OPERATOR = [
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "app_icon"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "category"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "vm_recovery_point"},
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "virtual_network"},
                "right_hand_side": {"collection": "ALL"},
            },
        ]

        DEFAULT = [
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "blueprint"},
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "environment"},
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "marketplace_item"},
                "right_hand_side": {"collection": "ALL"},
            },
        ]

        PERMISSION_TO_ACCESS_MAP = {
            "View_Image": {
                "operator": "IN",
                "left_hand_side": {"entity_type": "image"},
                "right_hand_side": {"collection": "ALL"},
            },
            "View_App_Icon": {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "app_icon"},
            },
            "View_Name_Category": {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "category"},
            },
            "Create_Or_Update_Name_Category": {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "category"},
            },
            "View_Environment": {
                "operator": "IN",
                "left_hand_side": {"entity_type": "environment"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            "View_Marketplace_Item": {
                "operator": "IN",
                "left_hand_side": {"entity_type": "marketplace_item"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            "View_User": {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "user"},
            },
            "View_User_Group": {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "user_group"},
            },
            "View_Role": {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "role"},
            },
            "View_Directory_Service": {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "directory_service"},
            },
            "Search_Sirectory_Service": {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "directory_service"},
            },
            "View_Identity_Provider": {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "identity_provider"},
            },
            "View_App_Task": {
                "operator": "IN",
                "left_hand_side": {"entity_type": "app_task"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            "View_App_Variable": {
                "operator": "IN",
                "left_hand_side": {"entity_type": "app_variable"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
        }


class NDB:

    OPERATIONS_POLLING_DELAY = 30

    class DatabaseTypes:
        POSTGRES = "postgres_database"

    class ProfileTypes:
        COMPUTE = "Compute"
        NETWORK = "Network"

    class StatusCodes:
        SUCCESS = "5"
        FAILURE = "4"
