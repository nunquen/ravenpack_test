import pytest

from cds.service.customs_software import ask_universe
from cds.main import parse_passenger
from cds.service.customs_software import CustomsDetectorSoftware
from cds.adapters.file_adapter import read_storage


cds = CustomsDetectorSoftware()


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
        (
            "Bad cowbow,    Black Cowboy hAT, Smokes, Towel,                      REJECT",
            False,
            "> Rejecting Bad cowbow aand testing lower casing comparison",
        ),
    ]
)
def test_manifest(manifest, expected_valuation, description):
    items = manifest.split(",")
    passenger = parse_passenger(items)
    approval_status = cds.process_entry(passenger.items)
    assert approval_status == expected_valuation, description


@pytest.fixture
def get_dummy_file_path():
    yield "/this/is/a/dummy/file_path.txt"


def test_file_adapater(get_dummy_file_path):
    assert read_storage(file_path=get_dummy_file_path) == []
