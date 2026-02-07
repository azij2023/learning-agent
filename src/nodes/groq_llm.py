from langchain_core.language_models import BaseLanguageModel
from groq import Groq
import os

class GroqLLM(BaseLanguageModel):
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _call(self, prompt, stop=None):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    @property
    def _identifying_params(self):
        return {"model": "llama-3.1-8b-instant"}
