from enum import Enum


class AuthConfig:
    class EXPECTED_ACTION(Enum):
        ACCEPTED = 'ACCEPTED'
        REJECTED = 'REJECTED'

    class DECISION(Enum):
        ACCEPT = 'ACCEPT'
        REJECT = 'REJECT'

    UNIVERSE_MEANING = 42


appconfig: AuthConfig = AuthConfig()
