import streamlit as st
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from config import Config
from utils.knowledge_base import KnowledgeBaseManager
from models.ai_agent import CustomerSupportAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=Config.STREAMLIT_TITLE,
    page_icon=Config.STREAMLIT_PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        color: #333333;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #333333;
    }
    .ai-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
        color: #333333;
    }
    .chat-message strong {
        color: #1a1a1a;
        font-weight: 600;
    }
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    .status-online { background-color: #4caf50; }
    .status-offline { background-color: #f44336; }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'agent_initialized' not in st.session_state:
        st.session_state.agent_initialized = False
    if 'knowledge_base_initialized' not in st.session_state:
        st.session_state.knowledge_base_initialized = False

def initialize_system():
    """Initialize the AI agent and knowledge base"""
    try:
        # Validate configuration
        Config.validate()
        
        # Initialize knowledge base
        if not st.session_state.knowledge_base_initialized:
            with st.spinner("Initializing knowledge base..."):
                knowledge_base = KnowledgeBaseManager(Config.CHROMA_PERSIST_DIRECTORY)
                st.session_state.knowledge_base = knowledge_base
                st.session_state.knowledge_base_initialized = True
                st.success("Knowledge base initialized successfully!")
        
        # Initialize AI agent
        if not st.session_state.agent_initialized:
            with st.spinner("Initializing AI agent..."):
                config_dict = {
                    "GOOGLE_API_KEY": Config.GOOGLE_API_KEY,
                    "GEMINI_MODEL": Config.GEMINI_MODEL,
                    "TEMPERATURE": Config.TEMPERATURE,
                    "MAX_TOKENS": Config.MAX_TOKENS
                }
                agent = CustomerSupportAgent(st.session_state.knowledge_base, config_dict)
                st.session_state.agent = agent
                st.session_state.agent_initialized = True
                st.success("AI agent initialized successfully!")
        
        return True
        
    except Exception as e:
        st.error(f"Error initializing system: {str(e)}")
        return False

def display_sidebar():
    """Display sidebar with system information and controls"""
    with st.sidebar:
        st.markdown("## 🤖 System Status")
        
        # System status
        if st.session_state.agent_initialized:
            st.markdown('<span class="status-indicator status-online"></span>AI Agent: Online', unsafe_allow_html=True)
            
            # Agent status info
            agent_status = st.session_state.agent.get_agent_status()
            st.markdown("### Agent Info")
            st.write(f"**Model:** {agent_status['model']}")
            st.write(f"**Temperature:** {agent_status['temperature']}")
            st.write(f"**Max Tokens:** {agent_status['max_tokens']}")
            st.write(f"**Memory Length:** {agent_status['memory_length']}")
            st.write(f"**Tools Available:** {agent_status['tools_available']}")
        else:
            st.markdown('<span class="status-indicator status-offline"></span>AI Agent: Offline', unsafe_allow_html=True)
        
        if st.session_state.knowledge_base_initialized:
            st.markdown('<span class="status-indicator status-online"></span>Knowledge Base: Online', unsafe_allow_html=True)
            
            # Knowledge base info
            kb_info = st.session_state.knowledge_base.get_collection_info()
            st.markdown("### Knowledge Base Info")
            st.write(f"**Total Documents:** {kb_info['total_documents']}")
            st.write(f"**Storage:** {kb_info['persist_directory']}")
        else:
            st.markdown('<span class="status-indicator status-offline"></span>Knowledge Base: Offline', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Knowledge base management
        st.markdown("## 📚 Knowledge Base")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload documents to knowledge base",
            type=['txt', 'pdf', 'md', 'csv'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("Add to Knowledge Base"):
                with st.spinner("Processing documents..."):
                    # Save uploaded files temporarily
                    temp_paths = []
                    for uploaded_file in uploaded_files:
                        temp_path = os.path.join(Config.KNOWLEDGE_BASE_DIR, uploaded_file.name)
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        temp_paths.append(temp_path)
                    
                    # Add to knowledge base
                    success = st.session_state.knowledge_base.add_documents(temp_paths)
                    if success:
                        st.success("Documents added to knowledge base successfully!")
                        # Clean up temp files
                        for temp_path in temp_paths:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                    else:
                        st.error("Failed to add documents to knowledge base")
        
        # Knowledge base controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear Knowledge Base"):
                if st.session_state.knowledge_base_initialized:
                    if st.session_state.knowledge_base.clear_knowledge_base():
                        st.success("Knowledge base cleared!")
                    else:
                        st.error("Failed to clear knowledge base")
        
        with col2:
            if st.button("Refresh Status"):
                st.rerun()
        
        st.markdown("---")
        
        # Agent controls
        st.markdown("## 🎛️ Agent Controls")
        
        if st.button("Clear Conversation"):
            if st.session_state.agent_initialized:
                st.session_state.agent.clear_memory()
                st.session_state.messages = []
                st.success("Conversation cleared!")
                st.rerun()

def display_chat_interface():
    """Display the main chat interface"""
    st.markdown('<h1 class="main-header">🤖 AI Customer Support Agent</h1>', unsafe_allow_html=True)
    
    # Chat messages display
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message ai-message">
                    <strong>🤖 AI Agent:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    # Initialize chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with chat_container:
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong> {prompt}
            </div>
            """, unsafe_allow_html=True)
        
        # Get AI response
        with st.spinner("AI Agent is thinking..."):
            try:
                response = st.session_state.agent.process_message(prompt)
                
                # Add AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Display AI response
                with chat_container:
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <strong>🤖 AI Agent:</strong> {response}
                    </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                error_msg = f"I apologize, but I encountered an error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
                with chat_container:
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <strong>🤖 AI Agent:</strong> {error_msg}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Rerun to update the display
        st.rerun()

def main():
    """Main application function"""
    st.title("AI Customer Support Agent")
    
    # Initialize session state
    initialize_session_state()
    
    # Check if system is initialized
    if not st.session_state.agent_initialized or not st.session_state.knowledge_base_initialized:
        st.warning("Please wait while the system initializes...")
        if initialize_system():
            st.success("System initialized successfully!")
            st.rerun()
        else:
            st.error("Failed to initialize system. Please check your configuration.")
            return
    
    # Display sidebar
    display_sidebar()
    
    # Display main chat interface
    display_chat_interface()

if __name__ == "__main__":
    main()
