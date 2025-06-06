import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chat.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-random-secret-key")  # For signing tokens/cookies
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day token expiry

