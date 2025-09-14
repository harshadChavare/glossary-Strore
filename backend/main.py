from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base
from app.api.auth.routes import router as auth_router
from app.api.products.routes import router as products_router
from app.api.cart.routes import router as cart_router
from app.api.checkout.routes import router as checkout_router
from app.api.admin.routes import router as admin_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-seed database on startup (add this)
@app.on_event("startup")
async def startup_event():
    from sqlalchemy.orm import sessionmaker
    from app.models.user import User
    from app.models.product import Product
    from app.core.security import get_password_hash
    from sqlalchemy import text
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("Resetting database...")
        
        # Use raw SQL to drop all tables with CASCADE
        db.execute(text("DROP SCHEMA public CASCADE"))
        db.execute(text("CREATE SCHEMA public"))
        db.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
        db.execute(text("GRANT ALL ON SCHEMA public TO public"))
        db.commit()
        
        # Now create all tables fresh
        Base.metadata.create_all(bind=engine)
        
        print("Seeding fresh database...")
        
        # Create admin user
        admin_user = User(
            name="Admin User",
            email="admin@ecommerce.com",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin_user)
        
        # Create regular user  
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
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        print("Database reset and seeded successfully!")
        
    except Exception as e:
        print(f"Error resetting database: {e}")
        db.rollback()
    finally:
        db.close()

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(products_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(checkout_router, prefix="/api")
app.include_router(admin_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
