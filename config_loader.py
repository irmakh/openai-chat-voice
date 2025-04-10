import configparser  # Import the configparser module to read configuration files
import os  # Import the os module to access environment variables

def load_config() -> dict:
    """
    Load configuration settings from a file and return them as a dictionary.

    This function reads a configuration file named 'config.ini' using ConfigParser
    and returns a dictionary with configuration settings based on the 'DEFAULT' 
    section of the file. It provides fallback values for each configuration variable 
    if they are not present in the file. The configuration includes settings for the 
    chat model name, API key, base URL, sound directory, and various flags controlling 
    file generation and output behavior.

    Returns:
        dict: A dictionary containing configuration settings.
    """
    config = configparser.ConfigParser()  # Create a ConfigParser instance
    config.read('config.ini')  # Read the configuration file
    
    return {
        "chat_model_name": config.get('DEFAULT', 'chat_model_name', fallback="llama-3.1-8b-lexi-uncensored-v2"),  # Get chat model name with a fallback
        "base_url": config.get('DEFAULT', 'base_url', fallback="http://localhost:1234/v1/"),  # Get base URL with a fallback
        "openai_api_key": config.get('DEFAULT', 'openai_api_key', fallback=os.environ.get("OPENAI_API_KEY") or 'your-api-key'),  # Get API key, fallback to environment variable
        "sound_directory": config.get('DEFAULT', 'sound_directory', fallback="sound-streams/"),  # Get sound directory with a fallback
        "transcript_directory": config.get('DEFAULT', 'transcript_directory', fallback="transcript-streams/"),  # Get transcript directory with a fallback
        "keep_generated_file": config.getboolean('DEFAULT', 'keep_generated_file', fallback=True),  # Get flag for keeping generated files
        "generate_transcript": config.getboolean('DEFAULT', 'generate_transcript', fallback=True),  # Get flag for generating transcripts
        "initial_content": config.get('DEFAULT', 'initial_content', fallback="You are a historian answering questions. You will state users question first than answer."),  # Get initial content with a fallback
        "read_after_generate": config.getboolean('DEFAULT', 'read_after_generate', fallback=True),  # Get flag for reading after generation
        "print_generated_text": config.getboolean('DEFAULT', 'print_generated_text', fallback=True),  # Get flag for printing generated text
        "memory_message_count": config.getint('DEFAULT', 'memory_message_count', fallback=10),  # Get count of messages to keep in memory
        "bot_name": config.get('DEFAULT', 'bot_name', fallback="Bot"),  # Get bot name with a fallback
        "remove_deepseek_think_tags": config.getboolean('DEFAULT', 'remove_deepseek_think_tags', fallback=True),  # Get flag for removing specific tags
        "speak_welcome": config.getboolean('DEFAULT', 'speak_welcome', fallback=True),  # Get flag for speaking welcome message
        "use_gpu": config.getboolean('DEFAULT', 'use_gpu', fallback=True),  # Get flag for using GPU processing,
        "bot_sound": config.get('DEFAULT', 'bot_sound', fallback="tts_models/en/vctk/vits") 
    }
