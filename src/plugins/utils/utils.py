from contextvars import ContextVar
from enum import Enum, auto
from functools import wraps
from starlette.requests import Request

# Holds the request per async context
current_request: ContextVar[Request] = ContextVar("current_request")

# Permission definitions
class Permission(Enum):
    READ_DATA = auto()
    WRITE_DATA = auto()
    ADMIN_ACCESS = auto()
    QUERY_DB = auto()

# Resource class
class Resource:
    def __init__(self, id, tenant_id):
        self.id = id
        self.tenant_id = tenant_id

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

def require_permission(permission):
    """Decorator to check if user has required permission for tool access"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = current_request.get()
            user = getattr(request.state, "user", {})
            
            if not user_has_permission(user, permission):
                return f"Access denied: Required permission '{permission.name}' not found"
                
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def can_access_resource(user, resource):
    """Check if user can access specific resource"""
    # Always deny if no user info
    if not user:
        return False
        
    # Super admins can access all resources
    if user.get("role") == "super_admin":
        return True
        
    # Users can only access resources in their tenant
    return user.get("tenant_id") == resource.tenant_id