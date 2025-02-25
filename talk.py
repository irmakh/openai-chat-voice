import datetime
import re
from openai import OpenAI
from config_loader import load_config
from helpers.tts_helper import run_tts, play_audio
from helpers.memory_helper import run_garbage_collection
from helpers.transcript_helper import save_transcript
from helpers.console_helper import get_user_input, exit_program
from helpers.chat_helper import generate

def main() -> None:
    """
    Main function to execute the program loop.

    This function initializes garbage collection, continuously gets user input,
    generates a response using the chat model, and then converts the response
    to speech using the TTS model. The loop continues until the user inputs 'bye'.

    Args:
        None

    Returns:
        None
    """
    config = load_config()
    # Initialize configuration settings and run garbage collection
    if config["speakWelcome"]:
        play_audio("hi.wav",config)
    run_garbage_collection()
    # Client to interact with the OpenAI API
    client = OpenAI(base_url=config["base_url"],api_key=config["OPENAI_API_KEY"])
    chatHistoryArray = [config["initialContent"]]
    memory = config["memoryMessageCount"]*2
    
    # Main program loop
    while True:
        fileDate = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        user_prompt= get_user_input(config)

        if user_prompt.lower() == "bye":
            if config["speakWelcome"]:
                play_audio("bye.wav",config)
            break
        
        chatHistory = '\n'.join(chatHistoryArray[-memory:])
        chatHistory = chatHistory.replace("{botName}", config["botName"])
        answer: str = generate(user_prompt,chatHistory, client, config)
        historyAnswer = answer

        if config["removeDeepseekThinkTags"]:
            # Remove text inside <think></think> tags from content
            answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL)

        chatHistoryArray.append("User: "+user_prompt)
        chatHistoryArray.append(f"{config['botName']}: "+historyAnswer)

        if len(chatHistoryArray) > memory:
            del chatHistoryArray[:-memory]
        
        del chatHistoryArray[0]
        chatHistoryArray = [config["initialContent"]]+chatHistoryArray

        run_tts(answer,fileDate,config)
        
        save_transcript(user_prompt, answer, fileDate,config)

        run_garbage_collection()
    # Exit the program
    exit_program(config)

if __name__ == "__main__":
    main()

