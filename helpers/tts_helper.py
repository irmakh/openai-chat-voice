import torch
from TTS.api import TTS
import pygame
from helpers.console_helper import print_text
from bgcolors import bcolors

def run_tts(answer: str,fileDate: str, config) -> None:
    """
    Run the TTS model, generate speech based on the user's prompt, and play the generated audio.

    Args:
        user_prompt (str): The user's prompt to generate speech from
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"

    #tts = TTS(model_name="tts_models/tr/common-voice/glow-tts", progress_bar=False).to(device)
    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False).to(device)

    if config["printGeneratedText"]:
        # Print the generated text
        print_text(answer,config)
    
    fullFile = config["sound_directory"] + "stream.wav"
   
    if config["keepGeneratedFile"]:
        fullFile = f"{config['sound_directory']}{fileDate}-sound.wav" 

    if answer is None:
        answer = "no answer"

    tts.tts_to_file(text=answer, file_path=fullFile)
    del tts
    if config["readAftergenerate"]:
        play_audio(fullFile,config)

def play_audio(file_path: str,config) -> None:
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
    print_text(f"{bcolors.OKBLUE}Press Ctrl+C to stop playing{bcolors.ENDC}",config,False)
    try:
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
