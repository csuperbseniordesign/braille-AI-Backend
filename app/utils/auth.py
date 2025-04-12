from fastapi import HTTPException, Security
import os
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
LOCAL_MODEL_API = "http://localhost:11434/api/generate"

def verify_api_key(api_key: str = Security(api_key_header)):
    server_api_key = get_api_key()

    if not server_api_key:
        raise HTTPException(status_code=500, detail="API key is not configured on the server")
   
    if api_key != server_api_key:
        raise HTTPException(status_code=403, detail='Could not validate API key')

    return api_key


def get_api_key():
    api_key = os.getenv('API_KEY')
    
    if not api_key:
        print('\033[91mAPI_KEY is set to None. API_KEY not found in enviroment variable\033[0m')
    
    return api_key

def fetch_model_api_key() -> str:
    return os.getenv("DEEPSEEK_API")