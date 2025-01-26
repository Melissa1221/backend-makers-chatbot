# E-commerce Chatbot

An intelligent e-commerce assistant powered by FastAPI, LangChain, and Supabase, providing product information and recommendations through natural language interaction.

## Features

- 🤖 AI-powered product recommendations using GPT-3.5
- 🔍 Natural language product search
- 📱 RESTful API endpoints for products and categories
- 🗄️ PostgreSQL database with Supabase integration
- 📚 Interactive API documentation (Swagger UI)
- 💬 Real-time chat with WebSocket support

## Tech Stack

- FastAPI
- LangChain
- OpenAI GPT-3.5
- Supabase (PostgreSQL)
- Python 3.8+

## Prerequisites

1. **OpenAI API Key**
   - Get one at: https://platform.openai.com/api-keys

2. **Supabase Project**
   - Create a project at: https://app.supabase.com
   - Get your project URL and anon key from Project Settings > API

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

### Option B: Using Poetry (Recommended)

1. **Install Poetry** (if not already installed)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. **Install dependencies**
```bash
poetry install
```

3. **Set up environment variables**
Create a `.env` file in the root directory:
```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Supabase
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here

# Security
SECRET_KEY=your_secret_key_here  # Change in production!
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. **Initialize the database**
   - Go to your Supabase project's SQL Editor
   - Copy and paste the following SQL to create the tables:

```sql
-- Categories table (Create this first since products reference it)
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    stock INTEGER NOT NULL DEFAULT 0,
    category_id UUID REFERENCES categories(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Product labels table
CREATE TABLE IF NOT EXISTS labels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Product-Labels relationship table
CREATE TABLE IF NOT EXISTS product_labels (
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    label_id UUID REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, label_id)
);

-- Product specifications table
CREATE TABLE IF NOT EXISTS product_specs (
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    spec_key VARCHAR(100) NOT NULL,
    spec_value TEXT NOT NULL,
    PRIMARY KEY (product_id, spec_key)
);
```

5. **Migrate initial data**
```bash
# Using pip/venv
python -m app.scripts.migrate_data

# Using Poetry
poetry run python -m app.scripts.migrate_data
```

6. **Run the server**
```bash
# Using pip/venv
uvicorn app.main:app --reload --port 8000

# Using Poetry
poetry run uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Products
- `GET /api/v1/products` - Get all products
- `GET /api/v1/products/{id}` - Get specific product
- `POST /api/v1/products` - Create a product
- `PUT /api/v1/products/{id}` - Update a product
- `DELETE /api/v1/products/{id}` - Delete a product

### Categories
- `GET /api/v1/categories` - Get all categories
- `GET /api/v1/categories/{id}` - Get specific category
- `POST /api/v1/categories` - Create a category
- `PUT /api/v1/categories/{id}` - Update a category
- `DELETE /api/v1/categories/{id}` - Delete a category

### Chat
- `POST /api/v1/chat`
  ```json
  {
    "message": "What laptops do you have?"
  }
  ```
- `WebSocket /api/v1/chat/ws/{client_id}` - Real-time chat

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Project Structure

```
ecommerce-chatbot/
├── app/
│   ├── main.py           # FastAPI application
│   ├── db/
│   │   └── supabase.py   # Supabase client
│   │   └── models/
│   │   │   ├── product.py    # Product models
│   │   │   └── category.py   # Category models
│   │   ├── routers/
│   │   │   ├── product.py    # Product endpoints
│   │   │   ├── category.py   # Category endpoints
│   │   │   └── chat.py       # Chat endpoints
│   │   └── services/
│   │   │   ├── product.py    # Product service
│   │   │   ├── category.py   # Category service
│   │   │   └── chat.py       # Chat service
│   └── ecommerce_chatbot/
│   │   ├── chatbot.py        # Chatbot logic
│   │   └── inventory.py      # Initial product data
│   ├── requirements.txt      # Python dependencies
│   ├── pyproject.toml       # Poetry configuration
│   └── .env                 # Environment variables
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
The project follows PEP 8 guidelines. We recommend using:
- black for code formatting
- isort for import sorting
- flake8 for linting

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