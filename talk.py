# Standard library imports
import datetime
import re
import logging
import sys
from typing import Optional

# OpenAI client for API interactions
from openai import OpenAI
# Custom helper modules
from config_loader import load_config
from helpers.tts_helper import run_tts, play_audio
from helpers.memory_helper import run_garbage_collection
from helpers.transcript_helper import save_transcript
from helpers.console_helper import get_user_input, exit_program
from helpers.chat_helper import generate
from helpers.chat_history_helper import manage_chat_history, get_formatted_history


# Configure logging with both file and console output
# This ensures we can track application behavior both in real-time and for later analysis
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
                      Must include 'base_url' and 'openai_api_key'

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

    This function handles:
    - System initialization
    - Chat interaction loop
    - Memory management
    - Text-to-speech processing
    - Transcript saving
    - Cleanup on exit
    """
    # Load configuration settings from external file
    logger.info("Loading configuration...")
    config = load_config()

    try:
        # Initialize OpenAI client with error checking
        client = initialize_client(config)
        if not client:
            logger.error("Failed to initialize. Exiting...")
            sys.exit(1)

        # Play welcome audio if enabled in configuration
        if config["speak_welcome"]:
            logger.info("Playing welcome message...")
            play_audio("hi.wav", config)

        # Initial memory cleanup to ensure optimal performance
        logger.info("Running initial garbage collection...")
        run_garbage_collection()

        # Initialize chat history with system prompt
        # This sets up the initial context for the conversation
        chat_history_array = [{"role": "user", "content": config["initial_content"]}]
        memory = config["memory_message_count"] * 2  # Calculate memory window size

        logger.info("Starting main interaction loop...")
        while True:
            try:
                # Generate unique timestamp for file naming
                file_date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

                # Get user input with configured prompt
                user_prompt = get_user_input(config)
                logger.info(f"Received user input: {user_prompt}")

                # Check for exit command and handle graceful shutdown
                if user_prompt.lower() == "bye":
                    if config["speak_welcome"]:
                        play_audio("bye.wav", config)
                    logger.info("Exit command received. Shutting down...")
                    break

                # Process chat history and generate AI response
                # This section manages the conversation context and memory
                logger.info(f"Chat history array: {chat_history_array}")
                chat_history = get_formatted_history(chat_history_array, memory, config["bot_name"])
                logger.info(f"Chat history: {chat_history}")
                answer: str = generate(user_prompt, chat_history, client, config)
                history_answer = answer

                # Remove thinking process tags if configured
                # These tags might contain internal AI reasoning that we don't want to show
                if config["remove_deepseek_think_tags"]:
                    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL)

                # Update conversation history while maintaining memory limits
                # This ensures the context window doesn't grow too large
                chat_history_array = manage_chat_history(
                    user_prompt,
                    history_answer,
                    chat_history_array,
                    config["initial_content"],
                    config["bot_name"],
                    memory
                )

                # Process response for output
                # - Convert text to speech
                # - Save conversation transcript
                run_tts(answer, file_date, config)
                save_transcript(user_prompt, answer, file_date, config)

                # Regular memory cleanup to prevent memory leaks
                run_garbage_collection()

            except Exception as e:
                # Handle errors in the main loop without crashing
                logger.error(f"Error in main loop: {str(e)}")
                continue

    except Exception as e:
        # Handle critical errors that require program termination
        logger.error(f"Critical error: {str(e)}")
        sys.exit(1)
    finally:
        # Ensure proper cleanup regardless of how the program exits
        logger.info("Cleaning up and exiting...")
        exit_program(config)

if __name__ == "__main__":
    main()