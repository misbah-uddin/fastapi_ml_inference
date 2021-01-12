
import random
from faker import Faker


def get_faker(seed=1234):
    return Faker(seed)


def load_model(model_selector):
    return None


def infer(model, data):
    return random.random()


def predict_housing_prices(model_selector: dict, inference_data: dict) -> dict:
    model = load_model(model_selector)
    response = {
        "model_selector": model_selector,
        "inference_data": inference_data,
        "inference_result": {"price": infer(model=model, data=inference_data)}}
    return response
