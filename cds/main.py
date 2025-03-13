"""
Disclaimer: There is no need to refactor this file, but you can modify it in order to integrate with your code
"""
import csv
from pathlib import Path
from typing import List

from cds.config import appconfig
from cds.customs_software import CustomsDetectorSoftware
from cds.libs.utils import read_storage
from cds.models.passanger import Passenger


CURRENT_DIRECTORY = Path(__file__).parent


def parse_passenger(values: List[str]) -> Passenger:
    person_name = values[0].strip()
    items = [item.strip() for item in values[1:-1]]
    approval_status = values[-1].strip() == appconfig.DECISION.ACCEPT
    return Passenger(person_name=person_name, items=items, approval_status=approval_status)


def check_passenger_status(approval_status: bool, passenger: Passenger):
    if approval_status != passenger.approval_status:
        expected_action = appconfig.EXPECTED_ACTION.ACCEPTED if passenger.approval_status else appconfig.EXPECTED_ACTION.REJECTED  # noqa: E501
        print(f'ERROR - "{passenger.person_name}" was not {expected_action}. Items: {passenger.items}')
    else:
        print(f'OK - "{passenger.person_name}"')


if __name__ == "__main__":
    STORAGE_PATH = CURRENT_DIRECTORY.joinpath("../storage").resolve(strict=True)
    PASSENGER_MANIFEST_FILE = CURRENT_DIRECTORY.joinpath("../passenger_manifest.csv").resolve(strict=True)

    cds = CustomsDetectorSoftware(
        safe_items=read_storage(STORAGE_PATH.joinpath("safe.txt")),
        dangerous_items=read_storage(STORAGE_PATH.joinpath("dangerous.txt")),
    )

    with open(PASSENGER_MANIFEST_FILE, newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            passenger = parse_passenger(row)
            approval_status = cds.process_entry(passenger.items)
            check_passenger_status(approval_status, passenger)
