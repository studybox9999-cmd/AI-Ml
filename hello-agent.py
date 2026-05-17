""" 
Hello Agent — a simple multi-turn conversational program. 
This introduces the core loop pattern we'll use throughout the course: 
    perceive (user input) -> reason (LLM call) -> act (output) -> repeat 
""" 
import os 
from anthropic import Anthropic 
from dotenv import load_dotenv 
from rich.console import Console 
from rich.prompt import Prompt 
from rich.panel import Panel 
  
load_dotenv() 
console = Console() 
client = Anthropic() 
  
# System prompt — defines the agent's persona/behavior 
SYSTEM_PROMPT = """You are a friendly and concise AI study buddy for a student 
learning about Agentic AI. Keep responses under 4 sentences unless asked for 
more detail. Use simple analogies when explaining technical concepts.""" 
  
# Conversation history (the agent's "short-term memory") 
conversation_history = [] 
  
  
def chat(user_message: str) -> str: 
    """Send a message to the agent and get a response.""" 
    # Add user message to history 
    conversation_history.append({ 
        "role": "user", 
        "content": user_message 
    }) 
  
    # Make the API call with FULL history (this is what makes it stateful) 
    response = client.messages.create( 
        model="claude-sonnet-4-5", 
        max_tokens=1024, 
        system=SYSTEM_PROMPT, 
        messages=conversation_history 
    )
     # Extract the assistant's response 
    assistant_message = response.content[0].text 
  
    # Add the assistant's response to history (so it remembers what it said) 
    conversation_history.append({ 
        "role": "assistant", 
        "content": assistant_message 
    }) 
  
    return assistant_message 
  
  
def main(): 
    """Run the conversational loop.""" 
    console.print(Panel.fit( 
        "[bold cyan]Hello Agent[/bold cyan]\n" 
        "Your AI study buddy for Agentic AI.\n" 
        "[dim]Type 'quit' or 'exit' to end the conversation.[/dim]", 
        border_style="cyan" 
    )) 
  
    while True: 
        # Get user input 
        user_input = Prompt.ask("\n[bold green]You[/bold green]") 
  
        # Check for exit 
        if user_input.lower() in ["quit", "exit", "bye"]: 
            console.print("\n[yellow]Goodbye! Happy learning![/yellow]") 
            break 
  
        # Get agent response 
        try: 
            response = chat(user_input) 
            console.print(f"\n[bold magenta]Agent[/bold magenta]: {response}") 
        except Exception as e: 
            console.print(f"\n[red]Error: {e}[/red]") 
            break 
  
    # Print conversation stats at the end 
    console.print(f"\n[dim]Total exchanges: {len(conversation_history) // 2}[/dim]") 
  
  
if __name__ == "__main__": 
    main()