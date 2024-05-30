from pydantic import BaseModel, validator
from typing import List

class PayloadModel(BaseModel):
    batchid: str
    payload: List[List[int]]

    @validator('payload')
    def payload_must_contain_integers(cls, v):
        if not all(isinstance(i, list) and all(isinstance(n, int) for n in i) for i in v):
            raise ValueError('Payload must be a list of lists of integers')
        return v
