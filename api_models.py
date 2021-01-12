
from pydantic import BaseModel, validator


VALID_STATE_NAMES = ["ak", "al", "ar", "ca", "fl", "mi", "ny"]
VALID_SEASONS = ["202001", "202004", "202007", "202010", "202101"]


class ModelSelector(BaseModel):
    state: str
    season: str

    @validator('state')
    def state_must_be_valid(cls, value):
        if value not in VALID_STATE_NAMES:
            raise ValueError(f"{value} is not an acceptable state names")
        return value

    @validator('season')
    def season_must_be_valid(cls, value):
        if value not in VALID_SEASONS:
            raise ValueError(f"{value} is not an acceptable season")
        return value


class InferenceData(BaseModel):
    sqfeet: float
    beds: int
    baths: int
    pets_allowed: bool
    parking_included: bool
    latitude: float
    longitude: float


class InferenceResult(BaseModel):
    price: float


class PredictionRequest(BaseModel):
    model_selector: ModelSelector
    inference_data: InferenceData


class PredictionResponse(BaseModel):
    model_selector: ModelSelector
    inference_data: InferenceData
    inference_result: InferenceResult
