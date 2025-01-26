"""E-commerce chatbot implementation using LangChain and LangGraph."""

import os
from typing import Sequence, TypedDict, Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from .inventory import INVENTORY

# Load environment variables
load_dotenv()

# Initialize the model
model = ChatOpenAI(
    model="gpt-3.5-turbo",  # Changed to a more widely available model
    temperature=0.7
)

# Create the system prompt with inventory context
inventory_str = "\n".join([
    f"{i+1}. {details['name']}: ${details['price']}, Stock: {details['stock']}\n   {details['description']}"
    for i, details in enumerate(INVENTORY.values())
])

SYSTEM_PROMPT = f"""You are a helpful e-commerce assistant. You have access to the following inventory:

{inventory_str}

Help customers by:
1. Answering questions about product availability, prices, and features
2. Making product recommendations based on customer needs
3. Being polite and professional at all times
4. If asked about a product not in the inventory, politely inform that it's not available

When listing products or information:
1. Always use numbered lists (1., 2., 3., etc.)
2. Present one product per line
3. Include the key information: name, price, and stock
4. Add relevant details like specifications when asked

Keep responses concise, organized, and focused on the inventory information provided."""

# Create the prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages")
])

# Define the state schema
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Create message trimmer (to prevent context window overflow)
def trim_messages(messages: list[BaseMessage], max_messages: int = 10) -> list[BaseMessage]:
    """Keep only the last max_messages (plus the system message)."""
    if len(messages) <= max_messages:
        return messages
    # Always keep the system message if it exists
    if isinstance(messages[0], SystemMessage):
        return [messages[0]] + messages[-max_messages + 1:]
    return messages[-max_messages:]

# Define the model call function
def call_model(state: State):
    """Process the current state and generate a response."""
    # Trim messages to prevent context overflow
    trimmed_messages = trim_messages(state["messages"])
    
    # Generate prompt and get response
    prompt = prompt_template.invoke({"messages": trimmed_messages})
    response = model.invoke(prompt)
    
    return {"messages": [response]}

def create_chatbot():
    """Create and return the chatbot application."""
    # Create the graph
    workflow = StateGraph(state_schema=State)
    
    # Add the single node for model calls
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)
    
    # Compile the graph with memory
    return workflow.compile(checkpointer=MemorySaver())

def get_initial_message() -> str:
    """Return the initial greeting message."""
    return "Hello! I'm your e-commerce assistant. How can I help you today?" 