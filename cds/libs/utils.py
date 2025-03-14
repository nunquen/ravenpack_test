"""
Util functions.

Functions:
    - parse_passenger: Parses a list of strings into a Passenger object.
    - check_passenger_status: Checks if the passenger's approval status matches the expected status.
"""
from typing import List
import logging

from cds.config import appconfig
from cds.models.passanger import Passenger


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def parse_passenger(values: List[str]) -> Passenger:
    """
    Parses a list of strings into a Passenger object.

    This function takes in a list of values, where the first item is the passenger's name, the items in between
    are the items associated with the passenger, and the last item is the passenger's approval status. The approval
    status is evaluated based on the decision criteria.

    Args:
        values (List[str]): A list of strings containing the passenger's information.
                            The first item is the name, the items in the middle are the items,
                            and the last item indicates the approval status.

    Returns:
        Passenger: A Passenger object containing the parsed information.
    """
    person_name = values[0].strip()
    items = [item.strip() for item in values[1:-1]]
    approval_status = values[-1].strip() == appconfig.DECISION.ACCEPT.value
    return Passenger(
        person_name=person_name, items=items, approval_status=approval_status
    )


def check_passenger_status(approval_status: bool, passenger: Passenger):
    """
    Checks if the passenger's approval status matches the expected status.

    This function compares the approval status of the passenger with the expected status.
    If they do not match, an error message is logged; otherwise, a success message is logged.

    Args:
        approval_status (bool): The expected approval status (True for accepted, False for rejected).
        passenger (Passenger): The Passenger object whose approval status is to be checked.

    Returns:
        None
    """
    if approval_status != passenger.approval_status:
        expected_action = (
            appconfig.EXPECTED_ACTION.ACCEPTED
            if passenger.approval_status
            else appconfig.EXPECTED_ACTION.REJECTED
        )  # noqa: E501
        logging.error(
            f'"{passenger.person_name}" was not {expected_action}. Items: {passenger.items}'
        )
    else:
        logging.log(msg=f'OK - "{passenger.person_name}"', level=logging.INFO)
