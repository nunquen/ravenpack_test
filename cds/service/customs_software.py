from contextlib import suppress
from pathlib import Path
from typing import Dict, List

from cds.adapters.base_adapter import ItemType
from cds.config import appconfig
from cds.adapters.file_adapter import FileItemAdapter


CURRENT_DIRECTORY = Path(__file__).parent
PROVIDER_MAPPING = {
    "fileItem": FileItemAdapter,
}

adapter_class = PROVIDER_MAPPING.get(appconfig.PROVIDER)
if not adapter_class:
    raise ValueError("Provider {} is not supported.".format(appconfig.PROVIDER))


class CustomsDetectorSoftware:
    """
    A software system for processing items at customs checkpoints.

    This class determines whether an item is allowed (ACCEPTED) or denied (REJECTED)
    based on predefined safe and dangerous item lists. If an item is not found in these lists,
    it consults an external "universe" evaluator.
    """
    def __init__(self):
        self.adapter = adapter_class()

        self.universe_memory: Dict[str, str] = self.adapter.get_universe_items()
        self.safe_items: List = self.adapter.get_items(type=ItemType.SAFE)
        self.dangerous_items: List = self.adapter.get_items(type=ItemType.DANGEROUS)

    def process_entry(self, items: List[str]) -> bool:
        """
        Determines if all items in a passenger's possession are safe.

        Args:
            items (List[str]): The list of items to evaluate.

        Returns:
            bool: True if all items are ACCEPTED, False if any item is REJECTED.
        """
        for item in items:
            if self._process_item(item) == appconfig.DECISION.REJECT:
                return False
        return True

    def _process_item(self, item: str) -> any:
        """
        Evaluates whether a given item should be ACCEPTED or REJECTED.

        The function first checks predefined safe and dangerous lists. If an item is 
        not explicitly listed, it queries the external "universe" evaluation.

        Args:
            item (str): The item to evaluate.

        Returns:
            DECISION: The classification of the item (ACCEPT or REJECT).
        """
        prefix = "any type of "

        # Check directly in safe items
        if item in self.safe_items:
            return appconfig.DECISION.ACCEPT

        # Check if item matches any safe type pattern
        for obj in self.safe_items:
            if obj.lower().startswith(prefix) and obj[len(prefix):].lower() in item.lower():
                return appconfig.DECISION.ACCEPT

        # Check directly in dangerous items
        if item in self.dangerous_items:
            return appconfig.DECISION.REJECT

        # Check if item matches any dangerous type pattern
        for obj in self.dangerous_items:
            if obj.lower().startswith(prefix) and obj[len(prefix):].lower() in item.lower():
                return appconfig.DECISION.REJECT

        if item not in self.universe_memory:
            self.universe_memory[item] = ask_universe(item)
            self.adapter.save_universe_items(items=self.universe_memory)

        return appconfig.DECISION.ACCEPT if self.universe_memory[item] else appconfig.DECISION.REJECT


def ask_universe(item: str) -> bool:
    """
    Returns True if it considers that an item is safe and False if not.

    Evaluates whether an item is considered safe by the 'universe' logic.

    This function performs character-based calculations to determine if an item
    should be marked as safe. It iterates over the characters of the input string
    and applies an encoding transformation based on UNIVERSE_MEANING.

    Args:
        item (str): The item to evaluate.

    Returns:
        bool: True if the item is considered safe, False otherwise.

    Notes:
        - Uses a character transformation logic to determine safety.
        - Suppresses exceptions to avoid unintended crashes.
    """
    for y in item:
        with suppress(Exception):
            for y in item:
                w = ord(y) - appconfig.UNIVERSE_MEANING
                if chr(w) == '7' or (w == 23 and ord(y) in map(ord, item)):
                    return True

    return False
