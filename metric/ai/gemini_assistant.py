# ai/gemini_assistant.py
import google.genai as genai
from config import GEMINI_API_KEY

class GeminiAI:
    """
    Simple wrapper for Google Gemini AI (GenAI).
    Call query(prompt) to get a text response.
    """

    def __init__(self, api_key=None):
        # Use the config API key if none provided
        self.api_key = api_key or GEMINI_API_KEY
        genai.configure(api_key=self.api_key)

    def query(self, prompt):
        """
        Send a prompt to Gemini AI and get a response.
        Returns the text string.
        """
        try:
            response = genai.TextGeneration.create(
                model="gemini-1",
                prompt=prompt,
                temperature=0.7,
                max_output_tokens=300
            )
            # The generated text is in candidates[0].content
            return response.candidates[0].content
        except Exception as e:
            # Return error message if something goes wrong
            return f"Error contacting Gemini AI: {str(e)}"
