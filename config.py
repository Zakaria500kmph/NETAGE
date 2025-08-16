import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Settings:
    # Database Configuration
    DATABASE_HOST = os.getenv("DATABASE_HOST", "dpg-d2g31b75r7bs73eiedhg-a.oregon-postgres.render.com")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "netage_testing")
    DATABASE_USER = os.getenv("DATABASE_USER", "netage_testing_user")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "AxnL2z8PiJWfOn6YEmj4TxGum0qn37ry")
    
    # Construct DATABASE_URL
    DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    
    # Application Configuration
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    
    # API Configuration
    API_TITLE = "NETAGE BI - Party Master API"
    API_DESCRIPTION = "Complete Party Master management system for NETAGE BI"
    API_VERSION = "1.0.0"
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_database_url(cls):
        """Get the database URL for SQLAlchemy"""
        return cls.DATABASE_URL
    
    @classmethod
    def get_database_config(cls):
        """Get database configuration as a dictionary"""
        return {
            "host": cls.DATABASE_HOST,
            "port": cls.DATABASE_PORT,
            "database": cls.DATABASE_NAME,
            "user": cls.DATABASE_USER,
            "password": cls.DATABASE_PASSWORD
        }

# Create a settings instance
settings = Settings()
