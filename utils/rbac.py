from common_models.models.permissions import Permission
from common_models.utils.rules import RuleValidator


def user_has_permission(user, perm_code):
    if getattr(user, 'is_superuser', False):
        return True
    return user.roles.filter(permissions__code=perm_code).exists()


def has_perm(user, perm_code: str, obj=None):
    """
    驗證使用者是否具備特定權限，並考量延伸規則
    """
    if user.is_superuser is True:
        return True

    # 透過角色取得所有權限
    permissions = Permission.objects.filter(roles__in=user.roles.all(), is_active=True).distinct()  # noqa

    # 確認是否有指定的 perm_code
    permission = permissions.filter(code=perm_code).first()
    if not permission:
        return False  # 沒有此權限

    # 檢查此權限是否有延伸規則
    rules = permission.rules.filter(is_active=True).order_by('-priority')

    # 沒有規則表示直接允許
    if not rules.exists():
        return True

    # 若有規則，逐一檢查（以優先順序排列）
    for rule in rules:
        validator = RuleValidator(rule.condition)

        # 若任一條規則不通過，則拒絕
        if not validator.evaluate(user):
            return False

    return True
