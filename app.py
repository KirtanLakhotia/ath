from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import base64
import mimetypes
import io


app = FastAPI()

# Input model
class InputModel(BaseModel):
    data: list[str] = []
    file_b64: str = None  # Optional Base64 string for the file

# Response model
class ResponseModel(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    numbers: list[int]
    alphabets: list[str]
    highest_lowercase_alphabet: list[str]
    is_prime_found: bool
    file_valid: bool
    file_mime_type: str = None
    file_size_kb: float = None

# Utility Functions


def detect_mime_type(decoded_file):
    # Known file header patterns (you can add more as needed)
    mime_types = {
        b"\x89PNG\r\n\x1a\n": "image/png",
        b"\xFF\xD8\xFF": "image/jpeg",
        b"%PDF": "application/pdf",
        b"PK\x03\x04": "application/zip",  # ZIP, DOCX, XLSX, etc.
    }

    # Match file header with known patterns
    for header, mime in mime_types.items():
        if decoded_file.startswith(header):
            return mime
    return "application/octet-stream"  # Default if MIME type can't be inferred

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

@app.post("/bfhl")
async def process_data(input_data: InputModel):
    try:
        # Parse input data
        data = input_data.data
        file_b64 = input_data.file_b64
        user_id = "john_doe_17091999"  # Hardcoded for this example
        email = "john@xyz.com"
        roll_number = "ABCD123"

        # Separate numbers and alphabets
        numbers = [int(x) for x in data if x.isdigit()]
        alphabets = [x for x in data if x.isalpha()]

        # Find highest lowercase alphabet
        lowercase_alphabets = [x for x in alphabets if x.islower()]
        highest_lowercase = [max(lowercase_alphabets)] if lowercase_alphabets else []

        # Check for prime numbers
        is_prime_found = any(is_prime(int(x)) for x in numbers)

        # Decode Base64 file if provided
        file_valid = False
        file_mime_type = None
        file_size_kb = None

        if file_b64:
            try:
                # Decode Base64 string
                decoded_file = base64.b64decode(file_b64)
                file_valid = True

                # Determine MIME type
                # file_mime_type = mimetypes.guess_type("file")[0]
                file_mime_type = detect_mime_type(decoded_file)
                print(file_mime_type)

                # Determine file size in KB
                file_size_kb = len(decoded_file) / 1024
            except Exception:
                file_valid = False

        # Construct response
        response = ResponseModel(
            is_success=True,
            user_id=user_id,
            email=email,
            roll_number=roll_number,
            numbers=numbers,
            alphabets=alphabets,
            highest_lowercase_alphabet=highest_lowercase,
            is_prime_found=is_prime_found,
            file_valid=file_valid,
            file_mime_type=file_mime_type,
            file_size_kb=file_size_kb,
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
