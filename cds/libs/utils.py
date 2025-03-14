from typing import List
import logging

from cds.config import appconfig
from cds.models.passanger import Passenger


logging.basicConfig(
    level=logging.INFO,  # Set the minimum level of messages to display
    format="%(asctime)s - %(levelname)s - %(message)s"  # Format log messages
)


def parse_passenger(values: List[str]) -> Passenger:
    person_name = values[0].strip()
    items = [item.strip() for item in values[1:-1]]
    approval_status = values[-1].strip() == appconfig.DECISION.ACCEPT.value
    return Passenger(person_name=person_name, items=items, approval_status=approval_status)


def check_passenger_status(approval_status: bool, passenger: Passenger):
    if approval_status != passenger.approval_status:
        expected_action = appconfig.EXPECTED_ACTION.ACCEPTED if passenger.approval_status else appconfig.EXPECTED_ACTION.REJECTED  # noqa: E501
        logging.error(f'"{passenger.person_name}" was not {expected_action}. Items: {passenger.items}')
    else:
        logging.log(msg=f'OK - "{passenger.person_name}"', level=logging.INFO)
