import jwt
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def generate_token(user_id, role, tenant_id):
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY not set.")

    payload = {
        "sub": user_id,
        "role": role,
        "tenant_id": tenant_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_token.py <user_id> <role> <tenant_id>")
        sys.exit(1)
    
    user_id, role, tenant_id = sys.argv[1:4]
    token = generate_token(user_id, role, tenant_id)
    print("\nGenerated JWT:\n")
    print(token)
    print()
