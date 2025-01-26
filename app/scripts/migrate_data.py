"""Script to migrate inventory data to Supabase."""
import asyncio
import os
from dotenv import load_dotenv
from supabase import create_client, Client

from ecommerce_chatbot.inventory import INVENTORY, CATEGORIES, LABELS

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL", ""),
    os.getenv("SUPABASE_KEY", "")
)

async def migrate_data():
    """Migrate inventory data to Supabase."""
    print("Starting data migration...")

    # Step 1: Insert categories
    print("\nInserting categories...")
    category_id_map = {}  # Map category names to their IDs
    for category_key, category_data in CATEGORIES.items():
        result = supabase.table('categories').insert({
            'name': category_data['name'],
            'description': category_data['description']
        }).execute()
        category_id_map[category_key] = result.data[0]['id']
        print(f"✓ Added category: {category_data['name']}")

    # Step 2: Insert labels
    print("\nInserting labels...")
    label_id_map = {}  # Map label names to their IDs
    for label in LABELS:
        result = supabase.table('labels').insert({
            'name': label
        }).execute()
        label_id_map[label] = result.data[0]['id']
        print(f"✓ Added label: {label}")

    # Step 3: Insert products with their specs and labels
    print("\nInserting products with specs and labels...")
    for product_key, product_data in INVENTORY.items():
        # Insert base product data
        product_result = supabase.table('products').insert({
            'name': product_data['name'],
            'price': product_data['price'],
            'description': product_data['description'],
            'stock': product_data['stock'],
            'category_id': category_id_map[product_data['category']],
            'image_url': product_data['image_url']
        }).execute()
        
        product_id = product_result.data[0]['id']
        print(f"✓ Added product: {product_data['name']}")

        # Insert product specifications
        if product_data.get('specs'):
            specs_data = [
                {
                    'product_id': product_id,
                    'spec_key': key,
                    'spec_value': str(value)
                }
                for key, value in product_data['specs'].items()
            ]
            supabase.table('product_specs').insert(specs_data).execute()
            print(f"  ✓ Added specs for: {product_data['name']}")

        # Insert product-label relationships
        if product_data.get('labels'):
            label_relations = [
                {
                    'product_id': product_id,
                    'label_id': label_id_map[label]
                }
                for label in product_data['labels']
            ]
            supabase.table('product_labels').insert(label_relations).execute()
            print(f"  ✓ Added labels for: {product_data['name']}")

    print("\nData migration completed successfully! 🎉")

if __name__ == "__main__":
    asyncio.run(migrate_data()) 