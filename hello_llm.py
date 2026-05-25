""" 
Your first LLM API call. 
This is the foundational pattern for everything we will build in this course. 
""" 
import os 
from anthropic import Anthropic 
from dotenv import load_dotenv 
  
# Load API keys from .env 
load_dotenv() 
  
# Initialize the client 
client = Anthropic()  # Uses ANTHROPIC_API_KEY from environment 
  
# Make the API call 
response = client.messages.create( 
    model="claude-sonnet-4-5", 
    max_tokens=1024, 
    messages=[ 
        { 
            "role": "user", 
            "content": "In exactly 3 sentences, explain what an AI agent is." 
        } 
    ] 
) 
  
# Print the response 
print("Claude says:\n") 
print(response.content[0].text) 
print(f"\nTokens used — Input: {response.usage.input_tokens}, Output: {response.usage.output_tokens}")