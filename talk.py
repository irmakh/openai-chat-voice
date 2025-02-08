

from TTS.api import TTS
import torch
from openai import OpenAI
import pygame
import datetime
import gc
import os
import configparser

def get_config()->None: 
    """
    Load configuration settings from a file and set global variables.

    This function reads a configuration file named 'config.ini' using ConfigParser
    and sets several global variables based on the 'DEFAULT' section of the file.
    It provides fallback values for each configuration variable if they are not
    present in the file. The configuration includes settings for the chat model
    name, API key, base URL, sound directory, and various flags controlling 
    file generation and output behavior.

    Globals:
        chat_model_name (str): Name of the chat model to use.
        base_url (str): Base URL for the API.
        OPENAI_API_KEY (str): API key for authentication.
        sound_directory (str): Directory for storing sound files.
        keepGeneratedFile (bool): Flag to determine if generated files should be kept.
        generateTranscript (bool): Flag to determine if transcripts should be generated.
        content (str): Content description for the assistant's behavior.
        readAftergenerate (bool): Flag to play audio after generation.
        printGeneratedText (bool): Flag to print generated text.
    Raises:
    """

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini')

    # Access configuration variables
    global chat_model_name
    chat_model_name = config.get('DEFAULT', 'chat_model_name', fallback="llama-3.1-8b-lexi-uncensored-v2")
    global base_url
    base_url = config.get('DEFAULT', 'base_url', fallback="http://localhost:1234/v1/")
    global OPENAI_API_KEY
    OPENAI_API_KEY = config.get('DEFAULT', 'OPENAI_API_KEY', fallback=os.environ.get("OPENAI_API_KEY"))

    if OPENAI_API_KEY is None:
        print("OPENAI_API_KEY not set in config or as environment variable, using default")
        OPENAI_API_KEY = 'your-api-key'

    global sound_directory
    sound_directory = config.get('DEFAULT', 'sound_directory', fallback="sound-streams/")
    global keepGeneratedFile
    keepGeneratedFile = config.getboolean('DEFAULT', 'keepGeneratedFile', fallback=True)
    global generateTranscript
    generateTranscript = config.getboolean('DEFAULT', 'generateTranscript', fallback=True)
    global initialContent
    initialContent = config.get('DEFAULT', 'initialContent', fallback="You are a historian answering questions. You will state users question first than answer.")
    global readAftergenerate
    readAftergenerate = config.getboolean('DEFAULT', 'readAfterGenerate', fallback=True)
    global printGeneratedText
    printGeneratedText = config.getboolean('DEFAULT', 'printGeneratedText', fallback=True)
    global memoryMessageCount
    memoryMessageCount = config.getint('DEFAULT', 'memoryMessageCount', fallback=10)
    global botName
    botName = config.get('DEFAULT', 'botName', fallback="Bot")

# Define colors for console output
global bcolors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run_garbage_collection() -> None:
    """
    Run garbage collection and free up GPU memory.

    Args:
        None

    Returns:
        None
    """
    torch.cuda.empty_cache()
    gc.collect()
    #print(f"{bcolors.OKGREEN}{datetime.datetime.now().strftime('%H:%M:%S')} - garbage collected{bcolors.ENDC}")
    print_used_gpu_memory()

def print_used_gpu_memory() -> None:
    """
    Print out the amount of memory used by the current process on the GPU.

    This value is the total amount of memory allocated by the process on the GPU,
    and is updated every time a tensor is allocated or deallocated. It is
    expressed in megabytes.

    Args:
        None
    Returns:
        None
    """
    if torch.cuda.is_available():
        used_memory: float = torch.cuda.memory_allocated() / (1024 ** 2)  # Convert to MB
        #print(f"{bcolors.OKBLUE}Used GPU Memory: {used_memory:.2f} MB{bcolors.ENDC}")


def play_audio(file_path: str) -> None:
    """
    Play an audio file given its path. This function blocks until the audio file has finished playing.

    Args:
        file_path (str): Path to the audio file to play

    Returns:
        None
    """
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def print_text(answer: str) -> None:
    """
    Print out the generated text in a formatted way.

    Args:
        answer (str): The generated text to print

    Returns:
        None
    """
    if printGeneratedText:
        print("\n\n")
        print(f"{bcolors.HEADER}{bcolors.BOLD}==============================================")
        print(f"                  TEXT TO SPEECH                ")
        print(f"=============================================={bcolors.ENDC}")
        print("\n")
        print(answer)
        print("\n")
        print(f"{bcolors.HEADER}==============================================")
        print("                  END OF SPEECH               ")
        print(f"=============================================={bcolors.ENDC}")
       
def run_tts(answer: str) -> None:
    """
    Run the TTS model, generate speech based on the user's prompt, and play the generated audio.

    Args:
        user_prompt (str): The user's prompt to generate speech from
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"

    #tts = TTS(model_name="tts_models/tr/common-voice/glow-tts", progress_bar=False).to(device)
    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False).to(device)
    run_garbage_collection()
    #Print the generated text
    print_text(answer)
    fileDate = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fullFile = sound_directory+"stream.wav"
   
    if(keepGeneratedFile):
        fullFile = f"{sound_directory}{fileDate}-sound.wav" 

    save_transcript(user_prompt, answer, fileDate)

    tts.tts_to_file(text=answer, file_path=fullFile)
    del tts
    run_garbage_collection()
    if readAftergenerate:
        play_audio(fullFile)

def save_transcript(user_prompt: str, answer: str, fileDate: str) -> None:
    """
    Save the generated transcript to a file.

    Args:
        user_prompt (str): The original user prompt
        answer (str): The generated text response
        fileDate (str): The date and time string for the file name

    Returns:
        None
    """
    if generateTranscript:
        with open(f"{sound_directory}{fileDate}-transcript.txt", 'w') as f:
            f.write(f"Original Prompt: {user_prompt}\n\n")
            f.write(answer)




def generate(user_prompt: str, content: str) -> str:
    """
    Run the chat model based on the user's prompt and generate a response.

    Args:
        user_prompt (str): The user's prompt to generate a response from

    Returns:
        str: The generated response
    """
    
    run_garbage_collection()
    completion = client.chat.completions.create(
        model=chat_model_name,
        messages=[
            {
                "role": "system", 
                "content": content
            },
            {
                "role": "user", 
                "content": user_prompt
            }
        ],
        temperature=0.7
    )

    answer = completion.choices[0].message.content
    run_garbage_collection()

    return answer

def exit_program() -> None:
    """
    Exit the program gracefully.

    This function runs the garbage collector, prints a message, plays a goodbye sound, and exits the program with code 0.

    Args:
        None

    Returns:
        None
    """
    run_garbage_collection()
    play_audio("bye.wav")
    file_path = os.path.join(sound_directory, "stream.wav")
    if os.path.exists(file_path):
        os.remove(file_path)
    print(f"{bcolors.HEADER}==============================================")
    print("               Thank you for using             ")
    print("                Our Application!               ")
    print("                Exiting program...               ")
    print(f"=============================================={bcolors.ENDC}")
    print("\n")
    exit(0)


def get_user_input() -> str:
    """
    Get user input and return the prompt as a string.

    Returns:
        str: The user's prompt
    """
    print("\n")
    print(f"{bcolors.HEADER}{bcolors.BOLD}==============================================")
    print("                  USER PROMPT                 ")
    print(f"=============================================={bcolors.ENDC}")
    user_prompt: str = input(f"{bcolors.OKBLUE}Enter your prompt: {bcolors.ENDC}")
    print(f"{bcolors.HEADER}{bcolors.BOLD}==============================================")
    print("                END OF USER PROMPT            ")
    print(f"=============================================={bcolors.ENDC}")
    print("\n")
    return user_prompt


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
    play_audio("hi.wav")
    global user_prompt
    # Initialize configuration settings and run garbage collection
    get_config()
    run_garbage_collection()
    # Client to interact with the OpenAI API
    global client
    client = OpenAI(base_url=base_url,api_key=OPENAI_API_KEY)
    chatHistoryArray = [initialContent]
    memory = memoryMessageCount*2
    # Main program loop
    while True:
        user_prompt= get_user_input()

        if user_prompt.lower() == "bye":
            break
        
        
        chatHistory = '\n'.join(chatHistoryArray[-memory:])
        chatHistory = chatHistory.replace("{botName}", botName)

        answer: str = generate(user_prompt,chatHistory)
        chatHistoryArray.append("User: "+user_prompt)
        chatHistoryArray.append(f"{botName}: "+answer)
        if len(chatHistoryArray) > memory:
            del chatHistoryArray[:-memory]
        chatHistoryArray = [initialContent]+chatHistoryArray
        run_tts(answer)
        run_garbage_collection()
    # Exit the program
    exit_program()

main()




