from helpers.memory_helper import run_garbage_collection
import logging

# Set up logging configuration
logger = logging.getLogger(__name__)

def generate(user_prompt: str, chat_history: str, client, config) -> str:
    """
    Generate a response using the OpenAI API.

    Args:
        user_prompt (str): The user's input message
        chat_history (str): Previous conversation history
        client: OpenAI client instance
        config: Configuration dictionary

    Returns:
        str: Generated response
    """
    try:
        messages = [
            {"role": "system", "content": chat_history},
            {"role": "user", "content": user_prompt}
        ]
        
        response = client.chat.completions.create(
            model=config["chat_model_name"],
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return "I apologize, but I encountered an error while processing your request."
