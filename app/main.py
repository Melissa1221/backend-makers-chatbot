"""Simple FastAPI application for chatbot."""

from typing import Dict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ecommerce_chatbot.chatbot import create_chatbot
from ecommerce_chatbot.inventory import INVENTORY, CATEGORIES, LABELS
from langchain_core.messages import HumanMessage

app = FastAPI(
    title="E-commerce Chatbot API",
    description="Simple API for chatting with the e-commerce assistant",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create chatbot instance
chatbot = create_chatbot()

class ChatMessage(BaseModel):
    """Chat message schema."""
    message: str

class ChatResponse(BaseModel):
    """Chat response schema."""
    response: str

@app.get("/products", tags=["products"])
async def get_products():
    """Get all products."""
    return {
        "products": [
            {
                "id": key,
                **value
            }
            for key, value in INVENTORY.items()
        ]
    }

@app.get("/products/{product_id}", tags=["products"])
async def get_product(product_id: str):
    """Get a specific product by ID."""
    if product_id not in INVENTORY:
        return {"error": "Product not found"}
    return {
        "product": {
            "id": product_id,
            **INVENTORY[product_id]
        }
    }

@app.get("/categories", tags=["categories"])
async def get_categories():
    """Get all product categories."""
    return {
        "categories": [
            {
                "id": key,
                **value
            }
            for key, value in CATEGORIES.items()
        ]
    }

@app.get("/categories/{category_id}/products", tags=["categories"])
async def get_products_by_category(category_id: str):
    """Get all products in a specific category."""
    products = [
        {
            "id": key,
            **value
        }
        for key, value in INVENTORY.items()
        if value["category"] == category_id
    ]
    return {"products": products}

@app.get("/labels", tags=["products"])
async def get_labels():
    """Get all available product labels."""
    return {"labels": LABELS}

@app.post("/chat", response_model=ChatResponse, tags=["chat"])
async def chat(message: ChatMessage):
    """Send a message to the chatbot."""
    # Create message
    user_message = HumanMessage(content=message.message)
    
    # Get chatbot response
    response_content = ""
    async for chunk, _ in chatbot.astream(
        {"messages": [user_message]},
        {"configurable": {"thread_id": "simple_chat"}},
        stream_mode="messages"
    ):
        if hasattr(chunk, 'content'):
            response_content += chunk.content
    
    return ChatResponse(response=response_content)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the E-commerce Chatbot API",
        "endpoints": {
            "products": "/products",
            "categories": "/categories",
            "labels": "/labels",
            "chat": "/chat"
        },
        "docs_url": "/docs"
    } 