from decouple import config
from typing import List

class Settings:
    DATABASE_URL: str = config("DATABASE_URL", default="postgresql://user:password@localhost/ecommerce_db")
    SECRET_KEY: str = config("SECRET_KEY", default="your-super-secret-key-change-this")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=60)
    
    # SMTP Email Settings
    SMTP_SERVER: str = config("SMTP_SERVER", default="")
    SMTP_PORT: int = config("SMTP_PORT", cast=int, default=587)
    SMTP_USERNAME: str = config("SMTP_USERNAME", default="")
    SMTP_PASSWORD: str = config("SMTP_PASSWORD", default="")
    EMAIL_FROM: str = config("EMAIL_FROM", default="")
    
    # Application Settings
    DEBUG: bool = config("DEBUG", cast=bool, default=True)
    CORS_ORIGINS: List[str] = config("CORS_ORIGINS", default="http://localhost:3000,https://smart-glossary.netlify.app").split(",")

settings = Settings()
