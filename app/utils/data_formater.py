from app.models import Paragraph

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

def format_to_paragraph_object(paragraph: Paragraph):

    # find option1 & answer1 for question1
    answer1, options1 = refine_option([paragraph.q1a1, paragraph.q1a2, paragraph.q1a3, paragraph.q1a4])

    # find option2 & answer2 for question2
    answer2, options2 = refine_option([paragraph.q2a1, paragraph.q2a2, paragraph.q2a3, paragraph.q2a4])

    return {
        "id" : paragraph.id,
        "title": paragraph.title,
        "paragraph": paragraph.paragraph,
        "atos": paragraph.atos,
        "word_count" : paragraph.word_count,
        "interest" : paragraph.interest,
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