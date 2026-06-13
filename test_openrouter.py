from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=[
            {
                "role": "user",
                "content": "What is deep learning?"
            }
        ]
    )

    print("\nResponse:\n")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nERROR:")
    print(e)