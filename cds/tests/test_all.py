import pytest
from pathlib import Path

from cds.customs_software import ask_universe
from cds.main import parse_passenger, read_storage
from cds.customs_software import CustomsDetectorSoftware


CURRENT_DIRECTORY = Path(__file__).parent
# PASSENGER_MANIFEST = CURRENT_DIRECTORY.joinpath('../../passenger_manifest.csv').resolve(strict=True)
STORAGE_PATH = CURRENT_DIRECTORY.joinpath('../../storage/').resolve(strict=True)

cds = CustomsDetectorSoftware(
        safe_items=read_storage(STORAGE_PATH.joinpath("safe.txt")),
        dangerous_items=read_storage(STORAGE_PATH.joinpath("dangerous.txt")),
    )


def test_universe_fundamentals():
    """
    If this test fails: Please contact your test provider!
    """
    assert ask_universe('supercalifragilisticexpialidocious'),  "Good fundamental"
    assert not ask_universe('Incomprehensibilities Strengths'), "Bad fundamental"


@pytest.fixture
def good_characters_list():
    yield ["A", "a"]


def test_good_characters(good_characters_list):
    for good_characters in good_characters_list:
        assert ask_universe(good_characters), "Good characters"


@pytest.mark.parametrize(
    "manifest, expected_valuation, description", [
        (
            "Sandy Cheeks,     Candy, Space Suit, Towel, Toothpaste, Toothbrush,  ACCEPT",
            True,
            "> Accepting Sandy Cheeks",
        ),
        (
            "Spike Spiegel,    Space Cowboy Hat, Smokes, Towel,                   REJECT",
            False,
            "> Rejecting Spike Spiegel",
        ),
        (
            "Hyperactive Kid,  Water gun, Candy, Towel, Toothbrush,               REJECT",
            False,
            "> Rejecting Hyperactive Kid",
        ),
        (
            "Luna TikTok,      Camera, Selfie Stick,                              REJECT",
            False,
            "> Rejecting Luna TikTok",
        ),
        (
            "Clark Kent,       Towel, Cape, Glasses,                              ACCEPT",
            True,
            "> Accepting Clark Kent",
        ),
        (
            "Sam Bell,         Old Recordings, Towel, Glasses,                    REJECT",
            False,
            "> Rejecting Sam Bell",
        ),
        (
            "Saul Maldonado,   Paparoach Old Recordings, Towel, Glasses,          ACCEPT",
            True,
            "> Accepting Saul Maldonado",
        ),
    ]
)
def test_manifest(manifest, expected_valuation, description):
    items = manifest.split(",")
    passenger = parse_passenger(items)
    approval_status = cds.process_entry(passenger.items)
    assert approval_status == expected_valuation, description
