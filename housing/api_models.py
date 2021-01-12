
from pydantic import BaseModel, validator


VALID_STATE_NAMES = ["ak", "al", "ar", "ca", "fl", "mi", "ny"]


class PredictionRequest(BaseModel):
    state: str
    region: int
    type: int
    sqfeet: float
    beds: int
    baths: int
    cats_allowed: bool
    dogs_allowed: bool
    smoking_allowed: bool
    wheelchair_access: bool
    electric_vehicle_charge: bool
    comes_furnished: bool
    laundry_options: int
    parking_options: int
    lat: float
    long: float

    @validator('state')
    def state_must_be_valid(cls, value):
        if value not in VALID_STATE_NAMES:
            raise ValueError(f"{value} is not in valid state names")
        return value

    def to_dict(self):
        return {
            key: {0: getattr(self, key)}
            for key in self.__fields__.keys()
            if key != "state"
        }

class PredictionResponse(BaseModel):
    price: float


class TrainRequest(BaseModel):
    state: str

    @validator('state')
    def state_must_be_valid(cls, value):
        if value not in VALID_STATE_NAMES:
            raise ValueError(f"{value} is not in valid state names")
        return value