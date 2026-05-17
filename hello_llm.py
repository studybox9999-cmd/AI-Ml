"""Same interaction, OpenAI version.""" 
import os 
from openai import OpenAI 
from dotenv import load_dotenv 
  
load_dotenv() 
  
client = OpenAI()  # Uses OPENAI_API_KEY from environment 
  
response = client.chat.completions.create( 
    model="gpt-4o-mini", 
    max_tokens=1024, 
    messages=[ 
        { 
            "role": "user", 
            "content": "In exactly 3 sentences, explain what an AI agent is." 
        } 
    ] 
) 
  
print("GPT says:\n") 
print(response.choices[0].message.content) 
print(f"\nTokens used — Input: {response.usage.prompt_tokens}, Output: {response.usage.completion_tokens}") 