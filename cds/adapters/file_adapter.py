from .base_adapter import BaseItemAdapter, ItemType
from pathlib import Path
from typing import List

import logging


CURRENT_DIRECTORY = Path(__file__).parent


def read_storage(file_path: str) -> List:
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
        with open(file_path) as file:
            return [line.strip() for line in file]
    except IOError as ioe:
        logging.error("Error reading file. '{}': {}".format(
            file_path,
            ioe
        ))
        return []


class FileItemAdapter(BaseItemAdapter):
    """
    Adapter to fetch and save items from files.
    """
    def __init__(self):
        super().__init__()
        STORAGE_PATH: str = CURRENT_DIRECTORY.joinpath("../../storage").resolve(strict=True)
        self.safe_items: List = read_storage(
            STORAGE_PATH.joinpath("{}.txt".format(ItemType.SAFE.value))
        )
        self.dangerous_items: List = read_storage(
            STORAGE_PATH.joinpath("{}.txt".format(ItemType.DANGEROUS.value))
        )

    def get_items(
        self,
        type: ItemType
    ) -> List[str]:
        """
        Retrieves a list of items based on the specified type.

        Args:
            type (ItemType): The category of items to fetch. Can be:
                - ItemType.SAFE: Returns a list of safe items.
                - ItemType.DANGEROUS: Returns a list of dangerous items.

        Returns:
            List[str]: A list of items corresponding to the given type.
        """
        return self.safe_items if type == ItemType.SAFE else self.dangerous_items

    def save_items(
        self,
        type: str,
        value: List[str]
    ):
        """
        Saves a list of items to a corresponding file based on the item type.

        Args:
            type (str): The category of items to save. Expected values:
                - "safe" for safe items.
                - "dangerous" for dangerous items.
            value (List[str]): A list of items to be saved.

        Returns:
            None

        Notes:
            - This function should write the given items to a predefined storage location.
            - Ensure proper handling of file operations to avoid data loss.
        """
        pass  # TODO: Implement file writing logic
