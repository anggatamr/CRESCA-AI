"""
Quick verification test for Gemini API connection using the new google-genai SDK.
"""

import os
from dotenv import load_dotenv
from google import genai

# Load API Key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def test_gemini_connectivity():
    print("Testing connection to Gemini 3.6 Flash...")
    assert api_key, "GEMINI_API_KEY is not set!"
    
    client = genai.Client(api_key=api_key)
    
    # Send a lightweight test prompt to gemini-3.6-flash
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Hello Gemini! Confirm that Cresca AI Sentinel agent is ready to initialize."
    )
    
    print("\n--- Gemini Response ---")
    print(response.text)
    print("-----------------------")
    print("Gemini API connection verified successfully!")

if __name__ == "__main__":
    test_gemini_connectivity()
