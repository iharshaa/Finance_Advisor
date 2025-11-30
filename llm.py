"""
llm.py - LangChain LLM Factory
================================

LangChain-based Qwen 2.5-7B initialization for Hindi financial advice.
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def get_llm(
    repo_id: str = "Qwen/Qwen2.5-7B-Instruct",
    temperature: float = 0.7,
    max_tokens: int = 512,
    api_token: Optional[str] = None
):
    """
    Initialize LangChain HuggingFace LLM (Qwen 2.5-7B).
    
    Args:
        repo_id: HuggingFace model ID
        temperature: Sampling temperature (0.0-1.0)
        max_tokens: Maximum tokens in response
        api_token: HuggingFace API token (reads from .env if None)
    
    Returns:
        LangChain ChatHuggingFace instance
    
    Example:
        >>> from langchain_core.messages import HumanMessage
        >>> llm = get_llm()
        >>> response = llm.invoke([HumanMessage(content="मुझे निवेश की सलाह दें")])
    """
    if api_token is None:
        api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    
    if not api_token:
        raise ValueError(
            "HuggingFace API token not found. "
            "Set HUGGINGFACEHUB_API_TOKEN in .env file.\n"
            "Get token: https://huggingface.co/settings/tokens"
        )
    
    try:
        from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
        
        # Create HuggingFace endpoint with LangChain
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            temperature=temperature,
            max_new_tokens=max_tokens,
            huggingfacehub_api_token=api_token,
        )
        
        # Wrap with ChatHuggingFace for better chat compatibility
        chat_llm = ChatHuggingFace(llm=llm)
        return chat_llm
        
    except Exception as e:
        raise Exception(f"Failed to initialize LangChain LLM {repo_id}: {str(e)}")