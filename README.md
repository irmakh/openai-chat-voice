"""
README.md

This project is a chatbot that uses the OpenAI chat model to generate responses to user input. The responses are then converted to speech using the TTS model.

The project was built using the following technologies:

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-00F300?style=for-the-badge&logo=openai&logoColor=white)
![TTS](https://img.shields.io/badge/TTS-FFC107?style=for-the-badge&logo=tts&logoColor=white)

To install the project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required packages using pip: `pip install -r requirements.txt`
3. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
4. Run the program using `python talk.py`

The program will continuously prompt the user for input and generate responses using the chat model. The responses will be converted to speech using the TTS model and played back to the user.

The program will exit when the user inputs 'exit'.

This project is licensed under the MIT License. See the LICENSE file for details.
## Installation

To set up the project, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install Dependencies:**
   Make sure you have Python installed on your system. You can install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Program:**
   Execute the main script to start the program:
   ```bash
   python talk.py
   ```

The program will prompt you for input, generate responses using the chat model, convert them to speech, and play them back. It will exit when you input 'exit'.

## Using LM Studio as OpenAI API Provider

To use LM Studio as your OpenAI API provider, follow these steps:

1. **Install LM Studio:**
   First, ensure that you have LM Studio installed on your system. If not, download and install it from the official website.

2. **Obtain API Key:**
   Ensure you have an API key from LM Studio. This key will authenticate your requests to the LM Studio API.

3. **Set Environment Variable:**
   Set the `OPENAI_API_KEY` environment variable to your LM Studio API key. You can do this by adding the following line to your shell configuration file (e.g., `.bashrc`, `.zshrc`):

   ```bash
   export OPENAI_API_KEY='your-lm-studio-api-key'
   ```

4. **Update Base URL:**
   In your code, update the `base_url` to point to the LM Studio API endpoint. For example:

   ```python
   base_url = "https://api.lmstudio.com/v1/"
   ```

5. **Run the Program:**
   Execute your script as usual. The program will now use LM Studio as the OpenAI API provider.

By following these instructions, you can seamlessly integrate LM Studio into your existing setup as the OpenAI API provider.


