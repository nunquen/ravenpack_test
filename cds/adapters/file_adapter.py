"""
File Item Adapter Module

This module defines the adapter pattern for managing item storage in files, specifically for items
categorized as safe, dangerous, and universe. It includes functions for reading and writing items
from/to text files and JSON files, along with a class to interact with the storage system.

Key components:
- Utility functions for reading and writing item data from/to files (`read_storage`, `read_json_storage`,
  `save_json_storage`).
- `FileItemAdapter`: An implementation of `BaseItemAdapter` to handle item fetching and saving from files.
"""
from pathlib import Path
from typing import Dict, List

import json
import logging

from .base_adapter import BaseItemAdapter, ItemType


CURRENT_DIRECTORY = Path(__file__).parent


def read_storage(
    file_path: str,
) -> List:
    """
    Reads a file and returns its contents as a list of stripped strings.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        List[str]: A list of lines from the file with leading/trailing whitespace removed.
                   If an error occurs while reading the file, an empty list is returned.

    Logs:
        Logs an error message if the file cannot be read due to an IOError.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file]
    except IOError as ioe:
        logging.error("Error reading file. '{}': {}".format(file_path, ioe))
        return []


def read_json_storage(file_path: str) -> Dict[str, str]:
    """
    Reads a JSON file and returns its contents as a dictionary.

    This function attempts to read a JSON file from the provided file path and
    parse it into a dictionary with string keys and string values. If the file
    does not exist, is improperly formatted, or contains invalid data, the function
    logs an error and returns an empty dictionary.

    Args:
        file_path (str): The path to the JSON file to be read.

    Returns:
        Dict[str, str]: A dictionary where keys are item names and values are their
                        evaluation status (e.g., "ACCEPT" or "REJECT"). If an error occurs,
                        returns an empty dictionary.

    Exceptions:
        - FileNotFoundError: If the file does not exist.
        - json.JSONDecodeError: If the file is not valid JSON.
        - ValueError: If the JSON file contains invalid data or is not a dictionary.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            universe_items = json.load(file)
            return universe_items

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as err:
        logging.error("Error reading file. '{}': {}".format(file_path, err))
        return {}


def save_json_storage(file_path: str, items: Dict[str, str]):
    """
    Saves the provided dictionary to a JSON file, replacing all existing content.

    This function writes the provided dictionary of items and their evaluation
    status (e.g., "ACCEPT" or "REJECT") to a JSON file. If the file does not exist,
    it will be created. Any existing content will be replaced with the new data.
    The function also handles potential exceptions that might arise during the
    file operations.

    Args:
        file_path (str): The path to the JSON file where the data will be saved.
        items (Dict[str, str]): A dictionary where keys are item names and values
                                are their evaluation status (e.g., "ACCEPT" or "REJECT").

    Returns:
        None

    Exceptions:
        - IOError: If there's an error during file writing.
        - ValueError: If the provided dictionary is not valid.
    """
    try:
        # Ensure the directory exists
        with open(file_path, "w", encoding="utf-8") as file:
            # Write the dictionary as a JSON object, replacing any existing content
            json.dump(items, file, indent=4)

    except (IOError, ValueError) as err:
        # Log any file I/O or value-related errors
        logging.error(f"Error saving file '{file_path}': {err}")


class FileItemAdapter(BaseItemAdapter):
    """
    Adapter to fetch and save items from files.
    """

    def __init__(self):
        super().__init__()
        self.STORAGE_PATH: str = CURRENT_DIRECTORY.joinpath("../../storage").resolve(
            strict=True
        )
        self.safe_items: List = read_storage(
            self.STORAGE_PATH.joinpath("{}.txt".format(ItemType.SAFE.value))
        )
        self.dangerous_items: List = read_storage(
            self.STORAGE_PATH.joinpath("{}.txt".format(ItemType.DANGEROUS.value))
        )
        self.universe_items: Dict[str, str] = read_json_storage(
            self.STORAGE_PATH.joinpath("{}.json".format(ItemType.UNIVERSE.value))
        )

    def get_items(self, item_type: ItemType) -> List[str]:
        """
        Retrieves a list of items based on the specified item_type.

        Args:
            item_type (ItemType): The category of items to fetch. Can be:
                - ItemType.SAFE: Returns a list of safe items.
                - ItemType.DANGEROUS: Returns a list of dangerous items.

        Returns:
            List[str]: A list of items corresponding to the given item_type.
        """
        return self.safe_items if item_type == ItemType.SAFE else self.dangerous_items

    def save_items(self, item_type: str, value: List[str]):
        """
        Saves a list of items to a corresponding file based on the item item_type.

        Args:
            item_type (str): The category of items to save. Expected values:
                - "safe" for safe items.
                - "dangerous" for dangerous items.
            value (List[str]): A list of items to be saved.

        Returns:
            None

        Notes:
            - This function should write the given items to a predefined storage location.
            - Ensure proper handling of file operations to avoid data loss.
        """
        # Implement file writing logic

    def get_universe_items(self) -> Dict[str, str]:
        """
        Fetches items from a JSON file and returns their evaluation status.

        This method reads a JSON file containing the evaluation status of items and
        returns it as a dictionary where the keys are item names and the values are
        their evaluation status (e.g., "ACCEPT" or "REJECT").

        Returns:
            Dict[str, str]: A dictionary where keys are item names and values are their evaluation
                            status (e.g., "ACCEPT" or "REJECT").
        """
        return self.universe_items

    def save_universe_items(self, items: Dict[str, str]):
        """Saves items to a file."""
        self.universe_items = items

        save_json_storage(
            self.STORAGE_PATH.joinpath("{}.json".format(ItemType.UNIVERSE.value)),
            items=self.universe_items,
        )
