"""Extended inventory data for Makers Tech e-commerce chatbot."""

# Category image URLs
CATEGORY_IMAGES = {
    "computers": "https://images.unsplash.com/photo-1621361365424-06f0e1eb5c49?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cHJvZHVjdG9zJTIwZGUlMjB0ZWNub2xvZ2lhfGVufDB8fDB8fHww",
    "phones": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "audio": "https://images.unsplash.com/photo-1603389335957-10bea39c9d32?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cHJvZHVjdG9zJTIwZGUlMjB0ZWNub2xvZ2lhfGVufDB8fDB8fHww",
    "wearables": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?q=80&w=1854&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
}

INVENTORY = {
    "hp_laptop": {
        "name": "HP Pavilion 15",
        "price": 749.99,
        "description": "Laptop HP Pavilion con procesador Intel Core i5, 8GB de RAM y 256GB SSD.",
        "stock": 5,
        "category": "computers",
        "image_url": CATEGORY_IMAGES["computers"],
        "labels": ["electronics", "work", "portable", "budget"],
        "specs": {
            "ram": "8GB",
            "storage": "256GB SSD",
            "processor": "Intel Core i5",
            "screen": "15.6 inch Full HD"
        }
    },
    "dell_laptop": {
        "name": "Dell Inspiron 14",
        "price": 899.99,
        "description": "Laptop Dell Inspiron con procesador Intel Core i7, 16GB RAM y 512GB SSD.",
        "stock": 3,
        "category": "computers",
        "image_url": CATEGORY_IMAGES["computers"],
        "labels": ["electronics", "work", "high-performance", "premium"],
        "specs": {
            "ram": "16GB",
            "storage": "512GB SSD",
            "processor": "Intel Core i7",
            "screen": "14 inch Full HD"
        }
    },
    "apple_laptop": {
        "name": "MacBook Air M1",
        "price": 1099.99,
        "description": "Laptop ligera y potente con chip M1, 8GB RAM y 256GB SSD.",
        "stock": 2,
        "category": "computers",
        "image_url": CATEGORY_IMAGES["computers"],
        "labels": ["electronics", "premium", "portable", "work"],
        "specs": {
            "ram": "8GB",
            "storage": "256GB SSD",
            "processor": "Apple M1",
            "screen": "13.3 inch Retina"
        }
    },
    "samsung_smartphone": {
        "name": "Samsung Galaxy S22",
        "price": 799.99,
        "description": "Smartphone con pantalla AMOLED de 6.1 pulgadas, cámara de 50MP y 5G.",
        "stock": 7,
        "category": "phones",
        "image_url": CATEGORY_IMAGES["phones"],
        "labels": ["electronics", "mobile", "5G", "camera"],
        "specs": {
            "screen": "6.1 inch AMOLED",
            "camera": "50MP triple",
            "battery": "4000mAh",
            "storage": "128GB"
        }
    },
    "iphone_13": {
        "name": "iPhone 13",
        "price": 999.99,
        "description": "El último iPhone con pantalla OLED, A15 Bionic y doble cámara de 12MP.",
        "stock": 4,
        "category": "phones",
        "image_url": CATEGORY_IMAGES["phones"],
        "labels": ["electronics", "mobile", "premium", "camera"],
        "specs": {
            "screen": "6.1 inch OLED",
            "camera": "12MP dual",
            "battery": "3300mAh",
            "storage": "128GB"
        }
    },
    "sony_headphones": {
        "name": "Sony WH-1000XM5",
        "price": 349.99,
        "description": "Auriculares inalámbricos con cancelación activa de ruido y batería de 30 horas.",
        "stock": 10,
        "category": "audio",
        "image_url": CATEGORY_IMAGES["audio"],
        "labels": ["electronics", "music", "wireless", "noise-cancelling"],
        "specs": {
            "battery": "30 hours",
            "connectivity": "Bluetooth 5.2",
            "features": ["Noise cancellation", "Touch controls"]
        }
    },
    "bose_speaker": {
        "name": "Bose SoundLink Mini II",
        "price": 199.99,
        "description": "Altavoz Bluetooth portátil con sonido profundo y batería de 12 horas.",
        "stock": 6,
        "category": "audio",
        "image_url": CATEGORY_IMAGES["audio"],
        "labels": ["electronics", "music", "portable", "wireless"],
        "specs": {
            "battery": "12 hours",
            "connectivity": "Bluetooth",
            "features": ["Deep sound", "Compact design"]
        }
    },
    "apple_watch": {
        "name": "Apple Watch Series 8",
        "price": 399.99,
        "description": "Reloj inteligente con sensores avanzados de salud y seguimiento de actividad.",
        "stock": 8,
        "category": "wearables",
        "image_url": CATEGORY_IMAGES["wearables"],
        "labels": ["electronics", "fitness", "health", "premium"],
        "specs": {
            "screen": "1.9 inch OLED",
            "battery": "18 hours",
            "sensors": ["ECG", "Blood oxygen", "GPS"]
        }
    },
    "fitbit_tracker": {
        "name": "Fitbit Charge 5",
        "price": 149.99,
        "description": "Rastreador de actividad con GPS integrado, monitoreo del sueño y más.",
        "stock": 15,
        "category": "wearables",
        "image_url": CATEGORY_IMAGES["wearables"],
        "labels": ["electronics", "fitness", "health", "budget"],
        "specs": {
            "screen": "1.04 inch AMOLED",
            "battery": "7 days",
            "sensors": ["Heart rate", "Sleep tracking", "GPS"]
        }
    },
    "lenovo_tablet": {
        "name": "Lenovo Tab P11 Pro",
        "price": 499.99,
        "description": "Tablet con pantalla OLED de 11.5 pulgadas, 6GB RAM y 128GB de almacenamiento.",
        "stock": 5,
        "category": "computers",
        "image_url": CATEGORY_IMAGES["computers"],
        "labels": ["electronics", "creativity", "portable", "budget"],
        "specs": {
            "screen": "11.5 inch OLED",
            "battery": "15 hours",
            "storage": "128GB",
            "features": ["Stylus support", "Dolby Atmos speakers"]
        }
    }
}

CATEGORIES = {
    "computers": {
        "name": "Laptops y Computadoras",
        "description": "Encuentra las mejores computadoras portátiles y de escritorio."
    },
    "phones": {
        "name": "Smartphones",
        "description": "Dispositivos móviles de última generación."
    },
    "audio": {
        "name": "Audio y Sonido",
        "description": "Auriculares, altavoces y más para los amantes del sonido."
    },
    "wearables": {
        "name": "Tecnología Vestible",
        "description": "Relojes inteligentes y rastreadores de actividad física."
    }
}

LABELS = [
    "electronics", "premium", "budget", "wireless", "portable",
    "high-performance", "work", "camera", "5G", "noise-cancelling",
    "fitness", "health", "creativity", "music", "mobile"
]
