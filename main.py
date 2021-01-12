
import threading

from fastapi import FastAPI, HTTPException
from housing.api_models import PredictionRequest, PredictionResponse, TrainRequest
from housing.services import predict_housing_price


app = FastAPI()


@app.post("/predict", response_model=PredictionResponse)
def predict(input: PredictionRequest):
    price = predict_housing_price(state=input.state, data=input.to_dict())
    response = PredictionResponse(price=price)
    return response
