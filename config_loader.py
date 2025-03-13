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
        "OPENAI_API_KEY": config.get('DEFAULT', 'OPENAI_API_KEY', fallback=os.environ.get("OPENAI_API_KEY") or 'your-api-key'),  # Get API key, fallback to environment variable
        "sound_directory": config.get('DEFAULT', 'sound_directory', fallback="sound-streams/"),  # Get sound directory with a fallback
        "transcript_directory": config.get('DEFAULT', 'transcript_directory', fallback="transcript-streams/"),  # Get transcript directory with a fallback
        "keepGeneratedFile": config.getboolean('DEFAULT', 'keepGeneratedFile', fallback=True),  # Get flag for keeping generated files
        "generateTranscript": config.getboolean('DEFAULT', 'generateTranscript', fallback=True),  # Get flag for generating transcripts
        "initialContent": config.get('DEFAULT', 'initialContent', fallback="You are a historian answering questions. You will state users question first than answer."),  # Get initial content with a fallback
        "readAftergenerate": config.getboolean('DEFAULT', 'readAfterGenerate', fallback=True),  # Get flag for reading after generation
        "printGeneratedText": config.getboolean('DEFAULT', 'printGeneratedText', fallback=True),  # Get flag for printing generated text
        "memoryMessageCount": config.getint('DEFAULT', 'memoryMessageCount', fallback=10),  # Get count of messages to keep in memory
        "botName": config.get('DEFAULT', 'botName', fallback="Bot"),  # Get bot name with a fallback
        "removeDeepseekThinkTags": config.getboolean('DEFAULT', 'removeDeepseekThinkTags', fallback=True),  # Get flag for removing specific tags
        "speakWelcome": config.getboolean('DEFAULT', 'speakWelcome', fallback=True),  # Get flag for speaking welcome message
        "useGpu": config.getboolean('DEFAULT', 'useGpu', fallback=True)  # Get flag for using GPU processing
    }
