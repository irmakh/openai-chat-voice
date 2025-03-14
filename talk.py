# Standard library imports
import datetime
import re
import logging
import sys
from typing import Optional

# OpenAI client for API interactions
from openai import OpenAI
from openai.types.chat import ChatCompletion

# Custom helper modules
from config_loader import load_config
from helpers.tts_helper import run_tts, play_audio
from helpers.memory_helper import run_garbage_collection
from helpers.transcript_helper import save_transcript
from helpers.console_helper import get_user_input, exit_program
from helpers.chat_helper import generate
from helpers.chat_history_helper import manage_chat_history, get_formatted_history

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def initialize_client(config: dict) -> Optional[OpenAI]:
    """
    Initialize the OpenAI client with error handling.
    
    Args:
        config (dict): Configuration dictionary containing API settings
        
    Returns:
        Optional[OpenAI]: Initialized OpenAI client or None if initialization fails
    """
    try:
        client = OpenAI(
            base_url=config["base_url"],
            api_key=config["openai_api_key"]
        )
        return client
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {str(e)}")
        return None

def main() -> None:
    """
    Main function to execute the program loop.

    This function initializes the system, manages the chat interaction loop,
    and handles cleanup on exit.
    """
    try:
        # Load configuration settings
        logger.info("Loading configuration...")
        config = load_config()
        
        # Initialize OpenAI client
        client = initialize_client(config)
        if not client:
            logger.error("Failed to initialize. Exiting...")
            sys.exit(1)
        
        # Play welcome message if configured
        if config["speak_welcome"]:
            logger.info("Playing welcome message...")
            play_audio("hi.wav", config)
        
        # Initialize system
        logger.info("Running initial garbage collection...")
        run_garbage_collection()
        
        # Initialize chat history as a list
        chat_history_array = [{"role": "user", "content": config["initial_content"]}]
        memory = config["memory_message_count"] * 2
        
        logger.info("Starting main interaction loop...")
        while True:
            try:
                # Generate timestamp
                file_date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
                
                # Get user input
                user_prompt = get_user_input(config)
                logger.info(f"Received user input: {user_prompt}")

                # Check for exit command
                if user_prompt.lower() == "bye":
                    if config["speak_welcome"]:
                        play_audio("bye.wav", config)
                    logger.info("Exit command received. Shutting down...")
                    break
                
                # Get chat history and generate response
                logger.info(f"Chat history array: {chat_history_array}")
                chat_history = get_formatted_history(chat_history_array, memory, config["bot_name"])
                logger.info(f"Chat history: {chat_history}")
                answer: str = generate(user_prompt, chat_history, client, config)
                history_answer = answer
         
                # Process response
                if config["remove_deepseek_think_tags"]:
                    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL)
                
                # Update chat history
                chat_history_array = manage_chat_history(
                    user_prompt,
                    history_answer,
                    chat_history_array,
                    config["initial_content"],
                    config["bot_name"],
                    memory
                )
                
                # Handle text-to-speech and transcript
                run_tts(answer, file_date, config)
                save_transcript(user_prompt, answer, file_date, config)
                
                # Cleanup
                run_garbage_collection()
                
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                continue
        
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("Cleaning up and exiting...")
        exit_program(config)

if __name__ == "__main__":
    main()

