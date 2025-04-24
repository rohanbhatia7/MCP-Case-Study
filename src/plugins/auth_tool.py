from typing import List
from plugins.utils.base_plugin import BasePlugin
from plugins.utils.permissions import Permission
from plugins.utils.decorators import require_permission
from plugins.utils.context import current_request
from plugins.utils.resource_access import Resource, can_access_resource

class AuthPlugin(BasePlugin):
    def __init__(self):
        self.tenant_resources = {
            "tenant_abc": [Resource("invoice_001", "tenant_abc"), Resource("invoice_002", "tenant_abc")],
            "tenant_xyz": [Resource("invoice_999", "tenant_xyz"), Resource("invoice_888", "tenant_xyz")],
        }
    
    @property
    def name(self) -> str:
        return "auth"
        
    @property
    def version(self) -> str:
        return "1.0.0"
        
    @property
    def description(self) -> str:
        return "Authentication and authorization tools for MCP server"
    
    @property
    def required_env_vars(self) -> List[str]:
        return ["SECRET_KEY"]  # Make sure the JWT secret is set
    
    def register_tools(self, mcp):
        """Register authentication tools with the MCP server"""
        
        @mcp.tool()
        @require_permission(Permission.ADMIN_ACCESS)
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
            tenant_resources = self.tenant_resources.get(tenant_id, [])
            
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

plugin = AuthPlugin()
