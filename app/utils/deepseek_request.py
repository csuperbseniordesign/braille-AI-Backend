import requests
import re
import json

def modify_question(questions: dict, name: str, api_key: str) -> dict:
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {api_key}'
    }

    data = {
        "model": "deepseek-chat",
        "messages" : [
            {"role": "system", "content": f"Change the name to {name}"},
            {"role": "user", "content" : f"{questions}"},
        ],
        "stream": False
    }

    # Make the API request
    response = requests.post(url, json=data, headers=headers)

    # Check for success
    if response.status_code == 200:
        response_data = response.json()
        return post_process_json(response_data['choices'][0]['message']['content'])
    
    else:
       print(f"Error {response.status_code}: {response.text}")
       return questions


def post_process_json(response_text: str) -> dict: 
    match = re.search(r'```json\n({.*?})\n```', response_text, re.DOTALL)

    if match:
        json_string = match.group(1)
        data = json.loads(json_string)
        return data
    
    else:
       return response_text