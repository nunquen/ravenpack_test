"""
Disclaimer: There is no need to refactor this file, but you can modify it in order to integrate with your code
"""
import csv
from pathlib import Path

from cds.libs.utils import check_passenger_status, parse_passenger
from cds.service.customs_software import CustomsDetectorSoftware


CURRENT_DIRECTORY = Path(__file__).parent


if __name__ == "__main__":
    PASSENGER_MANIFEST_FILE = CURRENT_DIRECTORY.joinpath(
        "../passenger_manifest.csv"
    ).resolve(strict=True)

    cds = CustomsDetectorSoftware()

    with open(PASSENGER_MANIFEST_FILE, newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            passenger = parse_passenger(row)
            approval_status = cds.process_entry(passenger.items)
            check_passenger_status(approval_status, passenger)
