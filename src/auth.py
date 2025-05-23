import os
import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from plugins.utils.utils import current_request

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Store the current user's details for RBAC later
        current_request.set(request)

        # Ensure there is an Authorization Token
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer"):
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
        # Retrieve the encoded token and classified secret key to decode it
        token = auth.split(" ")[1]
        SECRET_KEY = os.getenv("SECRET_KEY")
        if not SECRET_KEY:
            return JSONResponse({"error": "Server misconfigured — no SECRET_KEY set"}, status_code=500)
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.state.user = payload
        except jwt.ExpiredSignatureError:
            return JSONResponse({"error": "Token expired"}, status_code=401)
        except jwt.InvalidTokenError:
            return JSONResponse({"error": "Invalid token"}, status_code=401)
        
        return await call_next(request)
