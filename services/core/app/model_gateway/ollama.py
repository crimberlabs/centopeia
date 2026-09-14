import json
import os
import urllib.error
import urllib.request

from app.model_gateway.models import (
    ChatRequest,
    ChatResponse,
)


class OllamaProvider:
    def __init__(self):
        self.base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://10.77.0.2:11434",
        ).rstrip("/")

        self.timeout = float(
            os.getenv("OLLAMA_TIMEOUT_SECONDS", "90")
        )

    def chat(self, request: ChatRequest) -> ChatResponse:
        payload = {
            "model": request.model,
            "messages": [
                message.model_dump()
                for message in request.messages
            ],
            "stream": False,
            "think": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            },
        }

        body = json.dumps(payload).encode("utf-8")

        http_request = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=body,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                http_request,
                timeout=self.timeout,
            ) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

        except urllib.error.HTTPError as exc:
            raise RuntimeError(
                f"Ollama returned HTTP {exc.code}"
            ) from exc

        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Unable to reach Ollama: {exc.reason}"
            ) from exc

        message = data.get("message", {})

        return ChatResponse(
            provider="ollama",
            model=data.get("model", request.model),
            content=message.get("content", ""),
            input_tokens=data.get("prompt_eval_count"),
            output_tokens=data.get("eval_count"),
            total_duration_ms=self._ns_to_ms(
                data.get("total_duration")
            ),
            load_duration_ms=self._ns_to_ms(
                data.get("load_duration")
            ),
            prompt_eval_duration_ms=self._ns_to_ms(
                data.get("prompt_eval_duration")
            ),
            eval_duration_ms=self._ns_to_ms(
                data.get("eval_duration")
            ),
        )

    @staticmethod
    def _ns_to_ms(value):
        if value is None:
            return None

        return round(value / 1_000_000, 3)
