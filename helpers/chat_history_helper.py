def manage_chat_history(user_prompt: str, bot_response: str, chat_history_array: list, initial_content: str, bot_name: str, memory_limit: int) -> list:
    """
    Manages the chat history by updating it with new messages and maintaining its size.
    
    Args:
        user_prompt (str): The user's input message
        bot_response (str): The bot's response message
        chat_history_array (list): Current chat history array
        initial_content (str): Initial system content/prompt
        bot_name (str): Name of the bot
        memory_limit (int): Maximum number of messages to keep in memory
        
    Returns:
        list: Updated chat history array
    """
    # Update chat history with user input and bot response
    chat_history_array.append(f"User: {user_prompt}")
    chat_history_array.append(f"{bot_name}: {bot_response}")
    
    # Maintain chat history size within memory limit
    if len(chat_history_array) > memory_limit:
        del chat_history_array[:-memory_limit]
    
    # Reset chat history with initial content
    del chat_history_array[0]
    chat_history_array = [initial_content] + chat_history_array
    
    return chat_history_array

def get_formatted_history(chat_history_array: list, memory_limit: int, bot_name: str) -> str:
    """
    Formats the chat history for use in generating responses.
    
    Args:
        chat_history_array (list): Current chat history array
        memory_limit (int): Maximum number of messages to include
        bot_name (str): Name of the bot to replace in the history
        
    Returns:
        str: Formatted chat history string
    """
    # Join recent messages and replace bot name placeholder
    chat_history = '\n'.join(chat_history_array[-memory_limit:])
    chat_history = chat_history.replace("{botName}", bot_name)
    
    return chat_history 