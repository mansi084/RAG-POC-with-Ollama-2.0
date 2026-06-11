from fastapi import FastAPI, UploadFile, File #Create the API app, handles uploaded files from user, tells FastAPI "this parameter is a file"
from pydantic import BaseModel #Helps define the structure of request data — like what a question request should look like
import shutil #Helps copy the uploaded file and save it to your documents folder
import os #Helps handle file paths and folder operations
from rag_service import RAGService #Imports your RAGService class — the brain of the entire project

app = FastAPI() #creates fast api app

rag_service = RAGService() #Create RAG Service object

class QuestionRequest(BaseModel): #This is the structure of the question request
    question: str

# Endpoint 1 — Upload and train on a document
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    #file-var name, :UploadFile-Type hint — saying "this should be an uploaded file", = File(...) means this field is mandatory
    # Step 1 - Save uploaded file to documents folder
    file_path = f"./documents/{file.filename}"    #file.filename - Name of uploaded file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f) #file.file - Actual file object containing the data
        #copyfileobj(src, dst) → Copies data from a source file object to a destination file object.
        #shutil helps in copying

    # Step 2 - Train RAG on this file
    result = rag_service.train(file_path)

    return {"message": result}


# Endpoint 2 — Ask a question
@app.post("/ask")
async def ask_question(request: QuestionRequest): 
    # QuestionRequest - type hint - The variable request should be an object of type QuestionRequest
    # Get answer from RAG
    answer = rag_service.ask(request.question) #request.question - Get the value stored in the question attribute of the request object.

    return {"answer": answer}

