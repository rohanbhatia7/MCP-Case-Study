class Resource:
    def __init__(self, id, tenant_id):
        self.id = id
        self.tenant_id = tenant_id

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