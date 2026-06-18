from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent    
print("All imports successful!")    
load_dotenv() 
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
) 
def calculator(expression: str) -> str:
    """Perform mathematical calculations."""
    return str(eval(expression)) 
agent = create_agent(
    model=llm,
    tools=[calculator]
) 
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is 25 * 40 + 100?"
            }
        ]
    }
) 
print(response["messages"][-1].content)