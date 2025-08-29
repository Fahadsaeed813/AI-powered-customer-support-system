import os
import chromadb
from chromadb.config import Settings
from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader, 
    CSVLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeBaseManager:
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Reduced from 1000 to 500
            chunk_overlap=100,  # Reduced from 200 to 100
            length_function=len,
        )
        
        # Initialize Chroma client
        self.chroma_client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize vector store
        self.vector_store = Chroma(
            client=self.chroma_client,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
    
    def load_document(self, file_path: str) -> List[str]:
        """Load document based on file type"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == ".txt":
                loader = TextLoader(file_path, encoding='utf-8')
            elif file_extension == ".pdf":
                loader = PyPDFLoader(file_path)
            elif file_extension == ".csv":
                loader = CSVLoader(file_path)
            elif file_extension == ".md":
                loader = UnstructuredMarkdownLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} documents from {file_path}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            return []
    
    def process_documents(self, documents: List[str]) -> List[str]:
        """Split documents into chunks"""
        try:
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            return []
    
    def add_documents(self, file_paths: List[str]) -> bool:
        """Add documents to knowledge base"""
        try:
            all_chunks = []
            
            for file_path in file_paths:
                if not os.path.exists(file_path):
                    logger.warning(f"File not found: {file_path}")
                    continue
                
                documents = self.load_document(file_path)
                if documents:
                    chunks = self.process_documents(documents)
                    all_chunks.extend(chunks)
            
            if all_chunks:
                # Add to vector store
                self.vector_store.add_documents(all_chunks)
                self.vector_store.persist()
                logger.info(f"Successfully added {len(all_chunks)} chunks to knowledge base")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[str]:
        """Search knowledge base for relevant information"""
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            return []
    
    def get_collection_info(self) -> dict:
        """Get information about the knowledge base"""
        try:
            collection = self.chroma_client.get_collection("langchain")
            count = collection.count()
            return {
                "total_documents": count,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {"total_documents": 0, "persist_directory": self.persist_directory}
    
    def clear_knowledge_base(self) -> bool:
        """Clear all documents from knowledge base"""
        try:
            self.chroma_client.reset()
            logger.info("Knowledge base cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing knowledge base: {str(e)}")
            return False
