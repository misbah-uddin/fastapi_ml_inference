
from fastapi import FastAPI
from api_models import PredictionRequest, PredictionResponse
from services import predict_housing_prices


app = FastAPI()


@app.post("/predict")
def predict(prediction_request: PredictionRequest):
    response = predict_housing_prices(**prediction_request.dict())
    print (response)
    prediction_response = PredictionResponse(**response)
    return prediction_response
