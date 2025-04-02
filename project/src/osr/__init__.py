# src/osr/__init__.py

from dotenv import load_dotenv  # type: ignore
import os

# Load .env from the project root (OSR/.env)
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(dotenv_path)
