class RuleValidator:
    def __init__(self, condition: dict):
        self.condition = condition

    def evaluate(self, user, obj=None):
        """
        驗證使用者與物件是否符合此規則
        目前先實作一個簡單的region規則作為範例
        """
        # 範例：驗證使用者是否在允許的region
        allowed_regions = self.condition.get("region")
        if allowed_regions:
            user_region = getattr(user, "region", None)
            if user_region not in allowed_regions:
                return False

        # 你可以在這裡繼續擴充其他條件的檢查
        return True


def validate_new_user_roles(creator, new_user_roles):
    """
    驗證建立者可否授予這些角色給新使用者
    """
    if creator.is_superuser is True:
        return True

    for role in new_user_roles:
        if role.level <= creator.get_highest_role_level():
            raise ValueError(f"無法授予等級高於或相同的角色: {role.name}")

    return True
