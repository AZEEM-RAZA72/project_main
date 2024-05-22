import google.generativeai as genai
import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Set up the model
def query(question, lang):
    prompt = f'''
    The question is {question}
    Now generate general paragraph example sentences in {lang}around 50 words dont exceed.
    Ensure the sentences are structured in format, clear and meaningful, avoiding any use of placeholders special characters.
    Autofill the placeholder with random values.
    format=<!Doctype HTML>
    '''

    print(prompt)
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

def correction_api(original, spoken):
    prompt = f'''
    You are my grammar teacher. I have spoken the following text: "{spoken.strip()}".
    please match the spoken text with the original text: "{original.strip()}".
    highlight mention: fluency score, accuracy score and pronunciation score
    and provide me tips on how to improve my grammar.
    also give me a score on how well I did out of 10.
    display the result in the following format:
    format=<!Doctype HTML>
    '''

    print(prompt)
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
    q = '''Self Introduction in English'''
    ans = query(q)
    print(ans.text)