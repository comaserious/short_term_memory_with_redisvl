from fastapi import FastAPI

app = FastAPI()

from chatbot.router import chat_router
routers = [chat_router]

for router in routers:
    app.include_router(router)

@app.get("/", tags=["root"], description = "ROOT API")
async def root():
    return {"message" : "WELCOME CHATBOT TEST"}