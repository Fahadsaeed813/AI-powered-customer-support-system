from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Any
import logging
from utils.knowledge_base import KnowledgeBaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomerSupportAgent:
    def __init__(self, knowledge_base: KnowledgeBaseManager, config: Dict[str, Any]):
        self.knowledge_base = knowledge_base
        self.config = config
        self.llm = ChatGoogleGenerativeAI(
            model=config.get("GEMINI_MODEL", "gemini-1.5-flash"),
            temperature=config.get("TEMPERATURE", 0.7),
            max_output_tokens=config.get("MAX_TOKENS", 500),
            google_api_key=config.get("GOOGLE_API_KEY")
        )
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create tools
        self.tools = self._create_tools()
        
        # Create prompt template
        self.prompt = self._create_prompt()
        
        # Create agent
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def _create_tools(self) -> List:
        """Create tools for the agent"""
        
        @tool
        def search_knowledge_base(query: str) -> str:
            """Search knowledge base for customer support information"""
            try:
                results = self.knowledge_base.search(query, k=2)  # Reduced from 3 to 2
                if results:
                    return f"Found relevant information:\n" + "\n\n".join(results)
                else:
                    return "No relevant information found in the knowledge base."
            except Exception as e:
                logger.error(f"Error searching knowledge base: {str(e)}")
                return f"Error searching knowledge base: {str(e)}"
        
        @tool
        def get_customer_info(customer_id: str) -> str:
            """Get customer info from CRM system"""
            # This is a placeholder - you would integrate with your actual CRM system
            return f"Customer ID {customer_id}: Basic customer information retrieved. For detailed info, please check the CRM system."
        
        @tool
        def create_support_ticket(issue: str, priority: str = "medium") -> str:
            """Create support ticket for customer issue"""
            # This is a placeholder - you would integrate with your actual ticketing system
            ticket_id = f"TKT-{hash(issue) % 10000:04d}"
            return f"Support ticket created: {ticket_id}\nIssue: {issue}\nPriority: {priority}\nStatus: Open"
        
        @tool
        def escalate_issue(issue: str, reason: str) -> str:
            """Escalate customer issue to higher priority"""
            return f"Issue escalated successfully.\nIssue: {issue}\nReason: {reason}\nEscalation timestamp: {self._get_current_timestamp()}"
        
        @tool
        def provide_solution_steps(problem: str) -> str:
            """Provide solution steps for customer problems"""
            # This would typically query your knowledge base for solution steps
            return f"Here are the steps to resolve: {problem}\n1. First, try the basic troubleshooting\n2. If that doesn't work, check the advanced options\n3. Contact support if the issue persists"
        
        return [
            search_knowledge_base,
            get_customer_info,
            create_support_ticket,
            escalate_issue,
            provide_solution_steps
        ]
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Create the prompt template for the agent"""
        
        system_message = """You are an AI Customer Support Agent. Help customers efficiently by:
1. Understanding their issues
2. Searching knowledge base for solutions
3. Providing clear, helpful responses
4. Creating tickets when needed
5. Escalating complex issues

Be professional and concise. Use available tools to search knowledge base, create tickets, and escalate issues."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        return prompt
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp for logging"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def process_message(self, user_message: str) -> str:
        """Process a user message and return a response"""
        try:
            # Add user message to memory
            self.memory.chat_memory.add_user_message(user_message)
            
            # Execute agent
            response = self.agent_executor.invoke({
                "input": user_message
            })
            
            # Add AI response to memory
            ai_response = response.get("output", "I apologize, but I couldn't process your request.")
            self.memory.chat_memory.add_ai_message(ai_response)
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            error_response = f"I apologize, but I encountered an error while processing your request. Please try again or contact human support if the issue persists. Error: {str(e)}"
            
            # Add error response to memory
            self.memory.chat_memory.add_ai_message(error_response)
            
            return error_response
    
    def get_conversation_history(self) -> List[BaseMessage]:
        """Get the conversation history"""
        return self.memory.chat_memory.messages
    
    def clear_memory(self) -> None:
        """Clear the conversation memory"""
        self.memory.clear()
        logger.info("Conversation memory cleared")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get the current status of the agent"""
        return {
            "model": self.config.get("GEMINI_MODEL", "gemini-1.5-flash"),
            "temperature": self.config.get("TEMPERATURE", 0.7),
            "max_tokens": self.config.get("MAX_TOKENS", 500),
            "memory_length": len(self.memory.chat_memory.messages),
            "tools_available": len(self.tools)
        }
