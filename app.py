from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from utils.db import init_db
from utils.chat import init_chat, is_ready
from models.ApiResponse import ApiResponse
from routes.chat_router import router as chat_router
from routes.message_router import router as message_router

# Define lifespan logic with proper startup/cleanup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle initialization (startup) and cleanup (shutdown) logic.
    """
    try:
        print("Starting application...")
        init_db()
        init_chat()
        yield
    finally:
        print("Application is shutting down...")


app = FastAPI(lifespan=lifespan)
app.include_router(chat_router, prefix="/chat", tags=["chat"]) 
app.include_router(message_router, prefix="/message", tags=["message"])


@app.get("/test")
async def test():
    """
    Route to check if chatbot is ready.
    """
    if not is_ready():
        return ApiResponse.error("Chatbot is not ready")
    return ApiResponse.success("Chatbot is ready")


@app.get("/")
async def root():
    """
    Root endpoint for testing the FastAPI server health.
    """
    return {"message": "FastAPI server is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", port=8000,reload=True)
