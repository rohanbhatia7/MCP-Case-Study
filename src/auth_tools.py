from auth_utils import require_role, require_tenant
from context import current_request
from test_data import TENANT_RESOURCES

def get_protected_tenant_data_factory(mcp):
    @mcp.tool()
    async def get_protected_tenant_data() -> str:
        """
        Access tenant-specific protected data for the authenticated user.

        This tool checks the user's role and tenant_id using the request context.
        Only users with the 'admin' role can access it. No arguments are required.
        """
        request = current_request.get()
        user = getattr(request.state, "user", {})
        
        try:
            require_role(user, "admin") # only admins can access this
            require_tenant(user, user.get("tenant_id")) # must match own tenant

            tenant_id = user.get("tenant_id")
            data = TENANT_RESOURCES.get(tenant_id, [])
            return f"Tenant {tenant_id} data:\n" + "\n".join(data or ["No data"])
        
        except Exception as e:
            return f"Access denied: {str(e)}"
