import logging

# Set up logging configuration
logger = logging.getLogger(__name__)

def manage_chat_history(user_prompt: str, answer: str, chat_history: list, initial_content: str, bot_name: str, memory: int) -> list:
    """
    Update the chat history with the latest user prompt and assistant answer.

    Args:
        user_prompt (str): The latest user input.
        answer (str): The assistant's response.
        chat_history (list): Current list of chat history messages.
        initial_content (str): Initial content of the chat.
        bot_name (str): Name of the bot.
        memory (int): Number of messages to keep in history.

    Returns:
        list: Updated chat history.
    """
    # Append the latest messages
    chat_history.append({"role": "user", "content": user_prompt})
    chat_history.append({"role": "assistant", "content": answer})
    logger.info(f"Chat history: {chat_history}")
    # Truncate history to maintain memory limit
    if len(chat_history) > memory:
        chat_history = chat_history[-memory:]
    

    return chat_history

def get_formatted_history(chat_history: list, memory: int, bot_name: str) -> str:
    """
    Format the chat history for the model input.

    Args:
        chat_history (list): List of chat messages.
        memory (int): Number of messages to include.
        bot_name (str): Name of the bot.

    Returns:
        str: Formatted chat history.
    """
    # Slice the chat history to include only the last 'memory' messages
    recent_history = chat_history[-memory:]

    # Format the history as a single string
    formatted_history = ""
    for message in recent_history:
        role = "User" if message["role"] == "user" else bot_name
        formatted_history += f"{role}: {message['content']}\n"
    
    return formatted_history