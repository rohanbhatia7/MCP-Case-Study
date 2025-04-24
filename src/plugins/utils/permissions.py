from enum import Enum, auto

class Permission(Enum):
    READ_DATA = auto()
    WRITE_DATA = auto()
    ADMIN_ACCESS = auto()
    QUERY_DB = auto()

# Role to permissions mapping
ROLE_PERMISSIONS = {
    "user": [Permission.READ_DATA],
    "editor": [Permission.READ_DATA, Permission.WRITE_DATA],
    "admin": [Permission.READ_DATA, Permission.WRITE_DATA, Permission.ADMIN_ACCESS, Permission.QUERY_DB],
}

def user_has_permission(user, permission):
    """Check if user has the required permission based on their role"""
    if not user or "role" not in user:
        return False
        
    user_role = user.get("role")
    return permission in ROLE_PERMISSIONS.get(user_role, [])
