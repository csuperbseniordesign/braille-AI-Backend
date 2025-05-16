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
# def test_create_student_initial():
#     student_data_initial = {
#     "grade": "4",
#     "reading_grade" : "3",
#     "gender": "male",
#     "ethnicity" : "asian",
#     "ethnicity_subgroup" : "vietnamese",
#     "from_SA" : 1,
#     "born" : "China",
#     "year" : 2001,
#     "region" : "midwest",
#     "interest" : "entertainment",
#     "language_home" : "vietnamese",
#     "student_id_alt" : "564DR7"
#     }
#     response = client.post("/students/", json=student_data_initial)
#     assert response.status_code == 200
#     # test to see if the json is added to the database
#     student_id = response.json()["id"]

#     student_data = {
#         "q1_result" : True,
#         "q2_result" : False,
#         "cr1_result" : 1,
#         "cr2_result" : 1,
#         "cr3_result" : 1,
#         "cr4_result" : 1,
#         "cr5_result" : 1,
#         "cr6_result" : 1,
#         "cr7_result" : 1,
#         "cr8_result" : 1,
#         "cr9_result" : 1,
#         "cr10_result" : 1,
#         "cr11_result" : 1,
#         "cr12_result" : 1,        
#         "modified_paragraph_id" : 2
#     }
#     response1 = client.put(f"/students/{student_id}", json = student_data)
#     assert response1.status_code == 200
 
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



