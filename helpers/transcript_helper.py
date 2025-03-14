from helpers.file_helper import write_transcript
def save_transcript(user_prompt: str, answer: str, file_date: str, config) -> None:
    """
    Save the generated transcript to a file.

    Args:
        user_prompt (str): The original user prompt
        answer (str): The generated text response
        file_date (str): The date and time string for the file name

    Returns:
        None
    """
    
    if config["generate_transcript"]:
        write_transcript(f"Original Prompt: {user_prompt}\n\n{answer}", config, file_date)

