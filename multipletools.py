# Multiple Tools Agent    
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent 
# Load Environment Variables
load_dotenv() 
# LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
) 
# TOOL 1 : Calculator 
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.
    """
    print("\n TOOL CALLED : calculator")
    print(f" INPUT : {expression}") 
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}" 
# TOOL 2 : Text Length 
def text_length(text: str) -> str:
    """
    Returns length of text.
    """
    print("\n TOOL CALLED : text_length")
    print(f" INPUT : {text}") 
    return f"Length of text is {len(text)}" 
# TOOL 3 : Uppercase 
def uppercase(text: str) -> str:
    """
    Convert text to uppercase.
    """
    print("\n TOOL CALLED : uppercase")
    print(f" INPUT : {text}") 
    return text.upper() 
# SYSTEM PROMPT 
system_prompt = """
You are a helpful AI assistant. 
Rules:
1. Use tools whenever a tool can solve the task.
2. Use calculator for mathematical calculations.
3. Use text_length when the user asks for the length of text.
4. Use uppercase when the user asks to convert text to uppercase.
5. If no tool is required, answer normally using your own knowledge.
6. Be concise and accurate.
""" 
# CREATE AGENT 
agent = create_agent(
    model=llm,
    tools=[calculator, text_length, uppercase],
    system_prompt=system_prompt
) 
# TERMINAL CHAT
print("=" * 60)
print(" MULTI TOOL AGENT")
print("Type 'exit', 'quit', or 'q' to stop")
print("=" * 60)

while True: 
    query = input("\n User : ").strip()
    if query.lower() in ["exit", "quit", "q"]:
        print("\n Goodbye!")
        break 
    try:
        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            }
        ) 
        print("\n Agent :", response["messages"][-1].content) 
    except Exception as e:
        print(f"\n Error : {e}")      
