import importlib
import os
from plugins.utils.utils import current_request

def load_plugins(mcp):
    """
    Load all plugins from the plugins directory that have register_tool functions.
    """
    plugin_dir = os.path.dirname(__file__)
    
    # Scan for all Python files
    for filename in os.listdir(plugin_dir):
        if filename.startswith("__") or not filename.endswith(".py"):
            continue
        
        module_name = f"plugins.{filename[:-3]}"
        try:
            module = importlib.import_module(module_name)
            
            # Check if this module has a register_tool function
            if hasattr(module, "register_tool"):
                try:
                    module.register_tool(mcp)
                    print(f"Loaded plugin: {filename[:-3]}")
                except Exception as e:
                    print(f"Error loading plugin {filename[:-3]}: {str(e)}")
        except ImportError as e:
            print(f"Error importing {module_name}: {str(e)}")