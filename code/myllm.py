import google.generativeai as genai
import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Set up the model
def query(question):
    prompt = f'''
    You are my english grammer expert. You are going to help me with my english grammer.
    the question is {question}
    Give me paragraph of to introduce yourself in English auto fill the fields.
    format=html
    '''
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                generation_config=generation_config,
                                safety_settings=safety_settings)



    convo = model.start_chat(history=[])
    response = convo.send_message(prompt)
    return response

if __name__ == "__main__":
    q = '''Self Introduction – Different ways to introduce “myself” (and others) in English
There are many different ways to introduce yourself and other people in English.'''
    ans = query(q)
    print(ans.text)