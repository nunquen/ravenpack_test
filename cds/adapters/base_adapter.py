from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List


class ItemType(Enum):
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
        pass

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
        pass
