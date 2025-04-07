"""
    Esse script implementa o método que recebe um prompt e retorna a chamada do modelo
"""
import os

from groq import Groq

GROQ_API_KEY = "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"

def get_completion(problem_statement: str, MODEL: str) -> str:

    client = Groq(
    api_key=GROQ_API_KEY,
    )
    
    SYSTEM_PROMPT = "You are an AI that only returns executable code. No explanations, no comments.\
    Provide a functioning implementation in Python for the given problem\n"

    chat_completion = client.chat.completions.create(
    messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": problem_statement}
    ],
    model=MODEL,
    )
    
    return chat_completion.choices[0].message.content

def get_completion_with_feedback(problem_statement: str, previous_attempt: str,\
                                tester_feedback: str, MODEL: str) -> str:

    client = Groq(
    api_key=GROQ_API_KEY,
    )
    
    SYSTEM_PROMPT = "You are an AI that only returns executable code. No explanations, no comments.\
    Provide a functioning implementation in Python for the given problem.\n \
    Your previous attempt at solving this problem, plus the corresponding error, is provided.\n"

    USER_PROMPT = "Problem statement:\n" + problem_statement
    USER_PROMPT += "Previous attempt:\n" + previous_attempt
    USER_PROMPT += "Tester feedback:\n" + tester_feedback

    chat_completion = client.chat.completions.create(
    messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
    ],
    model=MODEL,
    )
    
    return chat_completion.choices[0].message.content