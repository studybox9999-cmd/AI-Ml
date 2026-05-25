""" 
Explore how parameters change LLM behavior. 
""" 
import os 
from anthropic import Anthropic 
from dotenv import load_dotenv 
from rich.console import Console 
from rich.table import Table 
  
load_dotenv() 
console = Console() 
client = Anthropic() 
  
PROMPT = "Write the opening sentence of a sci-fi novel about a sentient AI." 
  
  
def call_with_temperature(temp: float, runs: int = 3) -> list[str]: 
    """Make multiple calls at a given temperature to observe variability.""" 
    outputs = [] 
    for _ in range(runs): 
        response = client.messages.create( 
            model="claude-sonnet-4-5", 
            max_tokens=100, 
            temperature=temp, 
            messages=[{"role": "user", "content": PROMPT}] 
        ) 
        outputs.append(response.content[0].text) 
    return outputs 
  
  
def main(): 
    console.print("[bold cyan]Temperature Exploration[/bold cyan]") 
    console.print(f"Prompt: [italic]{PROMPT}[/italic]\n") 
  
    # Test three temperature settings 
    for temp in [0.0, 0.7, 1.0]: 
        table = Table(title=f"Temperature = {temp}", show_lines=True) 
        table.add_column("Run", style="cyan", width=5) 
        table.add_column("Output", style="white") 
  
        outputs = call_with_temperature(temp, runs=3) 
        for i, output in enumerate(outputs, 1): 
            table.add_row(str(i), output.strip()) 
  
        console.print(table) 
        console.print() 
        if __name__ == "__main__": 
            main()