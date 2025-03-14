"""
Item Storage and Evaluation Module

This module defines the structures and interfaces for managing categorized items
and their evaluations within a system. It includes:

- ItemType Enum: Categorizes items into 'safe', 'dangerous', and 'universe' types.
- BaseItemAdapter Class: An abstract base class outlining methods for retrieving,
  saving, and managing evaluations of items across different categories.
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List


class ItemType(Enum):
    """
    ItemType Enum

    Enumeration representing different categories of items.

    Attributes:
        SAFE (str): Represents items that are considered safe.
        DANGEROUS (str): Represents items that are considered dangerous.
        UNIVERSE (str): Represents items that are evaluated in the universe context.
    """

    SAFE = "safe"
    DANGEROUS = "dangerous"
    UNIVERSE = "universe"


class BaseItemAdapter(ABC):
    """
    Abstract base class for an item storage provider.

    This class defines the required interface for any item storage system
    that handles retrieving and saving categorized items.
    """

    @abstractmethod
    def get_items(self, item_type: ItemType) -> List[str]:
        """
        Retrieves a list of stored items based on the given item_type.

        Args:
            item_type (ItemType): The category of items to fetch. Expected values:
                            - ItemType.SAFE: Retrieves safe items.
                            - ItemType.DANGEROUS: Retrieves dangerous items.

        Returns:
            List[str]: A list of stored items for the specified category.
        """

    @abstractmethod
    def save_items(self, item_type: ItemType, value: List[str]):
        """
        Saves a list of items under the specified category.

        Args:
            item_type (ItemType): The category of items to save. Expected values:
                            - ItemType.SAFE: Saves safe items.
                            - ItemType.DANGEROUS: Saves dangerous items.
            value (List[str]): A list of items to be saved.

        Returns:
            None

        Notes:
            - Subclasses must implement this method to store items persistently.
            - Implementations should handle file or database interactions properly.
        """

    @abstractmethod
    def save_universe_items(self, items: Dict[str, str]):
        """
        Saves the current state of universe-evaluated items.

        This method is responsible for persisting the universe's memory of item evaluations.
        Implementing classes should define how the data is stored (e.g., in a file, database, or cache).

        Args:
            items (Dict[str, str]): A dictionary where keys are item names and values are their evaluation
                                    status (e.g., "ACCEPT" or "REJECT").

        Returns:
            None
        """

    @abstractmethod
    def get_universe_items(self) -> Dict[str, str]:
        """
        Retrieves the stored universe evaluation results for items.

        This method is responsible for fetching the previously saved evaluation results
        of items (e.g., whether they were ACCEPTED or REJECTED). Implementing classes should
        define how the data is retrieved (e.g., from a file, database, or cache).

        Returns:
            Dict[str, str]: A dictionary where keys are item names and values are their evaluation
                            status (e.g., "ACCEPT" or "REJECT").
        """
