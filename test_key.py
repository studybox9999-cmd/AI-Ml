"""Test script to verify API keys are configured correctly.""" 
import os 
from dotenv import load_dotenv 
  
load_dotenv() 
  
anthropic_key = os.getenv("ANTHROPIC_API_KEY") 
openai_key = os.getenv("OPENAI_API_KEY") 
  
print("API Key Status:") 
print(f"  Anthropic: {'Found' if anthropic_key else 'Missing'}") 
print(f"  OpenAI:    {'Found' if openai_key else 'Missing'}") 
  
if anthropic_key: 
    print(f"  Anthropic key prefix: {anthropic_key[:15]}...") 
if openai_key: 
    print(f"  OpenAI key prefix:    {openai_key[:15]}...")