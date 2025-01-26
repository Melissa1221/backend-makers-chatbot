"""Product service with Supabase integration."""
from typing import Dict, List, Optional
from app.db.supabase import get_supabase
from app.models.product import ProductCreate, ProductUpdate, Product

class ProductService:
    """Product service with Supabase integration."""

    def __init__(self):
        """Initialize service with Supabase client."""
        self.supabase = get_supabase()

    async def create_product(self, product: ProductCreate) -> Product:
        """Create a new product."""
        # Insert product base data
        result = self.supabase.table('products').insert({
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'stock': product.stock,
            'category_id': product.category_id,
            'image_url': product.image_url
        }).execute()
        
        product_id = result.data[0]['id']

        # Insert product specs
        if product.specs:
            specs_data = [
                {'product_id': product_id, 'spec_key': k, 'spec_value': v}
                for k, v in product.specs.items()
            ]
            self.supabase.table('product_specs').insert(specs_data).execute()

        # Insert labels
        if product.labels:
            # First, ensure all labels exist
            for label in product.labels:
                self.supabase.table('labels').upsert(
                    {'name': label}, on_conflict='name'
                ).execute()

            # Get label IDs
            label_results = self.supabase.table('labels').select('id').in_('name', product.labels).execute()
            label_ids = [row['id'] for row in label_results.data]

            # Create product-label relationships
            label_relations = [
                {'product_id': product_id, 'label_id': label_id}
                for label_id in label_ids
            ]
            self.supabase.table('product_labels').insert(label_relations).execute()

        return await self.get_product(product_id)

    def _process_product_data(self, product_data: dict, specs_map: Dict[str, Dict[str, str]], labels_map: Dict[str, List[str]]) -> Product:
        """Process product data with its specs and labels."""
        product_id = product_data['id']
        return Product(
            **product_data,
            specs=specs_map.get(product_id, {}),
            labels=labels_map.get(product_id, [])
        )

    async def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by ID."""
        # Get product with specs and labels in a single query
        result = self.supabase.table('products')\
            .select(
                '*',
                count='exact'
            )\
            .eq('id', product_id)\
            .execute()
        
        if not result.data:
            return None

        product_data = result.data[0]

        # Get specs in a single query
        specs_result = self.supabase.table('product_specs')\
            .select('*')\
            .eq('product_id', product_id)\
            .execute()
        specs = {row['spec_key']: row['spec_value'] for row in specs_result.data}

        # Get labels in a single query
        labels_result = self.supabase.table('product_labels')\
            .select('labels(name)')\
            .eq('product_id', product_id)\
            .execute()
        
        labels = [
            row['labels']['name'] 
            for row in labels_result.data 
            if row.get('labels')
        ]

        return Product(
            **product_data,
            specs=specs,
            labels=labels
        )

    async def list_products(self) -> List[Product]:
        """Get all products with optimized queries."""
        # Get all products
        products_result = self.supabase.table('products').select('*').execute()
        if not products_result.data:
            return []

        product_ids = [p['id'] for p in products_result.data]
        
        # Get all specs in a single query
        specs_result = self.supabase.table('product_specs')\
            .select('*')\
            .in_('product_id', product_ids)\
            .execute()
        
        # Create specs map
        specs_map = {}
        for spec in specs_result.data:
            product_id = spec['product_id']
            if product_id not in specs_map:
                specs_map[product_id] = {}
            specs_map[product_id][spec['spec_key']] = spec['spec_value']

        # Get all labels in a single query
        labels_result = self.supabase.table('product_labels')\
            .select('product_id, labels(name)')\
            .in_('product_id', product_ids)\
            .execute()
        
        # Create labels map
        labels_map = {}
        for label_rel in labels_result.data:
            product_id = label_rel['product_id']
            if label_rel.get('labels') and label_rel['labels'].get('name'):
                if product_id not in labels_map:
                    labels_map[product_id] = []
                labels_map[product_id].append(label_rel['labels']['name'])

        # Combine all data
        return [
            self._process_product_data(product_data, specs_map, labels_map)
            for product_data in products_result.data
        ]

    async def update_product(self, product_id: int, product: ProductUpdate) -> Optional[Product]:
        """Update a product."""
        update_data = product.model_dump(exclude_unset=True)

        # Update base product data
        base_fields = {'name', 'price', 'description', 'stock', 'category_id'}
        base_update = {k: v for k, v in update_data.items() if k in base_fields}
        if base_update:
            self.supabase.table('products').update(base_update).eq('id', product_id).execute()

        # Update specs if provided
        if 'specs' in update_data:
            # Delete existing specs
            self.supabase.table('product_specs').delete().eq('product_id', product_id).execute()
            # Insert new specs
            if update_data['specs']:
                specs_data = [
                    {'product_id': product_id, 'spec_key': k, 'spec_value': v}
                    for k, v in update_data['specs'].items()
                ]
                self.supabase.table('product_specs').insert(specs_data).execute()

        # Update labels if provided
        if 'labels' in update_data:
            # Delete existing label relationships
            self.supabase.table('product_labels').delete().eq('product_id', product_id).execute()
            # Insert new labels
            if update_data['labels']:
                # Ensure labels exist
                for label in update_data['labels']:
                    self.supabase.table('labels').upsert(
                        {'name': label}, on_conflict='name'
                    ).execute()

                # Get label IDs and create relationships
                label_results = self.supabase.table('labels').select('id').in_('name', update_data['labels']).execute()
                label_ids = [row['id'] for row in label_results.data]
                label_relations = [
                    {'product_id': product_id, 'label_id': label_id}
                    for label_id in label_ids
                ]
                self.supabase.table('product_labels').insert(label_relations).execute()

        return await self.get_product(product_id)

    async def delete_product(self, product_id: int) -> bool:
        """Delete a product."""
        result = self.supabase.table('products').delete().eq('id', product_id).execute()
        return bool(result.data)

    async def get_products_by_category(self, category_id: int) -> List[Product]:
        """Get all products in a specific category."""
        # Get products in the category
        products_result = self.supabase.table('products')\
            .select('*')\
            .eq('category_id', category_id)\
            .execute()
        
        if not products_result.data:
            return []

        product_ids = [p['id'] for p in products_result.data]
        
        # Get specs and labels using the same optimization as list_products
        specs_result = self.supabase.table('product_specs')\
            .select('*')\
            .in_('product_id', product_ids)\
            .execute()
        
        specs_map = {}
        for spec in specs_result.data:
            product_id = spec['product_id']
            if product_id not in specs_map:
                specs_map[product_id] = {}
            specs_map[product_id][spec['spec_key']] = spec['spec_value']

        labels_result = self.supabase.table('product_labels')\
            .select('product_id, labels(name)')\
            .in_('product_id', product_ids)\
            .execute()
        
        labels_map = {}
        for label_rel in labels_result.data:
            product_id = label_rel['product_id']
            if label_rel.get('labels') and label_rel['labels'].get('name'):
                if product_id not in labels_map:
                    labels_map[product_id] = []
                labels_map[product_id].append(label_rel['labels']['name'])

        return [
            self._process_product_data(product_data, specs_map, labels_map)
            for product_data in products_result.data
        ]

    async def get_products_by_label(self, label_name: str) -> List[Product]:
        """Get all products with a specific label."""
        # Get products with the specified label
        products_result = self.supabase.table('product_labels')\
            .select('products(*)')\
            .eq('labels.name', label_name)\
            .execute()
        
        if not products_result.data:
            return []

        # Extract product data and IDs
        products_data = [
            item['products'] for item in products_result.data 
            if item.get('products')
        ]
        product_ids = [p['id'] for p in products_data]

        if not product_ids:
            return []
        
        # Get specs and labels using the same optimization as list_products
        specs_result = self.supabase.table('product_specs')\
            .select('*')\
            .in_('product_id', product_ids)\
            .execute()
        
        specs_map = {}
        for spec in specs_result.data:
            product_id = spec['product_id']
            if product_id not in specs_map:
                specs_map[product_id] = {}
            specs_map[product_id][spec['spec_key']] = spec['spec_value']

        labels_result = self.supabase.table('product_labels')\
            .select('product_id, labels(name)')\
            .in_('product_id', product_ids)\
            .execute()
        
        labels_map = {}
        for label_rel in labels_result.data:
            product_id = label_rel['product_id']
            if label_rel.get('labels') and label_rel['labels'].get('name'):
                if product_id not in labels_map:
                    labels_map[product_id] = []
                labels_map[product_id].append(label_rel['labels']['name'])

        return [
            self._process_product_data(product_data, specs_map, labels_map)
            for product_data in products_data
        ] 