from app.models import Paragraph
from app.utils.auth import fetch_model_api_key
from app.utils.deepseek_request import modify_question

def refine_option(option: list) -> list:
    answer = ""
    option_list = []

    for i in range(len(option)):
        answer_option = option[i]
        
        if option[i].startswith("\\*"):
            answer = answer_option.replace("\\*", "")
            option_list.append(answer.strip())

        else:
            option_list.append(answer_option.strip())
    
    return answer.strip(), option_list

def format_to_paragraph_object(paragraph: Paragraph, target_name: str) -> dict:
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
    modified_question = modify_question(questions=questions, name=target_name, api_key=api_key)

    return modified_question