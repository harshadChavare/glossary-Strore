from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.product import Product
from app.core.security import get_password_hash
from app.core.config import settings
from app.db.database import Base
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def seed_database():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = db.query(User).filter(User.email == "admin@ecommerce.com").first()
        if not admin_user:
            admin_user = User(
                name="Admin User",
                email="admin@ecommerce.com",
                password_hash=get_password_hash("admin123"),
                role="admin"
            )
            db.add(admin_user)
        
        # Create regular user
        regular_user = db.query(User).filter(User.email == "user@ecommerce.com").first()
        if not regular_user:
            regular_user = User(
                name="Regular User",
                email="user@ecommerce.com",
                password_hash=get_password_hash("user123"),
                role="user"
            )
            db.add(regular_user)
        
        # Create products
        products_data = [
            {"category": "Fruits", "name": "Apple", "price": 1.2, "stock": 100},
            {"category": "Fruits", "name": "Banana", "price": 0.8, "stock": 150},
            {"category": "Fruits", "name": "Orange", "price": 1.5, "stock": 80},
            {"category": "Vegetables", "name": "Carrot", "price": 0.5, "stock": 200},
            {"category": "Vegetables", "name": "Broccoli", "price": 2.0, "stock": 50},
            {"category": "Vegetables", "name": "Spinach", "price": 1.8, "stock": 75},
            {"category": "Dairy", "name": "Milk", "price": 3.5, "stock": 60},
            {"category": "Dairy", "name": "Cheese", "price": 5.0, "stock": 40},
            {"category": "Dairy", "name": "Yogurt", "price": 2.5, "stock": 90},
            {"category": "Grains", "name": "Rice", "price": 4.0, "stock": 120},
            {"category": "Grains", "name": "Wheat Flour", "price": 3.0, "stock": 100},
            {"category": "Beverages", "name": "Orange Juice", "price": 4.5, "stock": 70}
        ]
        
        for product_data in products_data:
            existing_product = db.query(Product).filter(Product.name == product_data["name"]).first()
            if not existing_product:
                product = Product(**product_data)
                db.add(product)
        
        db.commit()
        print("Database seeded successfully!")
        print("\nCredentials:")
        print("Admin: admin@ecommerce.com / admin123")
        print("User: user@ecommerce.com / user123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
