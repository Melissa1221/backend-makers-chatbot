"""Script to migrate existing inventory data to Supabase."""
import asyncio
import uuid
from app.db.supabase import get_supabase
from ecommerce_chatbot.inventory import INVENTORY, CATEGORIES

async def migrate_data():
    """Migrate inventory data to Supabase."""
    supabase = get_supabase()
    
    print("Starting data migration...")
    
    # 1. Insert categories
    print("\nMigrating categories...")
    for category_id, category in CATEGORIES.items():
        result = supabase.table('categories').upsert({
            'id': str(uuid.uuid4()),
            'name': category['name'],
            'description': category['description']
        }).execute()
        print(f"✓ Inserted category: {category['name']}")
    
    # Get category IDs for reference
    categories_result = supabase.table('categories').select('*').execute()
    category_map = {
        cat['name']: cat['id'] 
        for cat in categories_result.data
    }
    
    # 2. Insert products with their relationships
    print("\nMigrating products...")
    for product_id, product in INVENTORY.items():
        # Find category ID
        category_name = CATEGORIES[product['category']]['name']
        category_id = category_map.get(category_name)
        
        # Insert product
        product_result = supabase.table('products').insert({
            'name': product['name'],
            'price': product['price'],
            'description': product['description'],
            'stock': product['stock'],
            'category_id': category_id
        }).execute()
        
        db_product_id = product_result.data[0]['id']
        print(f"✓ Inserted product: {product['name']}")
        
        # Insert product specs
        if product['specs']:
            specs_data = [
                {
                    'product_id': db_product_id,
                    'spec_key': key,
                    'spec_value': str(value)
                }
                for key, value in product['specs'].items()
            ]
            supabase.table('product_specs').insert(specs_data).execute()
            print(f"  ✓ Added {len(specs_data)} specifications")
        
        # Insert labels
        if product['labels']:
            # Ensure labels exist
            for label in product['labels']:
                supabase.table('labels').upsert(
                    {'name': label},
                    on_conflict='name'
                ).execute()
            
            # Get label IDs
            label_results = supabase.table('labels').select('id').in_('name', product['labels']).execute()
            label_ids = [row['id'] for row in label_results.data]
            
            # Create product-label relationships
            label_relations = [
                {'product_id': db_product_id, 'label_id': label_id}
                for label_id in label_ids
            ]
            supabase.table('product_labels').insert(label_relations).execute()
            print(f"  ✓ Added {len(label_relations)} labels")
    
    print("\nMigration completed successfully!")

if __name__ == "__main__":
    asyncio.run(migrate_data()) 