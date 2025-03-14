# AI Chatbot with Text-to-Speech Capabilities

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-00F300?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![TTS](https://img.shields.io/badge/TTS-FFC107?style=for-the-badge&logo=tts&logoColor=white)](https://github.com/mozilla/TTS)

## Overview

This project implements an interactive chatbot that combines the power of OpenAI's language models with text-to-speech technology. The chatbot can:

- Generate human-like responses to user input using OpenAI's chat models
- Convert text responses to natural-sounding speech
- Support both OpenAI API and LM Studio as providers
- Provide an interactive conversation experience

## Features

- 🤖 **Advanced Language Processing**: Leverages OpenAI's chat models for intelligent responses
- 🗣️ **Text-to-Speech**: Converts text responses to natural speech output
- 🔄 **Interactive Mode**: Continuous conversation until explicitly terminated
- 🔌 **Flexible API Support**: Works with both OpenAI API and LM Studio
- 🔒 **Secure**: Uses environment variables for API key management

## Quick Start

1. **Clone and Setup:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   pip install -r requirements.txt
   ```

2. **Configure API Key:**
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

3. **Run the Program:**
   ```bash
   python talk.py
   ```

## Detailed Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Internet connection for API access

### Step-by-Step Setup

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

The program will prompt you for input, generate responses using the chat model, convert them to speech, and play them back. Enter 'bye' or 'exit' to terminate the program.

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

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
