"""
Application configuration settings.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(BASE_DIR, "chroma_langchain_db")

CSV_FILE_PATH = os.path.join(DATA_DIR, "realistic_restaurant_reviews.csv")

EMBEDDING_MODEL = "mxbai-embed-large"
LLM_MODEL = "phi"

COLLECTION_NAME = "restaurant_reviews"
SEARCH_KWARGS = {"k": 5}


# Streamlit UI configurations
UI = {
    "page_title": "🍕 Pizza Review Assistant",
    "page_icon": "🍕",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

MAX_HISTORY = 50 