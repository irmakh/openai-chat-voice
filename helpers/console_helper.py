
import os
from bgcolors import bcolors
from helpers.memory_helper import run_garbage_collection


def print_text(answer: str, config, headers: bool = True) -> None:
    """
    Print out the generated text in a formatted way.

    Args:
        answer (str): The generated text to print
        headers (bool, optional): Whether to add headers to the output. Defaults to True.

    Returns:
        None
    """
    if config["print_generated_text"]:
        if headers:
            print("\n\n")
            print(f"{bcolors.HEADER}{bcolors.BOLD}==============================================")
            print("                  TEXT TO SPEECH                ")
            print(f"=============================================={bcolors.ENDC}")
            print("\n")
        print(answer)
        if headers:
            print("\n")
            print(f"{bcolors.HEADER}==============================================")
            print("                  END OF SPEECH               ")
            print(f"=============================================={bcolors.ENDC}")

def get_user_input(config) -> str:
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

def exit_program(config) -> None:
    """
    Exit the program gracefully.

    This function runs the garbage collector, prints a message, plays a goodbye sound, and exits the program with code 0.

    Args:
        None

    Returns:
        None
    """
    run_garbage_collection()

    file_path = os.path.join(config['sound_directory'], "stream.wav")
    if os.path.exists(file_path):
        os.remove(file_path)
    print(f"{bcolors.HEADER}==============================================")
    print("               Thank you for using             ")
    print("                Our Application!               ")
    print("                Exiting program...               ")
    print(f"=============================================={bcolors.ENDC}")
    print("\n")
    exit(0)
