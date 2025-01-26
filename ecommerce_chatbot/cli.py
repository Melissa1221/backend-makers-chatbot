"""Command-line interface for the e-commerce chatbot."""

import os
from langchain_core.messages import HumanMessage
from .chatbot import create_chatbot, get_initial_message
import click
from app.services.recommendation import RecommendationService

def check_api_key():
    """Check if OpenAI API key is set."""
    if not os.getenv("OPENAI_API_KEY"):
        print("\nError: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key in the .env file or environment variables.")
        return False
    return True

@click.group()
def cli():
    pass

@cli.command()
def update_recommendations():
    """Actualiza las recomendaciones de productos"""
    click.echo("Actualizando recomendaciones de productos...")
    service = RecommendationService()
    service.update_recommendations()
    click.echo("¡Recomendaciones actualizadas exitosamente!")

if __name__ == '__main__':
    cli()