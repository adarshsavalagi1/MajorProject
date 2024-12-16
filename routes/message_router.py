from fastapi import APIRouter 
from pydantic import BaseModel
from models.ApiResponse import ApiResponse
from utils.chat import get_response
from utils.db import get_data, insert_message


router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str
    
@router.get("/")
async def get_chat(id: int):
    """
    Function to get all chat sessions for a user.
    """
    try:
        chats = get_data(id)
        return ApiResponse.success("Chat sessions retrieved successfully.", chats)
    except Exception as e:
        return ApiResponse.error(f"Failed to retrieve chat sessions: {str(e)}")

@router.post("/chat")
async def create_chat(id: int, chat_request: ChatRequest):
    """
    Function to create a new chat session.
    """
    try:
        prev_data = get_data(id)
        res = get_response( prev_data,chat_request.prompt,  id)
        insert_message(id, chat_request.prompt, res)
        chats = get_data(id)
        return ApiResponse.success("Chat sessions retrieved successfully.", chats)
    except Exception as e:
        return ApiResponse.error(f"Failed to retrieve chat sessions: {str(e)}")