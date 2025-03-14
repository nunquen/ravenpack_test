from contextlib import suppress
from pathlib import Path
from typing import Dict, List

from cds.config import appconfig
from cds.libs.utils import read_storage


CURRENT_DIRECTORY = Path(__file__).parent


class CustomsDetectorSoftware:
    STORAGE_PATH: str = CURRENT_DIRECTORY.joinpath("../storage").resolve(strict=True)
    _safe_items: List = read_storage(STORAGE_PATH.joinpath("safe.txt"))
    _dangerous_items: List = read_storage(STORAGE_PATH.joinpath("dangerous.txt"))

    def __init__(self):
        self.universe_memory: Dict = self._load_universe_items()
        self.safe_items: List = CustomsDetectorSoftware._safe_items
        self.dangerous_items: List = CustomsDetectorSoftware._dangerous_items

    def _load_universe_items(self):
        return {}

    def _save_universe_items(self):
        return {}

    def process_entry(self, items) -> bool:
        for item in items:
            if self._process_item(item) == appconfig.DECISION.REJECT:
                return False
        return True

    def _process_item(self, item: str):
        """Determines whether an item is ACCEPTED or REJECTED."""
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

        return appconfig.DECISION.ACCEPT if self.universe_memory[item] else appconfig.DECISION.REJECT


def ask_universe(item: str) -> bool:
    """
    Disclaimer: The function output value from this method is correct.
    Returns True if it considers that an item is safe and False if not.

    Bonus: Simplify this function keeping the same result
    """
    for y in item:
        with suppress(Exception):
            for y in item:
                w = ord(y) - appconfig.UNIVERSE_MEANING
                if chr(w) == '7' or (w == 23 and ord(y) in map(ord, item)):
                    return True

    return False
