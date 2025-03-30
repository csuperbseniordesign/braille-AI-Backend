from app.utils.auth import verify_api_key, fetch_model_api_key
from app.utils.sys_check import run_system_check
from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi.security.api_key import APIKeyHeader
import httpx
import json
import random
from app.models import Base, Paragraph, Student, ModifiedParagraph, engine, SessionLocal
from app.schemas import ParagraphSchema, StudentSchema, ModifiedParagraphSchema
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

run_system_check()
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow only this origin (frontend)
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allow only these methods
    allow_headers=["*"],  # Allow any headers
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/secure-data")
def secure_data(api_key: str = Depends(verify_api_key)):
    return {"message": "You have access to secure data"}

@app.get("/generate")
async def generate_text(request: Request):
    # extract raw json data
    data = await request.json()
    

    # check if prompt exist
    prompt = data.get("prompt")

    # if prompt doesn't exist
    # return error notify no prompt is given
    if not prompt:
        return {"error" : "Prompt is required"}
    
    json_data = json.dumps(data)
    model_key = fetch_model_api_key()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(model_key, data=json_data)

            if response.status_code != 200:
                return {"response" : response.status_code}
            
        except:
            return {"error" : "unable to connect to local model"}

        # convert response.text to json from string
        response_json = json.loads(response.text)

        return response_json

# needs explanation on how this works
@app.get("/paragraphs/")
def create_paragraph(paragraph: ParagraphSchema, db: Session = Depends(get_db)):
    db_paragraph = Paragraph(**paragraph.model_dump())
    db.add(db_paragraph)
    db.commit()
    db.refresh(db_paragraph)
    return db_paragraph

## get json paragraph based on interest and atos
@app.get("/paragraphs/{interest}/{min_atos}/{max_atos}")
def read_paragraph(interest: str,min_atos: float, max_atos : float, db: Session = Depends(get_db)):
    query = db.query(Paragraph)
    query = query.filter(Paragraph.atos.between(min_atos, max_atos))
    query = query.filter(Paragraph.interest == interest)
    paragraph = query.all()
    if not paragraph:
        raise HTTPException(status_code=404, detail="Paragraph not found")
    return random.choice(paragraph)

@app.get("/paragraph/{paragraph_id}")
def get_paragraph(paragraph_id: int, db: Session = Depends(get_db)):
    paragraph = db.query(Paragraph).filter(Paragraph.id == paragraph_id).first()
    
    if not paragraph:
        print(f"Paragraph with ID {paragraph_id} not found.")  # Logs the issue
        raise HTTPException(status_code=404, detail=f"Paragraph {paragraph_id} not found")
    
    return paragraph

@app.post("/students/")
def create_student(student: StudentSchema, db: Session = Depends(get_db)):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/modified_paragraphs/")
def create_modified_paragraph(modified_paragraph: ModifiedParagraphSchema, db: Session = Depends(get_db)):
    db_modified_paragraph = ModifiedParagraph(**modified_paragraph.model_dump())
    db.add(db_modified_paragraph)
    db.commit()
    db.refresh(db_modified_paragraph)
    return db_modified_paragraph

@app.get("/modified_paragraphs/{modified_paragraph_id}")
def read_modified_paragraph(modified_paragraph_id: int, db: Session = Depends(get_db)):
    modified_paragraph = db.query(ModifiedParagraph).filter(ModifiedParagraph.id == modified_paragraph_id).first()
    if not modified_paragraph:
        raise HTTPException(status_code=404, detail="Modified Paragraph not found")
    return modified_paragraph