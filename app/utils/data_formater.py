from app.model.models import Paragraph
from app.utils.auth import fetch_model_api_key
from app.utils.deepseek_request import modify_question

def refine_option(options: list) -> tuple[str, list[str]]:
    """
    Extracts the correct answer based on '*' or '\\*' prefix
    and returns (answer, cleaned_options).
    """
    answer = ""
    cleaned_options = []

    for opt in options:
        stripped = opt.strip()

        # Detect correct answer if it starts with '*' OR '\*'
        if stripped.startswith("*") or stripped.startswith("\\*"):
            # Remove ANY leading '*' or '\*'
            cleaned = stripped.lstrip("*").lstrip("\\*").strip()
            answer = cleaned
            cleaned_options.append(cleaned)
        else:
            cleaned_options.append(stripped)

    return answer, cleaned_options


def format_to_paragraph_object(paragraph: Paragraph, target_name: str, target_gender: str) -> dict:
    # get deepseek api key
    api_key = fetch_model_api_key()

    # find option1 & answer1 for question1
    answer1, options1 = refine_option([paragraph.q1a1, paragraph.q1a2, paragraph.q1a3, paragraph.q1a4])

    # find option2 & answer2 for question2
    answer2, options2 = refine_option([paragraph.q2a1, paragraph.q2a2, paragraph.q2a3, paragraph.q2a4])

    questions = {
        "questions": [
            {
                "question": paragraph.q1,
                "options": options1,
                "answer": answer1
            },
            {
                "question": paragraph.q2,
                "options": options2,
                "answer" : answer2
            }
        ]
    }

    if not api_key:
        return paragraph
    
    # call api to modify name and pronouns in questions
    modified_question = modify_question(questions=questions, name=target_name, gender=target_gender, api_key=api_key)

    return modified_question