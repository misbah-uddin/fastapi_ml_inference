
import random
from faker import Faker
from unittest.mock import Mock

def get_faker(seed=1234):
    return Faker(seed)


def load_model(model_selector):
    model = Mock(model_selector)
    return model


def infer_price(model, inference_data):
    mock = Mock()
    mock.return_value = random.randint(1000, 2000)
    price = mock(model, inference_data)
    return price


def predict_housing_price(model_selector: dict, inference_data: dict) -> dict:
    model = load_model(model_selector)
    response = {
        "model_selector": model_selector,
        "inference_data": inference_data,
        "inference_result": {"price": infer_price(model=model, inference_data=inference_data)}}
    return response
