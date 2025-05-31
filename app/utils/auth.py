import os

def get_api_key():
    api_key = os.getenv('API_KEY')
    
    if not api_key:
        print('\033[91mAPI_KEY is set to None. API_KEY not found in enviroment variable\033[0m')
    
    return api_key

def fetch_model_api_key() -> str:
    return os.getenv("DEEPSEEK_API")