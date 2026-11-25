
from app.llm.gemini_provider import GeminiProvider


try:
    gemini = GeminiProvider()

    response = gemini.generate(
        "Reply with exactly: Gemini connection successful."
    )

    print("Gemini API Connection: SUCCESS")
    print("Gemini Response:", response)

except Exception as error:
    print("Gemini API Connection: FAILED")
    print("Error:", type(error).__name__, str(error))
