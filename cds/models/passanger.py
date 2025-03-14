"""
Module for defining the Passenger data model.

Classes:
    - Passenger: A Pydantic model representing a passenger's details.

"""
from typing import List
from pydantic import BaseModel


class Passenger(BaseModel):
    """
    Represents a passenger's information.

    Attributes:
        person_name (str): The name of the passenger.
        items (List[str]): A list of items associated with the passenger.
        approval_status (bool): The approval status of the passenger; True if accepted, False if rejected.

    Example:
        Creating a Passenger instance:

        >>> passenger = Passenger(person_name="John Doe", items=["Item1", "Item2"], approval_status=True)
    """

    person_name: str
    items: List[str]
    approval_status: bool
