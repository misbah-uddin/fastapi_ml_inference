
from fastapi import FastAPI
from housing.api_models import PredictionRequest, PredictionResponse
from housing.services import predict_housing_prices


app = FastAPI()


@app.post("/predict")
def predict(prediction_request: PredictionRequest):
    response = predict_housing_prices(**prediction_request.dict())
    prediction_response = PredictionResponse(**response)
    return prediction_response
