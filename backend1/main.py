# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from users import router as user_router
from products import router as product_router
# from products import router as product_router  # <-- ✅ import product router


import uvicorn

app = FastAPI()

# CORS (dev purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(user_router)
# app.include_router(glossary_router)
app.include_router(product_router)  # <-- ✅ register the new product router
app.include_router(glossary_cart_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
