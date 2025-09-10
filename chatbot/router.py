from fastapi import APIRouter

chat_router = APIRouter(prefix="/chat")

@chat_router.get("/", tags=["root"], description = "ROOT API")
async def root():
    return {"message" : "chatbot router"}