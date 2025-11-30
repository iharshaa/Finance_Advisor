"""
utils.py - Utility Functions
==============================

Helper functions for text summarization and conversation logging.

Functions:
- summarize_short(): Create short summaries of agent responses
- save_conversation(): Save complete conversation to JSON file
- load_conversation(): Load conversation from JSON file
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


def summarize_short(text: str, max_length: int = 200) -> str:
    """
    Create a short summary of text by truncating.
    
    This is a simple truncation-based summarizer.
    For production, consider using:
    - LLM-based summarization
    - extractive summarization (sumy, gensim)
    - TextRank algorithm
    
    Args:
        text: Text to summarize
        max_length: Maximum characters in summary
    
    Returns:
        Truncated text with ellipsis if needed
    
    Example:
        >>> long_text = "This is a very long text..." * 100
        >>> summary = summarize_short(long_text, 50)
        >>> len(summary) <= 53  # 50 + "..."
        True
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = " ".join(text.split())
    
    if len(text) <= max_length:
        return text
    
    # Truncate and add ellipsis
    return text[:max_length].rsplit(' ', 1)[0] + "..."


def save_conversation(
    user_data: Dict[str, Any],
    sip_calc: Dict[str, float],
    advisor_output: str,
    risk_output: str,
    planner_output: str,
    output_dir: str = "logs"
) -> str:
    """
    Save complete conversation to JSON file with timestamp.
    
    Creates a structured JSON file containing:
    - User input data
    - SIP calculations
    - All agent outputs
    - Timestamp
    
    Args:
        user_data: Dictionary with user inputs (income, target, years, etc.)
        sip_calc: Dictionary with SIP calculation results
        advisor_output: Advisor agent's response
        risk_output: Risk analyst agent's response
        planner_output: Planner agent's response
        output_dir: Directory to save logs (default: "logs")
    
    Returns:
        Path to the saved JSON file
    
    Example:
        >>> filename = save_conversation(
        ...     user_data={'income': 50000, 'target': 1000000},
        ...     sip_calc={'monthly_sip': 12244.45},
        ...     advisor_output="...",
        ...     risk_output="...",
        ...     planner_output="..."
        ... )
        >>> print(filename)
        logs/finance_plan_20251130_103000.json
    """
    # Create conversation data structure
    conversation_data = {
        "timestamp": datetime.now().isoformat(),
        "date_readable": datetime.now().strftime("%d %B %Y, %I:%M %p"),
        "user_input": user_data,
        "calculations": sip_calc,
        "agent_outputs": {
            "advisor": {
                "role": "सलाहकार (Advisor)",
                "output": advisor_output,
                "summary": summarize_short(advisor_output, 100)
            },
            "risk_analyst": {
                "role": "जोखिम विश्लेषक (Risk Analyst)",
                "output": risk_output,
                "summary": summarize_short(risk_output, 100)
            },
            "planner": {
                "role": "योजनाकर्त्ता (Planner)",
                "output": planner_output,
                "summary": summarize_short(planner_output, 100)
            }
        },
        "metadata": {
            "version": "1.0",
            "system": "Multi-Agent Hindi Finance Advisor"
        }
    }
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"finance_plan_{timestamp_str}.json")
    
    # Save to JSON file with UTF-8 encoding (important for Hindi text)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(conversation_data, f, ensure_ascii=False, indent=2)
    
    return filename


def load_conversation(filename: str) -> Dict[str, Any]:
    """
    Load a conversation from a JSON file.
    
    Args:
        filename: Path to the JSON file
    
    Returns:
        Dictionary containing conversation data
    
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    
    Example:
        >>> data = load_conversation("logs/finance_plan_20251130_103000.json")
        >>> print(data['user_input']['monthly_income'])
        50000
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_conversations(output_dir: str = "logs") -> List[Dict[str, str]]:
    """
    List all saved conversations with metadata.
    
    Args:
        output_dir: Directory containing conversation logs
    
    Returns:
        List of dictionaries with filename, timestamp, and size
    
    Example:
        >>> conversations = list_conversations()
        >>> for conv in conversations:
        ...     print(f"{conv['filename']}: {conv['timestamp']}")
    """
    if not os.path.exists(output_dir):
        return []
    
    conversations = []
    
    for filename in os.listdir(output_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(output_dir, filename)
            
            # Get file stats
            stat = os.stat(filepath)
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            
            conversations.append({
                'filename': filename,
                'filepath': filepath,
                'timestamp': modified_time.isoformat(),
                'timestamp_readable': modified_time.strftime("%d %B %Y, %I:%M %p"),
                'size_bytes': stat.st_size,
                'size_kb': round(stat.st_size / 1024, 2)
            })
    
    # Sort by timestamp (newest first)
    conversations.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return conversations


def format_conversation_summary(conversation_data: Dict[str, Any]) -> str:
    """
    Format a conversation into a readable summary.
    
    Args:
        conversation_data: Conversation data dictionary
    
    Returns:
        Formatted string summary
    
    Example:
        >>> data = load_conversation("logs/finance_plan_20251130_103000.json")
        >>> summary = format_conversation_summary(data)
        >>> print(summary)
    """
    user_data = conversation_data.get('user_input', {})
    calc = conversation_data.get('calculations', {})
    timestamp = conversation_data.get('date_readable', 'Unknown date')
    
    summary = f"""
📅 Date: {timestamp}

💰 Financial Goal:
- Monthly Income: ₹{user_data.get('monthly_income', 0):,}
- Target Amount: ₹{user_data.get('target_amount', 0):,}
- Time Horizon: {user_data.get('years', 0)} years
- Risk Profile: {user_data.get('risk_profile', 'Unknown')}

📊 Calculations:
- Required Monthly SIP: ₹{calc.get('monthly_sip', 0):,}
- Total Investment: ₹{calc.get('total_investment', 0):,}
- Expected Returns: ₹{calc.get('expected_returns', 0):,}

🤖 Agent Summaries:
"""
    
    agents = conversation_data.get('agent_outputs', {})
    for key, value in agents.items():
        role = value.get('role', key)
        summary_text = value.get('summary', 'No summary')
        summary += f"\n{role}:\n{summary_text}\n"
    
    return summary


if __name__ == "__main__":
    # Test utility functions
    print("Testing utility functions...\n")
    
    # Test summarization
    long_text = "यह एक बहुत लंबा पाठ है जो कई वाक्यों से बना है। " * 20
    short_summary = summarize_short(long_text, 100)
    print(f"Original length: {len(long_text)}")
    print(f"Summary length: {len(short_summary)}")
    print(f"Summary: {short_summary}\n")
    
    # Test save and load
    test_user_data = {
        "monthly_income": 50000,
        "target_amount": 1000000,
        "years": 5,
        "risk_profile": "मध्यम जोखिम"
    }
    
    test_sip_calc = {
        "monthly_sip": 12244.45,
        "total_investment": 734667.0,
        "expected_returns": 265333.0
    }
    
    test_filename = save_conversation(
        test_user_data,
        test_sip_calc,
        "सलाहकार की राय...",
        "जोखिम विश्लेषण...",
        "अंतिम योजना...",
        output_dir="test_logs"
    )
    
    print(f"✅ Saved to: {test_filename}")
    
    # Load it back
    loaded_data = load_conversation(test_filename)
    print(f"✅ Loaded: {loaded_data['metadata']['system']}")
    
    # List conversations
    convs = list_conversations("test_logs")
    print(f"\n✅ Found {len(convs)} conversation(s)")
    
    # Clean up test files
    import shutil
    if os.path.exists("test_logs"):
        shutil.rmtree("test_logs")
        print("✅ Cleaned up test files")
