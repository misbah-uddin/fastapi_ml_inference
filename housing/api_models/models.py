
from pydantic import BaseModel, Field, PositiveInt, PositiveFloat, validator
from faker import Faker

from housing.api_models.parameters import *
from housing.api_models.sample_data import SampleData


sample_data = SampleData()


class ModelSelector(BaseModel):
    state: str
    season: str

    @validator("state")
    def state_must_be_valid(cls, value):
        if value not in VALID_STATE_NAMES:
            raise ValueError(f"{value} is not an acceptable state names")
        return value

    @validator("season")
    def season_must_be_valid(cls, value):
        if value not in VALID_SEASONS:
            raise ValueError(f"{value} is not an acceptable season")
        return value

    class Config:
        schema_extra = {"examples": [sample_data.model_selector]}


class InferenceData(BaseModel):
    sqfeet: float=Field(gte=0)
    beds: PositiveInt
    baths: PositiveInt
    pets_allowed: bool
    parking_included: bool
    latitude: float
    longitude: float

    class Config:
        schema_extra = {"examples": [sample_data.model_selector]}


class InferenceResult(BaseModel):
    price: PositiveFloat=Field(gte=MIN_PRICE, lte=MAX_PRICE)

    class Config:
        schema_extra = {"examples": [sample_data.inference_result]}


class PredictionRequest(BaseModel):
    model_selector: ModelSelector
    inference_data: InferenceData

    class Config:
        schema_extra = {"examples": [sample_data.prediction_request]}


class PredictionResponse(PredictionRequest):
    inference_result: InferenceResult

    class Config:
        schema_extra = {"examples": [sample_data.prediction_response]}
