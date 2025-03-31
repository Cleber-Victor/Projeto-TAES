"""
    Esse script implementa o método que recebe um prompt e retorna a chamada do modelo
"""
import os

from groq import Groq

GROQ_API_KEY = "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"

def get_completion(prompt: str, MODEL: str) -> str:

    client = Groq(
    api_key=GROQ_API_KEY,
    )
    
    SYSTEM_PROMPT = "You are an AI that only returns executable code. No explanations, no comments.\
    Provide a functioning implementation in Python for the given problem\n"

    chat_completion = client.chat.completions.create(
    messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
    ],
    model=MODEL,
    )
    
    return chat_completion.choices[0].message.content