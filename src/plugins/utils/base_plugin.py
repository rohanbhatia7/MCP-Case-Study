from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Optional
from mcp.server.fastmcp import FastMCP

class BasePlugin(ABC):
    """Base class for all MCP server plugins"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the plugin"""
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the plugin"""
        pass
        
    @property
    def description(self) -> str:
        """Description of the plugin"""
        return "MCP server plugin"
    
    @property
    def required_env_vars(self) -> List[str]:
        """List of required environment variables"""
        return []
    
    def validate_env(self) -> bool:
        """Validate that required environment variables are set"""
        import os
        return all(os.getenv(var) for var in self.required_env_vars)
    
    @abstractmethod
    def register_tools(self, mcp: FastMCP) -> None:
        """Register tools with the MCP server"""
        pass