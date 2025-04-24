from plugins.utils.utils import current_request, require_permission, Permission, Resource, can_access_resource

# Simulate tenant resources
TENANT_RESOURCES = {
    "tenant_abc": [Resource("invoice_001", "tenant_abc"), Resource("invoice_002", "tenant_abc")],
    "tenant_xyz": [Resource("invoice_999", "tenant_xyz"), Resource("invoice_888", "tenant_xyz")],
}

def register_tool(mcp):
    """Register authentication tools with the MCP server"""
    
    @mcp.tool()
    @require_permission(Permission.QUERY_DB)
    async def get_protected_tenant_data(resource_id: str = None) -> str:
        """
        Access tenant-specific protected data for the authenticated user.
        
        Args:
            resource_id: Optional specific resource to access
        """
        request = current_request.get()
        user = getattr(request.state, "user", {})            
        tenant_id = user.get("tenant_id")
        
        # Get all resources for tenant
        tenant_resources = TENANT_RESOURCES.get(tenant_id, [])
        
        if resource_id:
            # Filter for specific resource
            for resource in tenant_resources:
                if resource.id == resource_id:
                    if can_access_resource(user, resource):
                        return f"Resource {resource_id} data: [Details...]"
                    else:
                        return "Access denied to this resource"
            return f"Resource {resource_id} not found"
        
        # Return all accessible resources
        accessible_resources = [
            res.id for res in tenant_resources 
            if can_access_resource(user, res)
        ]
        
        if not accessible_resources:
            return "No accessible resources found"
            
        return f"Accessible resources for tenant {tenant_id}:\n" + "\n".join(accessible_resources)
