
import unittest
from unittest.mock import patch

from faker import Faker
from starlette.testclient import TestClient
from fastapi import HTTPException


from housing.api_models import PredictionRequest
from main import app


def get_faker(seed=1234):
    return Faker(seed)


def get_fake_data(value):
    fake = get_faker()
    type_data_generator_map = {
        "str": fake.pystr,
        "bool": fake.pybool,
        "int": fake.pyint,
        "float": fake.pyfloat
    }

    try:
        type_data_generator = type_data_generator_map[value.type_.__name__]
        return type_data_generator()
    except KeyError:
        raise


def generate_fake_prediction_data(exclude=None):
    exclude = exclude or []
    fake_prediction_data = {
        key: get_fake_data(value)
        for key, value in PredictionRequest.__fields__.items()
        if key not in exclude
    }

    return fake_prediction_data


test_client = TestClient(app)
fake = get_faker()
fake_price = fake.pyfloat()
fake_state = fake.pystr()


class TestRootEndpoint(unittest.TestCase):
    def setUp(self):
        self.endpoint = "/"

    def test_get_root(self):
        response = test_client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

class TestPredictEndpoint(unittest.TestCase):

    def setUp(self):
        self.endpoint = "/predict"

    @patch("main.predict_housing_price", return_value=fake_price)
    def test_post_predict(self, predict_func):
        request_data = generate_fake_prediction_data()
        prediction_request = PredictionRequest(**request_data)
        response = test_client.post(self.endpoint, json=request_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"price": fake_price})
        predict_func.assert_called_once_with(state=prediction_request.state, data=prediction_request.to_dict())

    @patch("main.predict_housing_price", return_value=fake_price)
    def test_post_predict_input_missing(self, predict_func):
        missing_parameter = "region"
        test_request_data = generate_fake_prediction_data(exclude=[missing_parameter])
        expected_response = {'loc': ['body', missing_parameter], 'msg': 'field required', 'type': 'value_error.missing'}
        response = test_client.post(self.endpoint, json=test_request_data)
        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(response.json()["detail"][0], expected_response)
        predict_func.assert_not_called()


class TestTrainEndpoint(unittest.TestCase):

    def setUp(self):
        self.endpoint = "/train"

    @patch("main.train_model_asynchronous", return_value=None)
    def test_post_train(self, train_func):
        response = test_client.post(self.endpoint, json={"state": fake_state})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        train_func.assert_called_once_with(fake_state)

    @patch("main.train_model_asynchronous", return_value=None)
    def test_post_train_fail(self, train_func):
        response = test_client.post(self.endpoint, json={"state": fake_state})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        train_func.assert_called_once_with(11)

    @patch("main.train_model_asynchronous", return_value=None, side_effect = HTTPException(status_code=400))
    def test_post_train_httpexception(self, train_func):
        response = test_client.post(self.endpoint, json={"state": fake_state})
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.json())
        train_func.assert_called_once_with(fake_state)