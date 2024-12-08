import os
from typing import Dict
from fastapi import APIRouter, UploadFile, HTTPException
from models.ApiResponse import ApiResponse
from PyPDF2 import PdfReader

from utils.db import delete_chat, get_all_chats, insert_chat, insert_chunk
from utils.pdf_helpers import extract_table_of_contents, process_chapters


# Create a router instance
router = APIRouter()

# Define the folder where uploaded files will be saved
UPLOAD_FOLDER = "uploaded_pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist



@router.post("/new")
async def new_chat(file: UploadFile):
    """
    Handles uploading of a new PDF to create a chat session and saves it in a folder.
    """
    # Validate that the uploaded file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Save the uploaded file to the designated folder
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    
    try:
        # Save file to the server
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    page_numbers = len(PdfReader(file_location).pages)
    id = insert_chat(file.filename, file_location, page_numbers)
    chunks = extract_table_of_contents(file_location)
    chapters = process_chapters(file_location, chunks)
    for chapter in chapters:
        insert_chunk(id, chapter["start_page"], chapter["end_page"], chapter["content"], chapter["title"], chapter["index"])
    # Respond with extracted text and file location
    response: Dict[str, str] = {
        "filename": file.filename,
        "saved_path": file_location,
        "chat_id": id,
        "pages": page_numbers

    }

    return ApiResponse.success("New chat session created and file saved successfully.", response)

@router.get("/")
async def get_all_chat():
    """
    Function to get all chat sessions from the database.
    """
    try:
        chats = get_all_chats()
        return ApiResponse.success("Chat sessions retrieved successfully.", chats)
    except Exception as e:
        return ApiResponse.error(f"Failed to retrieve chat sessions: {str(e)}")
    

@router.delete("/{chat_id}")
async def delete_chat_by_id(chat_id: int):
    """
    Function to delete a chat session by ID.
    Args:
        chat_id: ID of the chat session to be deleted.
    """
    try:
        delete_chat(chat_id)
        return ApiResponse.success(f"Chat session with ID {chat_id} deleted successfully.")
    except Exception as e:
        return ApiResponse.error(f"Failed to delete chat session: {str(e)}")