class PermissionError(Exception):
    pass

def require_role(user: dict, role: str):
    if user.get("role") != role:
        raise PermissionError(f"Access denied for role: {user.get('role')}")

def require_tenant(user: dict, tenant: str):
    if user.get("tenant_id") != tenant:
        raise PermissionError(f"Access denied: tenant mismatch")
