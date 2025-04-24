import importlib
import os
from plugins.utils.context import current_request

def load_plugins(mcp):
    """
    Load all plugins from the plugins directory.
    Only loads plugins that follow the BasePlugin class pattern.
    """
    plugin_dir = os.path.dirname(__file__)
    
    # Scan for all Python files
    for filename in os.listdir(plugin_dir):
        if filename.startswith("__") or not filename.endswith(".py"):
            continue
        
        module_name = f"plugins.{filename[:-3]}"  # drop `.py`
        module = importlib.import_module(module_name)
        
        # Check if this is a plugin (has a BasePlugin instance)
        plugin_instance = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            try:
                from plugins.utils.base_plugin import BasePlugin
                if isinstance(attr, BasePlugin):
                    plugin_instance = attr
                    break
            except ImportError:
                pass
        
        if plugin_instance:
            # Plugin found
            if plugin_instance.validate_env():
                try:
                    plugin_instance.register_tools(mcp)
                    print(f"Loaded plugin: {plugin_instance.name} v{plugin_instance.version}")
                except Exception as e:
                    print(f"Error loading plugin {plugin_instance.name}: {str(e)}")
            else:
                print(f"Plugin {plugin_instance.name} missing required environment variables: {plugin_instance.required_env_vars}")
