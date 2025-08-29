#!/usr/bin/env python3
"""
Console-based AI Customer Support Agent
For testing and development purposes
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from config import Config
from utils.knowledge_base import KnowledgeBaseManager
from models.ai_agent import CustomerSupportAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsoleInterface:
    def __init__(self):
        self.knowledge_base = None
        self.agent = None
        self.running = False
    
    def initialize_system(self):
        """Initialize the AI agent and knowledge base"""
        try:
            print("🚀 Initializing AI Customer Support System...")
            
            # Validate configuration
            Config.validate()
            print("✅ Configuration validated")
            
            # Initialize knowledge base
            print("📚 Initializing knowledge base...")
            self.knowledge_base = KnowledgeBaseManager(Config.CHROMA_PERSIST_DIRECTORY)
            print("✅ Knowledge base initialized")
            
            # Initialize AI agent
            print("🤖 Initializing AI agent...")
            config_dict = {
                "GOOGLE_API_KEY": Config.GOOGLE_API_KEY,
                "GEMINI_MODEL": Config.GEMINI_MODEL,
                "TEMPERATURE": Config.TEMPERATURE,
                "MAX_TOKENS": Config.MAX_TOKENS
            }
            self.agent = CustomerSupportAgent(self.knowledge_base, config_dict)
            print("✅ AI agent initialized")
            
            print("\n🎉 System ready! Type 'help' for available commands.")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing system: {str(e)}")
            return False
    
    def display_help(self):
        """Display available commands"""
        help_text = """
🤖 AI Customer Support Agent - Available Commands:

📝 Chat Commands:
  - Just type your message to chat with the AI agent
  - Type 'quit' or 'exit' to close the application
  - Type 'clear' to clear conversation history
  - Type 'history' to view conversation history

📚 Knowledge Base Commands:
  - 'upload <file_path>' - Upload document to knowledge base
  - 'search <query>' - Search knowledge base
  - 'kb_info' - Show knowledge base information
  - 'clear_kb' - Clear knowledge base

🎛️ System Commands:
  - 'status' - Show system status
  - 'help' - Show this help message
  - 'quit' or 'exit' - Exit application

💡 Example Usage:
  - "I have a problem with my account"
  - "How do I reset my password?"
  - "upload ./documents/faq.txt"
  - "search password reset"
        """
        print(help_text)
    
    def display_status(self):
        """Display system status"""
        if not self.agent:
            print("❌ System not initialized")
            return
        
        print("\n📊 System Status:")
        print("=" * 50)
        
        # Agent status
        agent_status = self.agent.get_agent_status()
        print(f"🤖 AI Agent:")
        print(f"   Model: {agent_status['model']}")
        print(f"   Temperature: {agent_status['temperature']}")
        print(f"   Max Tokens: {agent_status['max_tokens']}")
        print(f"   Memory Length: {agent_status['memory_length']}")
        print(f"   Tools Available: {agent_status['tools_available']}")
        
        # Knowledge base status
        kb_info = self.knowledge_base.get_collection_info()
        print(f"\n📚 Knowledge Base:")
        print(f"   Total Documents: {kb_info['total_documents']}")
        print(f"   Storage: {kb_info['persist_directory']}")
        
        print("=" * 50)
    
    def upload_document(self, file_path):
        """Upload document to knowledge base"""
        if not self.knowledge_base:
            print("❌ Knowledge base not initialized")
            return
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        print(f"📤 Uploading {file_path} to knowledge base...")
        success = self.knowledge_base.add_documents([file_path])
        
        if success:
            print("✅ Document uploaded successfully!")
        else:
            print("❌ Failed to upload document")
    
    def search_knowledge_base(self, query):
        """Search knowledge base"""
        if not self.knowledge_base:
            print("❌ Knowledge base not initialized")
            return
        
        print(f"🔍 Searching for: {query}")
        results = self.knowledge_base.search(query, k=2)  # Reduced from 3 to 2
        
        if results:
            print(f"\n📖 Found {len(results)} relevant results:")
            print("-" * 50)
            for i, result in enumerate(results, 1):
                print(f"{i}. {result[:200]}...")
                print("-" * 50)
        else:
            print("❌ No relevant results found")
    
    def clear_conversation(self):
        """Clear conversation history"""
        if not self.agent:
            print("❌ Agent not initialized")
            return
        
        self.agent.clear_memory()
        print("✅ Conversation history cleared")
    
    def show_history(self):
        """Show conversation history"""
        if not self.agent:
            print("❌ Agent not initialized")
            return
        
        messages = self.agent.get_conversation_history()
        
        if not messages:
            print("📝 No conversation history")
            return
        
        print("\n📝 Conversation History:")
        print("=" * 50)
        
        for i, message in enumerate(messages, 1):
            if hasattr(message, 'content'):
                role = "👤 You" if hasattr(message, 'type') and message.type == 'human' else "🤖 AI"
                print(f"{i}. {role}: {message.content}")
                print("-" * 50)
    
    def process_command(self, command):
        """Process user command"""
        command = command.strip().lower()
        
        if command in ['quit', 'exit']:
            print("👋 Goodbye! Have a great day!")
            self.running = False
            return
        
        elif command == 'help':
            self.display_help()
        
        elif command == 'status':
            self.display_status()
        
        elif command == 'clear':
            self.clear_conversation()
        
        elif command == 'history':
            self.show_history()
        
        elif command == 'kb_info':
            if self.knowledge_base:
                kb_info = self.knowledge_base.get_collection_info()
                print(f"📚 Knowledge Base: {kb_info['total_documents']} documents")
            else:
                print("❌ Knowledge base not initialized")
        
        elif command == 'clear_kb':
            if self.knowledge_base:
                if self.knowledge_base.clear_knowledge_base():
                    print("✅ Knowledge base cleared")
                else:
                    print("❌ Failed to clear knowledge base")
            else:
                print("❌ Knowledge base not initialized")
        
        elif command.startswith('upload '):
            file_path = command[7:].strip()
            self.upload_document(file_path)
        
        elif command.startswith('search '):
            query = command[7:].strip()
            self.search_knowledge_base(query)
        
        elif command:
            # Process as chat message
            if not self.agent:
                print("❌ AI agent not initialized")
                return
            
            print(f"\n🤖 AI Agent is thinking...")
            try:
                response = self.agent.process_message(command)
                print(f"\n🤖 AI Agent: {response}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def run(self):
        """Run the console interface"""
        print("🤖 Welcome to AI Customer Support Agent!")
        print("=" * 50)
        
        # Initialize system
        if not self.initialize_system():
            return
        
        self.running = True
        
        # Main loop
        while self.running:
            try:
                user_input = input("\n💬 You: ").strip()
                if user_input:
                    self.process_command(user_input)
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Have a great day!")
                break
            except EOFError:
                print("\n\n👋 Goodbye! Have a great day!")
                break

def main():
    """Main function"""
    console = ConsoleInterface()
    console.run()

if __name__ == "__main__":
    main()
