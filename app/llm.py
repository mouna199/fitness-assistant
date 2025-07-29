from openai import OpenAI
from dotenv import dotenv_values

env = dotenv_values(".envrc")
client = OpenAI(api_key=env["OPENAI_API_KEY"])

def llm(prompt, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
