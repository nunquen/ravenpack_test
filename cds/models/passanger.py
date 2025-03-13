from pydantic import BaseModel
from typing import List


class Passenger(BaseModel):
    person_name: str
    items: List[str]
    approval_status: bool
