"""
ChatGPT Text Tools Script

Author: Wilmer Leon
Contact: https://www.linkedin.com/in/wilmer-leon/

Description:
This script provides tools for checking grammar, generating TLDRs, and listing available OpenAI models. It is designed to be efficient, maintainable, and robust, making it suitable for publication and professional use.

Usage:
Run the script with the following command:
    python chatgpt_text_tools.py <task> [<text>]

Tasks:
- 'grammar': Checks and corrects grammar in the provided text.
- 'tldr': Generates a concise TLDR for the provided text.
- 'list_models' or 'lm': Lists all available OpenAI models.

Dependencies:
- Python 3.8 or higher
- `openai` package (install with `pip install openai`)
- An active OpenAI API key set in the environment variable `OPENAI_API_KEY`

"""

import os
import sys
import datetime
import openai
import keyring

# Constants for OpenAI models
MODEL_CHECK_GRAMMAR = "gpt-4o-2024-08-06"
MODEL_TLDR = "gpt-4o-2024-08-06"

class ChatGPTHelper:
    """
    Helper class to interact with OpenAI models for grammar checking, TLDR generation, and listing available models.
    """

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = api_key

    @staticmethod
    def log_to_file(filename, message, verbose=False):
        """Logs messages to a file with a timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a") as f:
            f.write(f"{timestamp} - {message}\n")
        if verbose:
            print(f"Log: {timestamp} - {message}")

    def check_grammar(self, text, log_file="grammar_log.txt", verbose=False):
        """
        Checks grammar for the provided text using OpenAI.

        :param text: The text to check grammar for.
        :param log_file: File to log the operations.
        :param verbose: If True, prints log messages.
        :return: Corrected text.
        """
        self.log_to_file(log_file, f"Received text: {text}", verbose)
        prompt = f"Check grammar, only output the text, no explanations or comments: {text}"
        
        try:
            completion = openai.ChatCompletion.create(
                model=MODEL_CHECK_GRAMMAR,
                messages=[{"role": "user", "content": prompt}],
            )
            corrected_text = completion.choices[0].message.content.strip()
            self.log_to_file(log_file, f"Corrected text: {corrected_text}", verbose)
            return corrected_text
        except Exception as e:
            self.log_to_file(log_file, f"Error: {e}", verbose)
            raise

    def generate_tldr(self, text, log_file="grammar_log.txt", verbose=False):
        """
        Generates a TLDR for the provided text using OpenAI.

        :param text: The text to summarize.
        :param log_file: File to log the operations.
        :param verbose: If True, prints log messages.
        :return: Generated TLDR.
        """
        self.log_to_file(log_file, f"Received text: {text}", verbose)
        prompt = f"Provide a TLDR for the following email. Do not use 3rd person, just a 1st person TLDR: {text}"
        
        try:
            completion = openai.ChatCompletion.create(
                model=MODEL_TLDR,
                messages=[{"role": "user", "content": prompt}],
            )
            tldr = completion.choices[0].message.content.strip()
            self.log_to_file(log_file, f"TLDR: {tldr}", verbose)
            return tldr
        except Exception as e:
            self.log_to_file(log_file, f"Error: {e}", verbose)
            raise

    def list_models(self, verbose=False):
        """
        Lists all available models from OpenAI.

        :param verbose: If True, prints log messages.
        :return: List of model names.
        """
        try:
            models = openai.Model.list()
            model_names = [model['id'] for model in models['data']]
            if verbose:
                print("Available models:")
                for name in model_names:
                    print(f"- {name}")
            return model_names
        except Exception as e:
            if verbose:
                print(f"Error fetching models: {e}")
            raise


def main():
    """
    Main entry point for the script. Handles command-line arguments.
    """
    if len(sys.argv) < 2:
        print("Usage: python chatgpt_text_tools.py <task> [<text>]")
        sys.exit(1)

    task = sys.argv[1].lower()
    text = sys.argv[2] if len(sys.argv) > 2 else None
    api_key = keyring.get_password("OPENAI_API_KEY", "ChatGPT Integration")

    if not api_key:
        print("API key not found in Keychain. Please add it first.")
        print("Use Keychain Access to add the key with:")
        print(" - Service name: OPENAI_API_KEY")
        print(" - Account name: ChatGPT Integration")
        sys.exit(1)

    try:
        helper = ChatGPTHelper(api_key)
        if task == "grammar":
            if not text:
                print("Error: Text is required for the 'grammar' task.")
                sys.exit(1)
            result = helper.check_grammar(text, verbose=True)
        elif task == "tldr":
            if not text:
                print("Error: Text is required for the 'tldr' task.")
                sys.exit(1)
            result = helper.generate_tldr(text, verbose=True)
        elif task in ["list_models", "lm"]:
            result = helper.list_models(verbose=True)
        else:
            print("Invalid task. Use 'grammar', 'tldr', or 'list_models'/'lm'.")
            sys.exit(1)

        if result:
            print(result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
