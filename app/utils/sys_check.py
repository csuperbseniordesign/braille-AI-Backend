from app.utils.auth import get_api_key, fetch_model_api_key

def run_system_check():
    get_api_key()
    fetch_model_api_key()