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
