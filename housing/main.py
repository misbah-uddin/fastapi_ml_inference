
from fastapi import FastAPI

from housing.api_models.models import PredictionRequest, PredictionResponse
from housing.services import predict_housing_price


app = FastAPI()


@app.post("/predict")
def predict_api(prediction_request: PredictionRequest):
    response = predict_housing_price(**prediction_request.dict())
    prediction_response = PredictionResponse(**response)
    return prediction_response
