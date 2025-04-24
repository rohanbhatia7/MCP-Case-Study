import os
import json
import asyncpg
from typing import Dict, List, Any, Optional
from plugins.utils.base_plugin import BasePlugin
from plugins.utils.permissions import Permission
from plugins.utils.decorators import require_permission
from plugins.utils.context import current_request

class PostgresPlugin(BasePlugin):
    def __init__(self):
        self.pool = None
        
    @property
    def name(self) -> str:
        return "postgres"
        
    @property
    def version(self) -> str:
        return "1.0.0"
        
    @property
    def description(self) -> str:
        return "PostgreSQL database connector for MCP server"
    
    @property
    def required_env_vars(self) -> List[str]:
        return ["POSTGRES_DSN"]
    
    async def get_pool(self) -> Optional[asyncpg.Pool]:
        """Get or create connection pool"""
        if self.pool is None:
            try:
                dsn = os.getenv("POSTGRES_DSN")
                self.pool = await asyncpg.create_pool(dsn)
            except Exception as e:
                print(f"Error creating PostgreSQL connection pool: {str(e)}")
                return None
        return self.pool
    
    def register_tools(self, mcp):
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
            
            pool = await self.get_pool()
            if not pool:
                return "Error: Database connection failed"
            
            try:
                # Execute query with tenant isolation
                params = params or []
                rows = await pool.fetch(query, *params)
                
                # Convert results to list of dicts
                result = [dict(row) for row in rows]
                return json.dumps(result, default=str, indent=2)
            except Exception as e:
                return f"Error executing query: {str(e)}"

plugin = PostgresPlugin()
