from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestModel(BaseModel):
    text: str
    action: str


@app.post("/process")
async def process(request: RequestModel):
    responses = {
        "diagnostic": f"Диагностика: {request.text[:50]}...",
        "recommend": f"Рекомендации: {request.text[:50]}...",
        "explain": f"Объяснение: {request.text[:50]}...",
        "question": f"Вопрос: {request.text[:50]}..."
    }

    return {
        "status": "ok",
        "action": request.action,
        "response": responses.get(request.action, "Неизвестное действие")
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
