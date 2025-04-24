from plugins.utils.utils import current_request, require_permission, Permission, Resource, can_access_resource

# Simulate tenant resources
TENANT_RESOURCES = {
    "tenant_abc": [
        Resource("invoice_001", "tenant_abc"),
        Resource("invoice_002", "tenant_abc"),
        Resource("invoice_003", "tenant_abc"),
        Resource("report_q1_2024", "tenant_abc"),
        Resource("report_q2_2024", "tenant_abc"),
        Resource("customer_list_2024", "tenant_abc"),
        Resource("contract_renewal_2024", "tenant_abc"),
        Resource("budget_forecast_2025", "tenant_abc"),
    ],
    "tenant_xyz": [
        Resource("invoice_999", "tenant_xyz"),
        Resource("invoice_888", "tenant_xyz"),
        Resource("invoice_777", "tenant_xyz"),
        Resource("report_q1_2024", "tenant_xyz"),
        Resource("report_q2_2024", "tenant_xyz"),
        Resource("vendor_list_2024", "tenant_xyz"),
        Resource("market_analysis_2024", "tenant_xyz"),
        Resource("strategic_plan_2025", "tenant_xyz"),
    ],
    "tenant_acme": [
        Resource("invoice_501", "tenant_acme"),
        Resource("invoice_502", "tenant_acme"),
        Resource("report_annual_2023", "tenant_acme"),
        Resource("employee_handbook", "tenant_acme"),
        Resource("product_roadmap", "tenant_acme"),
        Resource("investor_presentation", "tenant_acme"),
    ]
}

def register_tool(mcp):
    """Register authentication tools with the MCP server"""
    
    @mcp.tool()
    @require_permission(Permission.QUERY_DB)
    async def get_protected_tenant_data(resource_id: str = "") -> str:
        """
        Access tenant-specific protected data for the authenticated user.
        
        Args:
            resource_id (optional): Specific resource to access
        """
        request = current_request.get()
        user = getattr(request.state, "user", {})            
        tenant_id = user.get("tenant_id")
        
        # Get all resources for tenant
        tenant_resources = TENANT_RESOURCES.get(tenant_id, [])
        
        if resource_id:
            # Filter for specific resource
            resource_id = resource_id.strip()
            for resource in tenant_resources:
                if resource.id == resource_id:
                    if can_access_resource(user, resource):
                        return f"Resource {resource_id} data: [Details...]"
                    else:
                        return "Access denied to this resource"
            return f"Resource {resource_id} not found for tenant"
        
        # Return all accessible resources
        accessible_resources = [
            res.id for res in tenant_resources 
            if can_access_resource(user, res)
        ]
        
        if not accessible_resources:
            return "No accessible resources found"
            
        return f"Accessible resources for tenant {tenant_id}:\n" + "\n".join(accessible_resources)
