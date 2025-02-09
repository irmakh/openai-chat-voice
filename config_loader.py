import configparser
import os

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
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    return {
        "chat_model_name": config.get('DEFAULT', 'chat_model_name', fallback="llama-3.1-8b-lexi-uncensored-v2"),
        "base_url": config.get('DEFAULT', 'base_url', fallback="http://localhost:1234/v1/"),
        "OPENAI_API_KEY": config.get('DEFAULT', 'OPENAI_API_KEY', fallback=os.environ.get("OPENAI_API_KEY") or 'your-api-key'),
        "sound_directory": config.get('DEFAULT', 'sound_directory', fallback="sound-streams/"),
        "keepGeneratedFile": config.getboolean('DEFAULT', 'keepGeneratedFile', fallback=True),
        "generateTranscript": config.getboolean('DEFAULT', 'generateTranscript', fallback=True),
        "initialContent": config.get('DEFAULT', 'initialContent', fallback="You are a historian answering questions. You will state users question first than answer."),
        "readAftergenerate": config.getboolean('DEFAULT', 'readAfterGenerate', fallback=True),
        "printGeneratedText": config.getboolean('DEFAULT', 'printGeneratedText', fallback=True),
        "memoryMessageCount": config.getint('DEFAULT', 'memoryMessageCount', fallback=10),
        "botName": config.get('DEFAULT', 'botName', fallback="Bot"),
        "removeDeepseekThinkTags": config.getboolean('DEFAULT', 'removeDeepseekThinkTags', fallback=True),
        "speakWelcome": config.getboolean('DEFAULT', 'speakWelcome', fallback=True)
    }
