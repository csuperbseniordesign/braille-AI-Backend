from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
#### (Use in bash to test post)
## PYTHONPATH=. pytest  
####
# def test_create_paragraph_real_db():
#     paragraph_data = {
#         "title": "Testing Paragraph",
#         "paragraph" : "This is a test!",
#         "word_count" : 8,
#         "atos" : 8.8,
#         "q1" : "what?",
#         "q1a1" : "1",
#         "q1a2" : "2",
#         "q1a3" : "3",
#         "q1a4" : "4",
#         "q2" : "where?",
#         "q2a1" : "1",
#         "q2a2" : "2",
#         "q2a3" : "3",
#         "q2a4" : "4",
#         "interest" : "entertainment"

#     }

#     response = client.post("/paragraphs/", json=paragraph_data)
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["title"] == "Testing Paragraph"
#     assert "id" in data

# function to send a request to submit a modified paragraph form
# def test_create_modified_paragraph():
#     modified_paragraph_data = {
#     "paragraph" : "New modified paragraph",
#     "atos" : 5.5,
#     "used" : 0,
#     "cr_avg": 0,
#     "ethnicity" : "asian",
#     "gender" : "male",
#     "q1" : "first modified question", 
#     "q1a1" : "choice 1",
#     "q1a2" : "choice 2",
#     "q1a3" : "choice 3",
#     "q1a4" : "choice 4",
#     "q2" : "second modified question",
#     "q2a1" : "choice 1",
#     "q2a2" : "choice 2",
#     "q2a3" : "choice 3",
#     "q2a4" : "choice 4", 
#     "interest" : "entertainment"  
#     }
#     response = client.post("/modified_paragraphs/", json=modified_paragraph_data)

#     assert response.status_code == 200
#     # test to see if the json is added to the database
#     data = response.json()
#     assert data["paragraph"] == "New modified paragraph"
#     assert "id" in data


# function to send a request to submit a student form to mysql
def test_create_student_paragraph():
    student_data = {
    "grade": "4",
    "ethnicity" : "asian",
    "gender": "male",
    "q1_result": 1,
    "q2_result": 0,
    "cr1_result" : 1,
    "cr2_result" : 2,
    "cr3_result" : 3,
    "cr4_result" : 4,
    "cr5_result" : 1,
    "cr6_result" : 2,
    "cr7_result" : 3,
    "cr8_result" : 4,
    "interest" : "entertainment",
    "born" : "China",
    "region" : "midwest",
    "year" : 2001,
    "modified_paragraph_id" : 3,
    "reading_grade" : "3",
    "from_SA" : 0
    }
    response = client.post("/students/", json=student_data)
    assert response.status_code == 200
    # test to see if the json is added to the database
    data = response.json()
    assert data["grade"] == "4"
    assert "id" in data

# function to send a request to submit a student form to mysql
# def test_create_student_modified_paragraph():
#     student_modified_paragraph = {
#         "student_id" : 1,
#         "modified_paragraph_id" : 2
#     }
#     response = client.post("/link_student_modified_paragraphs/", json=student_modified_paragraph)
#     assert response.status_code == 200
#     # test to see if the json is added to the database
#     data = response.json()
#     assert data["student_id"] == 1
#     assert "id" in data



