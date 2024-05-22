import ollama
from ollama import Client , AsyncClient
import asyncio

def query():
    response = ollama.chat(model='llama2', messages=[
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
    ])
    return response['message']['content']




if __name__ == '__main__':
    print(query())