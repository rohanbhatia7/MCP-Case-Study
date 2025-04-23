import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Define a test user payload
payload = {
    "sub": "user_123",
    "role": "admin",
    "tenant_id": "tenant_abc"
}

# Create the token, encode the payload using HS256 (ensures authentication and integrity)
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print(f"JWT Token:\n\n{token}\n")

# Show the payload, decode the token
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
print(f"Payload:\n\n{payload}\n")
