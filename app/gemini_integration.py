import google.generativeai as genai
from django.conf import settings

def configure_gemini():
    genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_content(prompt, word_limit=100):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}" 