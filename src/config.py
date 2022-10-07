from os import path, getenv, environ
from dotenv import load_dotenv

dirname = path.dirname(__file__)

"""
Load .env file if one is found. Create variables that can be used in the project.
"""
try:
    load_dotenv(dotenv_path=path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

# ENVIRONMENT = getenv("ENVIRONMENT") or "production"
# If environment variable is not defined it defaults to production

PORT = environ.get("PORT", 5000)

SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")

class Config:
    """Set base Flask config variables"""
    SECRET_KEY = getenv("SECRET_KEY")
    CLIENT_ID = getenv("GOOGLE_CLIENT_ID")
    ENV = getenv("ENVIRONMENT")

    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """Production config vars"""
    GOOGLE_URI = getenv("PROD_GOOGLE_URI")


class LocalConfig(Config):
    """Development config vars"""
    GOOGLE_URI = getenv("LOCAL_GOOGLE_URI")


class TestConfig(Config):
    """Test environment config vars"""
    GOOGLE_URI = getenv("TEST_GOOGLE_URI")


def load_config(mode=getenv("ENVIRONMENT")):
    """Load configuration to app"""
    try:
        if mode == "local":
            return LocalConfig
        if mode == "prod":
            return ProdConfig
        if mode == "test":
            return TestConfig
        return None
    except ImportError:
        # TODO: default to production?
        return None
