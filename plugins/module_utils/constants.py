class ACP:
    class EntityFilterExpressionList:
        PROJECT_ADMIN = [
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "image"},
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "marketplace_item"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "directory_service"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "role"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "user"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "user_group"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "environment"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
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
                "left_hand_side": {"entity_type": "app_task"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "app_variable"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "identity_provider"},
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
            }
        ]

        DEVELOPER = [
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "image"},
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "marketplace_item"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
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
                "left_hand_side": {"entity_type": "app_task"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "app_variable"},
                "right_hand_side": {"collection": "SELF_OWNED"},
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
            }
        ]

        CONSUMER = [
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "image"},
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "marketplace_item"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
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
                "left_hand_side": {"entity_type": "app_task"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "app_variable"},
                "right_hand_side": {"collection": "SELF_OWNED"},
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
            }
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

        PERMISSION_TO_EXPRESSION_MAP = {
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
