from fastapi import FastAPI
from groq import Groq
from classes import MessageRequest
import os
from dotenv import load_dotenv
from starlette.responses import StreamingResponse

load_dotenv()

app = FastAPI()

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)


@app.get("/")
async def chat_llm():
    return {"message": "Hello World"}


@app.post("/send-message")
async def chat_llm(request: MessageRequest):

    print("request.message", request.message)

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role":"system","content": "You are my personal friend called Harry and you will help me with development doubts"},
            {"role": "user", "content": request.message}],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    async def generate():
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""

            yield content

    return StreamingResponse(generate(), media_type="text/plain")
