

def save_transcript(user_prompt: str, answer: str, fileDate: str, config) -> None:
    """
    Save the generated transcript to a file.

    Args:
        user_prompt (str): The original user prompt
        answer (str): The generated text response
        fileDate (str): The date and time string for the file name

    Returns:
        None
    """
    
    if config["generateTranscript"]:
        with open(f"{config['transcript_directory']}{fileDate}-transcript.txt", 'w') as f:
            f.write(f"Original Prompt: {user_prompt}\n\n")
            f.write(str(answer))
