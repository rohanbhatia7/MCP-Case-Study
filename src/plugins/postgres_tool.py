import os
import json
import asyncpg
from typing import Dict, List, Any, Optional
from plugins.utils.utils import current_request, require_permission, Permission

# Connection pool
_pool = None

async def get_pool() -> Optional[asyncpg.Pool]:
    """Get or create connection pool"""
    global _pool
    if _pool is None:
        dsn = os.getenv("POSTGRES_DSN")
        if not dsn:
            print("Warning: POSTGRES_DSN not set. PostgreSQL functionality disabled.")
            return None
            
        try:
            _pool = await asyncpg.create_pool(dsn)
        except Exception as e:
            print(f"Error creating PostgreSQL connection pool: {str(e)}")
            return None
    return _pool

def register_tool(mcp):
    """Register PostgreSQL tools with the MCP server"""
    
    @mcp.tool()
    @require_permission(Permission.QUERY_DB)
    async def postgres_query(query: str, params: list = None) -> str:
        """
        Execute a read-only SQL query against PostgreSQL.
        
        Args:
            query: SQL query to execute (must be SELECT only)
            params: Optional list of parameters
        """
        # Security check - only allow SELECT queries
        if not query.strip().upper().startswith("SELECT"):
            return "Error: Only SELECT queries are allowed"
        
        # Get user info for tenant isolation
        request = current_request.get()
        user = getattr(request.state, "user", {})
        tenant_id = user.get("tenant_id")
        
        # Add tenant filter to query if not admin
        if user.get("role") != "admin" and tenant_id:
            # This is a simple approach - in production you'd use proper query parsing
            if "WHERE" in query.upper():
                query += f" AND tenant_id = '{tenant_id}'"
            else:
                query += f" WHERE tenant_id = '{tenant_id}'"
        
        pool = await get_pool()
        if not pool:
            return "Error: Database connection failed. Make sure POSTGRES_DSN is set."
        
        try:
            # Execute query with tenant isolation
            params = params or []
            rows = await pool.fetch(query, *params)
            
            # Convert results to list of dicts
            result = [dict(row) for row in rows]
            return json.dumps(result, default=str, indent=2)
        except Exception as e:
            return f"Error executing query: {str(e)}"