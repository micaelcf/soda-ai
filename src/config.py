from pydantic import BaseModel
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    """Server config settings."""

    root_url: str = getenv("ROOT_URL", default="http://localhost:8080")

    # Security settings
    authjwt_secret_key: str = getenv("SECRET_JWT", default="mysupersecretkey")
    database_url: str = getenv("DATABASE_URL", default="sqlite:///database.db")
    gemini_api_key: str = getenv("GOOGLE_API_KEY", default="your-google-api-key")

    # testing: bool = getenv("TESTING", default=False, cast=bool)


CONFIG = Settings()
