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
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    stock INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Product labels table
CREATE TABLE IF NOT EXISTS labels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Product-Labels relationship table
CREATE TABLE IF NOT EXISTS product_labels (
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    label_id INTEGER REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, label_id)
);

-- Product specifications table
CREATE TABLE IF NOT EXISTS product_specs (
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    spec_key VARCHAR(100) NOT NULL,
    spec_value TEXT NOT NULL,
    PRIMARY KEY (product_id, spec_key)
);
```