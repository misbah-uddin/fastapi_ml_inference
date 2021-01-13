

from faker import Faker
from random import choice
from dataclasses import dataclass, field

from housing.api_models import parameters


def get_sample_state():
    return choice(parameters.VALID_STATE_NAMES)


def get_sample_season():
    return choice(parameters.VALID_SEASONS)


def get_sample_price(seed: int = parameters.SEED):
    fake = Faker(seed)
    return fake.pyfloat(min_value=parameters.MIN_PRICE, max_value=parameters.MAX_PRICE)


def get_sample_inference_data(seed=parameters.SEED):
    fake = Faker(seed)
    inference_data = {
        "sqfeet": fake.pyfloat(min_value=0),
        "beds": fake.pyint(min_value=1),
        "baths": fake.pyint(min_value=1),
        "pets_allowed": fake.pybool(),
        "parking_included": fake.pybool(),
        "latitude": fake.pyfloat(),
        "longitude": fake.pyfloat()
    }

    return inference_data


@dataclass
class SampleData:
    inference_result: dict=None
    prediction_request: dict=None
    prediction_response: dict=None
    state: float=field(default_factory=get_sample_state)
    season: float=field(default_factory=get_sample_season)
    price: float=field(default_factory=get_sample_price)
    inference_data: dict=field(default_factory=get_sample_inference_data)

    def __post_init__(self):
        self.model_selector = self.get_sample_model_selector(state=self.state, season=self.season)
        self.inference_result = self.get_sample_inference_response(self.price)
        self.prediction_request = self.get_sample_prediction_request(model_selector=self.model_selector,
                                                                     inference_data=self.inference_data)
        self.prediction_response = self.get_sample_prediction_response(model_selector=self.model_selector,
                                                                       inference_data=self.inference_data,
                                                                       inference_result=self.inference_result)

    @classmethod
    def get_sample_state(cls):
        return choice(parameters.VALID_STATE_NAMES)

    @classmethod
    def get_sample_season(cls):
        return choice(parameters.VALID_SEASONS)

    @classmethod
    def get_sample_model_selector(cls, state, season):
        return {"state": state, "season": season}

    @classmethod
    def get_sample_inference_response(cls, price):
        return {"price": price}

    @classmethod
    def get_sample_prediction_request(cls, model_selector, inference_data):
        return {
            "model_selector": model_selector,
            "inference_data": inference_data
        }

    @classmethod
    def get_sample_prediction_response(cls, model_selector, inference_data, inference_result):
        return {
            "model_selector": model_selector,
            "inference_data": inference_data,
            "inference_result": inference_result
        }
