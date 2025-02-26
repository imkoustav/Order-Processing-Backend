# import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg://ecommerce_user:admin@localhost:5432/ecommerce_db")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "").replace(
#         "postgres://", "postgresql+psycopg2://", 1
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "").replace(
#         "postgres://", "postgresql+psycopg2://", 1  # Convert to SQLAlchemy-compatible format
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# import os
# from dotenv import load_dotenv

# load_dotenv()  # ✅ Ensure environment variables are loaded

# SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # ✅ Correctly read from .env

# if not SQLALCHEMY_DATABASE_URI:
#     raise ValueError("❌ DATABASE_URL is not set. Check your .env file.")

import os
from dotenv import load_dotenv

load_dotenv()  # ✅ Load environment variables
#print("DATABASE_URL from os.environ:", os.environ.get("DATABASE_URL"))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # ✅ Use .env variable
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #print(SQLALCHEMY_DATABASE_URI)



