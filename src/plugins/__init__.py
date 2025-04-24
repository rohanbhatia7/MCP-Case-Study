TOOL_REGISTRY = {}

def register_tool(name):
    def wrapper(fn):
        TOOL_REGISTRY[name] = fn
        return fn
    return wrapper
