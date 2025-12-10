import requests
import re
import json

def modify_question(questions: dict, name: str, gender: str, api_key: str) -> dict:
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    schema = """{
      "questions": [
        {
          "question": "string",
          "options": ["string", "string", "string", "string"],
          "answer": "string"
        }
      ]
    }"""

    system_content = f"""
You are a JSON generator. Always respond ONLY with valid JSON matching this schema:

{schema}

Input will already follow this schema.

CRITICAL INSTRUCTIONS:

NAME REPLACEMENT:
1. Identify the MAIN character in the input questions. This is typically:
   - The character mentioned first
   - The character the questions are primarily about
   - The character performing the main actions
2. Replace THAT SPECIFIC CHARACTER'S NAME ONLY with "{name}" in ALL occurrences in:
   - "question" field
   - "options" array
   - "answer" field
3. Do NOT change other characters' names. Only replace the main character's name.

PRONOUN REPLACEMENT:
1. Update ONLY the main character's pronouns:
   - If "{gender}" = "male": use he/him/his/himself
   - If "{gender}" = "female": use she/her/her/herself
   - If "{gender}" = "nonbinary": use they/them/their/themselves
2. Change pronouns ONLY when they clearly refer to the main character.
3. Make necessary grammatical adjustments for subject-verb agreement.


2d. Change only pronouns referring to the main character; do not change pronouns referring to other entities.
3. Do NOT change which option is correct:
   - The "answer" field must remain the same option as in the input (only name/pronoun changes allowed).
   - Do NOT reorder options.
   - Do NOT add or remove options.
4. Do NOT change any other words except for names and pronouns.
5. Do NOT include asterisks (*) anywhere in the output.
6. Do NOT wrap the JSON in markdown or backticks. Respond with raw JSON only.
7. Do NOT include any additional keys or metadata.
8. Do NOT change all names to "${name}" – only the primary/main character

Output strictly valid JSON and nothing else.
""".strip()

    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": json.dumps(questions),
            },
        ],
        "stream": False,
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        content = response_data["choices"][0]["message"]["content"]
        return post_process_json(content)
    else:
        print(f"Error {response.status_code}: {response.text}")
        return questions  # fallback


# modify_question.py (or wherever this function is)
def post_process_json(response_text: str) -> dict: 
    match = re.search(r'```json\n({.*?})\n```', response_text, re.DOTALL)

    if match:
        json_string = match.group(1)
        data = json.loads(json_string)
        return data
    else:
        # Try to parse the response directly
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            if isinstance(response_text, dict):
                return response_text
            print(f"Failed to parse JSON: {response_text}")
            return {"questions": []}