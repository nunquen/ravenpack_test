from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class ItemType(Enum):
    SAFE = "safe"
    DANGEROUS = "dangerous"


class BaseItemAdapter(ABC):
    """
    Abstract base class for an item storage provider.

    This class defines the required interface for any item storage system
    that handles retrieving and saving categorized items.
    """

    @abstractmethod
    def get_items(self, type: ItemType) -> List[str]:
        """
        Retrieves a list of stored items based on the given type.

        Args:
            type (ItemType): The category of items to fetch. Expected values:
                            - ItemType.SAFE: Retrieves safe items.
                            - ItemType.DANGEROUS: Retrieves dangerous items.

        Returns:
            List[str]: A list of stored items for the specified category.
        """
        pass

    @abstractmethod
    def save_items(self, type: ItemType, value: List[str]):
        """
        Saves a list of items under the specified category.

        Args:
            type (ItemType): The category of items to save. Expected values:
                            - ItemType.SAFE: Saves safe items.
                            - ItemType.DANGEROUS: Saves dangerous items.
            value (List[str]): A list of items to be saved.

        Returns:
            None

        Notes:
            - Subclasses must implement this method to store items persistently.
            - Implementations should handle file or database interactions properly.
        """
        pass
