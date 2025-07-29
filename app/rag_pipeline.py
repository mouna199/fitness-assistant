from app.prompt_builder import build_prompt
from app.llm import llm
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rag(query, search_fn):
    """
    RAG (Retrieval-Augmented Generation) pipeline for fitness assistant.
    
    Args:
        query (str): User's fitness-related question
        search_fn (callable): Function to search for relevant documents
        
    Returns:
        str: Generated response from the LLM
        
    Raises:
        ValueError: If query is empty or None
        Exception: If search or LLM generation fails
    """
    # Input validation
    if not query or not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a non-empty string")
    
    if not callable(search_fn):
        raise ValueError("search_fn must be a callable function")
    
    try:
        # Retrieve relevant documents
        logger.info(f"Searching for documents related to: {query}")
        results = search_fn(query)
        
        # Validate search results
        if not results:
            logger.warning("No relevant documents found for the query")
            return "I don't know. No relevant information was found for your question."
        
        if not isinstance(results, list):
            raise ValueError("Search function must return a list of documents")
        
        # Log the number of retrieved documents
        logger.info(f"Retrieved {len(results)} relevant documents")
        
        # Build prompt with retrieved context
        prompt = build_prompt(results, query)
        
        # Generate response using LLM
        logger.info("Generating response using LLM")
        response = llm(prompt)
        
        if not response or not response.strip():
            logger.warning("LLM returned empty response")
            return "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
        
        logger.info("Successfully generated response")
        return response.strip()
        
    except Exception as e:
        logger.error(f"Error in RAG pipeline: {str(e)}")
        raise Exception(f"RAG pipeline failed: {str(e)}")
