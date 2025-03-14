"""AuthConfig Module

This module defines the AuthConfig class, which includes enumerations for expected actions
and decisions, as well as configuration constants related to the authentication process.
"""

from enum import Enum
import os


class AuthConfig:
    """
    AuthConfig Class

    A configuration class that contains enumerations for expected actions and decisions,
    along with constants for universe meaning and the item provider.

    Attributes:
        EXPECTED_ACTION (Enum): Enumeration for expected actions (ACCEPTED, REJECTED).
        DECISION (Enum): Enumeration for decisions (ACCEPT, REJECT).
        UNIVERSE_MEANING (int): Constant representing the meaning of the universe.
        PROVIDER (str): The item provider, determined by the 'PROVIDER' environment variable.
    """

    class EXPECTED_ACTION(Enum):
        """
        EXPECTED_ACTION Enum

        Enumeration representing the expected actions in the authentication process.

        Attributes:
            ACCEPTED (str): Represents an accepted action.
            REJECTED (str): Represents a rejected action.
        """

        ACCEPTED = "ACCEPTED"
        REJECTED = "REJECTED"

    class DECISION(Enum):
        """
        DECISION Enum

        Enumeration representing possible decisions in the authentication process.

        Attributes:
            ACCEPT (str): Represents an acceptance decision.
            REJECT (str): Represents a rejection decision.
        """

        ACCEPT = "ACCEPT"
        REJECT = "REJECT"

    UNIVERSE_MEANING = 42
    """
    UNIVERSE_MEANING int

    Constant representing the meaning of the universe. Used as a base value in certain computations.
    """

    PROVIDER = os.environ.get("PROVIDER", "fileItem")
    """
    PROVIDER str

    The item provider, determined by the 'PROVIDER' environment variable. Defaults to 'fileItem' if not set.
    """


# Instantiate the appconfig object
appconfig: AuthConfig = AuthConfig()
