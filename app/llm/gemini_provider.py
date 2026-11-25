import time
from google import genai
from app.core.config import settings


class GeminiProvider:
    FALLBACK_MODELS = ["gemini-3.5-flash-lite"]

    def __init__(self, model: str = "gemini-3.5-flash", retries: int = 3):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = model
        self.retries = retries

    def _call(self, model: str, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
        )
        return response.text or ""

    def generate(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        models = [self.model] + [m for m in self.FALLBACK_MODELS if m != self.model]
        last_error = None

        for model in models:
            for attempt in range(self.retries):
                try:
                    return self._call(model, prompt)
                except Exception as e:
                    last_error = e
                    msg = str(e)
                    if "404" in msg or "NOT_FOUND" in msg:
                        break  # model not available, try next model
                    if any(code in msg for code in ("503", "429", "500")):
                        time.sleep(2 ** attempt)
                        continue
                    raise  # auth errors, bad requests etc.

        raise RuntimeError(f"All Gemini models failed: {last_error}")