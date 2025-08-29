# 🤖 AI Customer Support Agent

End-to-end AI-powered customer support system built with LangChain, Google Gemini, and Chroma vector database.

## ✨ Features

- **🤖 AI Agent**: Powered by Google Gemini 1.5 Flash with LangChain orchestration
- **📚 Knowledge Base**: Vector database using Chroma for document storage and retrieval
- **🛠️ Smart Tools**: Built-in tools for ticket creation, issue escalation, and customer info retrieval
- **💬 Dual Interface**: Both Streamlit web UI and console interface
- **📄 Multi-format Support**: Handles TXT, PDF, MD, and CSV documents
- **🧠 Memory Management**: Maintains conversation context and history
- **🔍 Semantic Search**: Advanced document search using embeddings

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │  Console App    │    │   AI Agent      │
│   (Web UI)      │    │  (CLI)          │    │   (LangChain)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Knowledge Base │
                    │   (Chroma DB)   │
                    └─────────────────┘
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Google Gemini API key
- Git

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd customer_support_ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the environment template:
```bash
copy env_example.txt .env
```

2. Edit `.env` file with your Google Gemini API key:
```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
MAX_TOKENS=4000
TEMPERATURE=0.7
```

### 4. Run the Application

#### Option A: Streamlit Web UI (Recommended)
```bash
streamlit run ui/streamlit_app.py
```

#### Option B: Console Interface
```bash
python console_app.py
```

## 📖 Usage

### Web UI (Streamlit)

1. **Start the application**: `streamlit run ui/streamlit_app.py`
2. **Upload documents**: Use the sidebar to upload TXT, PDF, MD, or CSV files
3. **Chat with AI**: Type your customer support questions in the chat interface
4. **Monitor system**: Check system status and knowledge base info in the sidebar

### Console Interface

1. **Start the application**: `python console_app.py`
2. **Available commands**:
   - `help` - Show available commands
   - `status` - Display system status
   - `upload <file_path>` - Upload document to knowledge base
   - `search <query>` - Search knowledge base
   - `clear` - Clear conversation history
   - `quit` or `exit` - Exit application

### Example Conversations

```
💬 You: I can't log into my account
🤖 AI Agent: I understand you're having trouble logging into your account. Let me search our knowledge base for solutions...

💬 You: How do I reset my password?
🤖 AI Agent: I found information about password reset. Here are the steps...

💬 You: I need to create a support ticket
🤖 AI Agent: I'll help you create a support ticket. Let me gather the necessary information...
```

## 🛠️ Customization

### Adding New Tools

Edit `models/ai_agent.py` to add new tools:

```python
@tool
def your_new_tool(parameter: str) -> str:
    """Description of what this tool does"""
    # Your tool implementation
    return "Tool result"
```

### Modifying the Knowledge Base

Edit `utils/knowledge_base.py` to:
- Change chunk size and overlap
- Add new document loaders
- Modify embedding settings

### Updating the UI

Edit `ui/streamlit_app.py` to:
- Change styling and layout
- Add new UI components
- Modify the chat interface


## 🔧 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Required |
| `GEMINI_MODEL` | Gemini model to use | `gemini-1.5-flash` |
| `CHROMA_PERSIST_DIRECTORY` | Chroma DB storage path | `./data/chroma_db` |
| `MAX_TOKENS` | Maximum tokens per response | `4000` |
| `TEMPERATURE` | AI response creativity | `0.7` |

## 🚨 Troubleshooting

### Common Issues

1. **Google Gemini API Key Error**
   - Ensure your API key is correct in `.env` file
   - Check if you have sufficient credits

2. **Chroma DB Errors**
   - Delete `./data/chroma_db` folder and restart
   - Ensure write permissions in the data directory

3. **Import Errors**
   - Ensure virtual environment is activated
   - Check if all dependencies are installed: `pip install -r requirements.txt`

4. **Streamlit Issues**
   - Clear Streamlit cache: `streamlit cache clear`
   - Check if port 8501 is available

### Performance Tips

- Use smaller document chunks for faster processing
- Limit the number of documents in knowledge base for development
- Adjust `MAX_TOKENS` based on your needs

## 🔮 Future Enhancements

- [ ] Integration with CRM systems (Salesforce, HubSpot)
- [ ] Multi-language support
- [ ] Voice interface
- [ ] Advanced analytics and reporting
- [ ] Slack/Discord integration
- [ ] Customer sentiment analysis
- [ ] Automated ticket routing
- [ ] Knowledge base versioning

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the AI orchestration framework
- [Google Gemini](https://ai.google.dev/) for the AI models
- [Chroma](https://www.trychroma.com/) for the vector database
- [Streamlit](https://streamlit.io/) for the web interface framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the console logs for error messages
3. Create an issue in the repository
4. Contact me

Fahad Saeed Full Stack AI Engineer 
"https://fahadsaeed.netlify.app/"

---

