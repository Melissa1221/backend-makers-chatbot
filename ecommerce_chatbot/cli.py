"""Command-line interface for the e-commerce chatbot."""

import os
from langchain_core.messages import HumanMessage
from .chatbot import create_chatbot, get_initial_message

def check_api_key():
    """Check if OpenAI API key is set."""
    if not os.getenv("OPENAI_API_KEY"):
        print("\nError: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key in the .env file or environment variables.")
        return False
    return True

def main():
    """Run the chatbot CLI."""
    # Check for API key
    if not check_api_key():
        return
        
    # Create the chatbot
    app = create_chatbot()
    
    # Set up the conversation config
    config = {"configurable": {"thread_id": "cli_session"}}
    
    # Initialize conversation history
    conversation_history = []
    
    # Print welcome message
    print("\nE-commerce Chatbot")
    print("=================")
    print(get_initial_message())
    print("\nType 'quit' to exit.")
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for quit command
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nGoodbye! Have a great day!")
                break
            
            # Add user message to history
            user_message = HumanMessage(content=user_input)
            conversation_history.append(user_message)
            
            # Process user input with full conversation history
            print("\nBot:", end=" ")
            for chunk, _ in app.stream(
                {"messages": conversation_history},
                config,
                stream_mode="messages"
            ):
                if hasattr(chunk, 'content'):
                    print(chunk.content, end="")
                    # Add bot response to history
                    conversation_history.append(chunk)
            print()  # New line after response
            
        except KeyboardInterrupt:
            print("\nGoodbye! Have a great day!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main() 