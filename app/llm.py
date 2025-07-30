"""OpenAI LLM helper."""

from __future__ import annotations

import os
from openai import OpenAI
from dotenv import dotenv_values


def _load_api_key() -> str | None:
    """Load ``OPENAI_API_KEY`` from ``.envrc`` or environment variables."""
    env = dotenv_values(".envrc")
    return env.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")


API_KEY = _load_api_key()
if not API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY not found. Set it in a .envrc file or as an environment variable."
    )

client = OpenAI(api_key=API_KEY)

def llm(prompt, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
