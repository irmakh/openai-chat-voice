import os 
def open_file(filepath):
    """
    Opens a file in write mode.

    Args:
        filepath (str): The path to the file to open.

    Returns:
        file: The opened file.
    """
    return open(filepath, 'w')

def write_to_opened_file(opened_file, contents):
    """
    Writes to an opened file.

    Args:
        opened_file (file): The file to write to.
        contents (str): The text to write.
    """
    # Write the contents to the file
    opened_file.write(contents)
    # Flush the file to make sure all the write operations have been completed
    opened_file.flush()
def write_transcript(contents, config, fileDate):
    """
    Writes the transcript to a file.

    Args:
        contents (str): The transcript contents to write.
        config (dict): The configuration dictionary.
        fileDate (str): The date and time string for the file name.

    Returns:
        None
    """
    # Open the file in write mode
    with open_file(config["transcript_directory"] + fileDate + "-transcript.txt") as file:
        # Write the contents to the file
        write_to_opened_file(file, contents)

def write_sound(contents, config, fileDate):
    """
    Writes the audio data to a file.

    Args:
        contents (bytes): The audio data to write.
        config (dict): The configuration dictionary.
        fileDate (str): The date and time string for the file name.

    Returns:
        None
    """
    # Open the file in write binary mode
    with open_file(config["sound_directory"] + fileDate + "-sound.wav", 'wb') as file:
        # Write the contents to the file
        write_to_opened_file(file, contents)

