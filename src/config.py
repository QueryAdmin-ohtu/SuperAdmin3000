import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

""" 
Load .env file if one is found. Create variables that can be used in the project.
"""
try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

# ENVIRONMENT = os.getenv("ENVIRONMENT") or "production" # If environment variable is not defined it defaults to production
PORT = os.environ.get("PORT", 5000)
