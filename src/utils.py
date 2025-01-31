from src.alias import JsonFileName
from typing import Union, IO
import dotenv
import json

class QuizFileHandler:
    """A context manager for handling JSON quiz files.
    
    Attributes:
        file_path (JsonFileName): The path to the JSON file.
        json_file (Union[IO, None]): The JSON file object.
    
    Methods:
        load: Loads the JSON file.
    """

    file_path: JsonFileName
    json_file: Union[IO, None]

    def __init__(self, file_path: JsonFileName) -> None:
        self.file_path = file_path
        self.json_file = None

    def __enter__(self) -> IO:
        self.json_file = open(self.file_path, 'r')
        return self.json_file
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.json_file.close()
        self.json_file = None

    def load(self) -> dict:
        """Loads the quiz from a JSON file.

        Returns:
            dict: The JSON file as a dictionary.
        """
        return json.load(self.json_file)


def get_discord_token(env_filepath: str = 'data/.env') -> str:
    """Loads the Discord bot token from a .env file.

    Returns:
        str: The Discord bot token.
    """
    dotenv.load_dotenv(dotenv_path=env_filepath)
    return dotenv.dotenv_values()['DISCORD_BOT_TOKEN']
