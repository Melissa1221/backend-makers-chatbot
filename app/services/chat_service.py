"""Chat service with Supabase integration."""
from typing import List
from app.db.supabase import get_supabase
from ecommerce_chatbot.chatbot import create_chatbot
from langchain_core.messages import HumanMessage

class ChatService:
    """Chat service with Supabase integration."""

    def __init__(self):
        """Initialize service with Supabase client and chatbot."""
        self.supabase = get_supabase()
        self.chatbot = create_chatbot()

    async def get_chat_response(self, message: str) -> str:
        """Get chatbot response."""
        # Create message
        user_message = HumanMessage(content=message)
        
        # Get chatbot response
        response_content = ""
        async for chunk, _ in self.chatbot.astream(
            {"messages": [user_message]},
            {"configurable": {"thread_id": "simple_chat"}},
            stream_mode="messages"
        ):
            if hasattr(chunk, 'content'):
                response_content += chunk.content
        
        return response_content

    async def get_product_info(self) -> List[dict]:
        """Get product information from Supabase."""
        result = self.supabase.table('products').select(
            'id', 'name', 'price', 'description', 'stock'
        ).execute()
        return result.data 