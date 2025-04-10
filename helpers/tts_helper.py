import torch
from TTS.api import TTS
import pygame
from bgcolors import bcolors
from helpers.console_helper import print_text
def run_tts(answer: str, file_date: str, config) -> None:
    """
    Run the TTS model, generate speech based on the user's prompt, and play the generated audio.

    Args:
        answer (str): The user's prompt to generate speech from
        file_date (str): The date for the output file name
        config: Configuration dictionary with settings for the text-to-speech engine and playback
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    #tts_model_name = "tts_models/en/jenny/jenny"
    tts_model_name = config['bot_sound']
    # Initialize TTS model
    tts = TTS(model_name=tts_model_name, progress_bar=False).to(device)
    if config["print_generated_text"]:
        # Print the generated text
        print_text(answer, config)

    file_extension = "-generated.wav" if config["keep_generated_file"] else ".wav"
    file_name = f"{config['sound_directory']}stream{file_extension}"
    if config["keep_generated_file"]:
        file_name = f"{config['sound_directory']}{file_date}{file_extension}"
    output_file_path = file_name
    if answer is None:
        answer = "no answer"

    # Generate and save the TTS audio
    tts.tts_to_file(text=answer, file_path=output_file_path)
    del tts


    if config["read_after_generate"]:
        play_audio(output_file_path, config)
    

def play_audio(file_path: str, config) -> None:
    """
    Play an audio file given its path. This function blocks until the audio file has finished playing.

    Args:
        file_path (str): Path to the audio file to play
        config: Configuration dictionary with settings for playback

    Returns:
        None
    """
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    print_text(f"{bcolors.OKBLUE}Press Ctrl+C to stop playing{bcolors.ENDC}", config, False)

    try:
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except KeyboardInterrupt:
        pygame.mixer.music.stop()