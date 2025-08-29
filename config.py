import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Google Gemini Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Vector Database Configuration
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")
    
    # Agent Configuration
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Knowledge Base Configuration
    KNOWLEDGE_BASE_DIR = "./data/knowledge_base"
    SUPPORTED_FILE_TYPES = [".txt", ".pdf", ".md", ".csv"]
    
    # UI Configuration
    STREAMLIT_TITLE = "AI Customer Support Agent"
    STREAMLIT_PAGE_ICON = "🤖"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required. Please set it in your .env file")
        
        # Create necessary directories
        os.makedirs(cls.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        os.makedirs(cls.KNOWLEDGE_BASE_DIR, exist_ok=True)
        
        return True
