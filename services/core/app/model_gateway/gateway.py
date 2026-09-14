from app.model_gateway.models import (
    ChatRequest,
    ChatResponse,
)
from app.model_gateway.ollama import OllamaProvider


class ModelGateway:
    def __init__(self):
        self.ollama = OllamaProvider()

    def chat(self, request: ChatRequest) -> ChatResponse:
        return self.ollama.chat(request)
