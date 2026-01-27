# src/list_models.py
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Inspect the raw output
models = client.models.list()
print("Raw models list:", models)

# If it's a list of dicts, print the keys
for m in models:
    # m might be a tuple like (id, metadata) or a dict
    if isinstance(m, dict):
        print(m.get("id", m))
    elif isinstance(m, tuple):
        print(m[0])  # first element is usually the model name
    else:
        print(m)
