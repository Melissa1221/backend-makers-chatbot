# E-commerce Chatbot

An intelligent e-commerce assistant powered by FastAPI and LangChain, providing product information and recommendations through natural language interaction.

## Features

- 🤖 AI-powered product recommendations
- 🔍 Natural language product search
- 📱 RESTful API endpoints for products and categories
- 🔐 Simple in-memory data storage for testing
- 📚 Interactive API documentation (Swagger UI)

## Tech Stack

- FastAPI
- LangChain
- OpenAI GPT
- Python 3.8+

## Quick Start

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ecommerce-chatbot
```

2. **Choose your installation method:**

### Option A: Using pip and venv

1. **Set up Python virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Option B: Using Poetry

1. **Install Poetry** (if not already installed)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. **Install dependencies**
```bash
poetry install
```

3. **Activate the poetry shell**
```bash
poetry shell
```

3. **Set up environment variables**
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
```

4. **Run the server**
```bash
# If using pip/venv
uvicorn app.main:app --reload --port 8003

# If using Poetry
poetry run uvicorn app.main:app --reload --port 8003
```

The API will be available at `http://localhost:8003`

## API Endpoints

### Products

- `GET /products` - Get all products
- `GET /products/{product_id}` - Get specific product details
- `GET /categories` - Get all product categories
- `GET /categories/{category_id}/products` - Get products by category
- `GET /labels` - Get all product labels

### Chat

- `POST /chat`
  ```json
  {
    "message": "What laptops do you have?"
  }
  ```

## API Documentation

Visit `http://localhost:8003/docs` for interactive Swagger documentation.

## Project Structure

```
ecommerce-chatbot/
├── app/
│   ├── main.py           # FastAPI application
│   └── services/
│       └── chat.py       # Chat service
├── ecommerce_chatbot/
│   ├── chatbot.py        # Chatbot logic
│   └── inventory.py      # Product data
├── requirements.txt      # Python dependencies
├── pyproject.toml       # Poetry configuration
└── .env                 # Environment variables
```

## Development

### Running Tests
```bash
# Using pip/venv
pytest

# Using Poetry
poetry run pytest
```

### Code Style
The project follows PEP 8 guidelines.

## Available Products

The chatbot has information about various products including:
- Laptops (HP, Dell, MacBook)
- Smartphones (Samsung, iPhone)
- Audio devices (Sony, Bose)
- Wearables (Apple Watch, Fitbit)
- Tablets (Lenovo)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.