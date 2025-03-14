from enum import Enum
import os


class AuthConfig:
    class EXPECTED_ACTION(Enum):
        ACCEPTED = 'ACCEPTED'
        REJECTED = 'REJECTED'

    class DECISION(Enum):
        ACCEPT = 'ACCEPT'
        REJECT = 'REJECT'

    UNIVERSE_MEANING = 42
    # Define the item provider here
    PROVIDER = os.environ.get("PROVIDER", "fileItem")


appconfig: AuthConfig = AuthConfig()
