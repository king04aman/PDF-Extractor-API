from app.auth import PDFExtractor, hash_password, verify_password, create_access_token, get_current_user, Token, TokenData 
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from collections import defaultdict
from typing import List
from uuid import uuid4
from typing import Dict
import logging
import base64
import os

app = FastAPI()

# Example user storage - placeholder for actual data
fake_users_db = {
    "TSPABAP": {
        "username": "TSP ABAPers",
        "password": hash_password("<REPLACE_WITH_SECURE_PASSWORD>")  # Placeholder for password
    }
}

# Define folder for file uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Request body model for extraction
class ExtractionRequest(BaseModel):
    file_id: str
    keywords: List[str]
    prompt: str

# Model for handling file uploads
class FileUpload(BaseModel):
    base64_string: str

# User models for authentication
class User(BaseModel):
    username: str

class UserInDB(User):
    password: str

# Configure logging
file_store = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiter storage and settings
rate_limit_data: Dict[str, list] = defaultdict(list)
RATE_LIMIT = 100
TIME_WINDOW = timedelta(minutes=1)

# Rate limiter function
def rate_limiter(request: Request):
    client_ip = request.client.host
    now = datetime.now()

    # Cleanup old requests beyond the time window
    rate_limit_data[client_ip] = [timestamp for timestamp in rate_limit_data[client_ip] if now - timestamp < TIME_WINDOW]

    # Enforce rate limiting
    if len(rate_limit_data[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

    # Log the current request
    rate_limit_data[client_ip].append(now)

# Middleware for rate limiting
@app.middleware("http")
async def add_rate_limit(request: Request, call_next):
    try:
        rate_limiter(request)
        response = await call_next(request)
    except HTTPException as e:
        response = JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    return response

# Token generation for user login
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    
    # Check for valid user and password verification
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate access token for the user
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Secure endpoint to get current user information
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: TokenData = Depends(get_current_user)):
    return {"username": current_user.username}

# File upload handler
@app.post("/upload")
async def upload_file(file_upload: FileUpload):
    try:
        file_id = str(uuid4())  # Generate unique file ID
        file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}-converted_pdf.pdf")
        
        # Decode the base64 file and save it to the server
        decoded_bytes = base64.b64decode(file_upload.base64_string)
        with open(file_path, 'wb') as output_file:
            output_file.write(decoded_bytes)

        file_store[file_id] = file_path  # Store file path
        return JSONResponse(content={"file_id": file_id, "file_path": file_path}, status_code=200)
    except Exception as e:
        # Log and return error in case of failure
        logger.error(f"File upload failed: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Endpoint for extracting header information from a PDF
@app.post("/extract-header")
async def extract_header(request: ExtractionRequest):
    try:
        # Check if the file exists in storage
        if request.file_id not in file_store:
            raise HTTPException(status_code=404, detail="File not found")

        file_path = file_store[request.file_id]
        pdf_extractor = PDFExtractor()  # Initialize PDF extractor
        content = pdf_extractor.extract_header_from_pdf(request.keywords, request.prompt, file_path)

        # Return extracted header information
        return JSONResponse(content={"header_info": content}, status_code=200)
    except Exception as e:
        # Log and return error in case of failure
        logger.error(f"Header extraction failed: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Endpoint for extracting item information from a PDF
@app.post("/extract-items")
async def extract_items(request: ExtractionRequest):
    try:
        # Check if the file exists in storage
        if request.file_id not in file_store:
            raise HTTPException(status_code=404, detail="File not found")

        file_path = file_store[request.file_id]
        pdf_extractor = PDFExtractor()  # Initialize PDF extractor
        content = pdf_extractor.extract_item_from_pdf(request.keywords, request.prompt, file_path)

        # Return extracted item information
        return JSONResponse(content={"item_info": content}, status_code=200)
    except Exception as e:
        # Log and return error in case of failure
        logger.error(f"Item extraction failed: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
