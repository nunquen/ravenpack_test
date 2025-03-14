from typing import List


def read_storage(file_path: str) -> List:
    with open(file_path) as file:
        return [line.strip() for line in file]
