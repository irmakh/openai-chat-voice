import os
import logging

# Set up logging configuration
logger = logging.getLogger(__name__)

def open_file(file_path):
    # Open a file for writing and return the file object
    try:
        return open(file_path, 'w')
    except Exception as e:
        # Log an error message if opening the file fails
        logger.error(f"Failed to open file {file_path}. Error: {str(e)}")
        raise

def write_to_opened_file(opened_file, contents):
    # Write contents to a previously opened file and flush any buffered data
    try:
        opened_file.write(contents)
        opened_file.flush()
    except Exception as e:
        # Log an error message if writing to the file fails
        logger.error("Failed to write to file. Error: " + str(e))
        raise

def write_transcript(contents, config, file_date):
    # Write transcript contents to a new text file with a filename based on the current date
    try:
        file_path = os.path.join(config["transcript_directory"], f"{file_date}-transcript.txt")
        with open_file(file_path) as file:
            write_to_opened_file(file, contents)
            logger.info("Transcript written successfully.")
    except Exception as e:
        # Log an error message if writing the transcript fails
        logger.error("Failed to write transcript. Error: " + str(e))
        raise

def write_sound(contents, config, file_date):
    # Write sound data to a new WAV file with a filename based on the current date
    try:
        file_path = os.path.join(config["sound_directory"], f"{file_date}-sound.wav")
        with open_file(file_path, 'wb') as file:
            write_to_opened_file(file, contents)
            logger.info("Sound data written successfully.")
    except Exception as e:
        # Log an error message if writing the sound data fails
        logger.error("Failed to write sound data. Error: " + str(e))
        raise