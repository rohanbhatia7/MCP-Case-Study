from functools import wraps
from plugins.utils.permissions import Permission, user_has_permission
from plugins.utils.context import current_request

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