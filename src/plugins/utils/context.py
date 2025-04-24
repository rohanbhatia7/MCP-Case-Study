from contextvars import ContextVar
from starlette.requests import Request

# Holds the request per async context
current_request: ContextVar[Request] = ContextVar("current_request")
