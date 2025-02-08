

from TTS.api import TTS
import torch
from openai import OpenAI
import pygame
import datetime
import gc
import os

# Name of the chat model to use
chat_model_name="llama-3.1-8b-lexi-uncensored-v2"

# URL of the OpenAI API
base_url = "http://localhost:1234/v1/"

# API key for the OpenAI API
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    print("OPENAI_API_KEY not set as environment variable, using default")
    OPENAI_API_KEY = 'your-api-key'


# Content to send to the chat model
# This is the prompt that the chat model will respond to
content = "You are a historian answering questions. You will state users question first than answer."

# Directory to store audio files
sound_directory = "sound-streams/"

# Keep the generated audio files after they have been played
# The file will be named <date>-sound.wav
keepGeneratedFile = True

# Generate a transcript of the chat session
# This will save the transcript to a text file
# The file will be named <date>-transcript.txt
generateTranscript = True

# Client to interact with the OpenAI API
client = OpenAI(base_url=base_url,api_key=OPENAI_API_KEY)

# Define colors for console output
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
    print("\n\n")
    print(f"{bcolors.HEADER}{bcolors.BOLD}==============================================")
    print(f"                  TEXT TO SPEECH                ")
    print(f"=============================================={bcolors.ENDC}")
    print("\n")
    print(answer)
    print("\n")
    print(f"{bcolors.HEADER}==============================================")
    print("                  END OF SPEECH               ")
    print("==============================================")
    print("               Thank you for using             ")
    print("                Our Application!               ")
    print(f"=============================================={bcolors.ENDC}")
    print("\n")

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
    if(generateTranscript):
        with open(f"{sound_directory}{fileDate}-transcript.txt", 'w') as f:
            f.write(answer)
    tts.tts_to_file(text=answer, file_path=fullFile)
    del tts
    run_garbage_collection()
    play_audio(fullFile)


def generate(user_prompt: str) -> str:
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
                "role": "assistant", 
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
    print("Exiting program...")
    play_audio("bye.wav")
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
    run_garbage_collection()
    while True:
        user_prompt: str = get_user_input()

        if user_prompt.lower() == "bye":
            break

        answer: str = generate(user_prompt)
        run_tts(answer)

        run_garbage_collection()




main()
exit_program()


