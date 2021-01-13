
import unittest
from unittest.mock import patch

from starlette.testclient import TestClient

from housing.api_models.models import InferenceResult, PredictionRequest, PredictionResponse
from housing.main import app
from housing.api_models.sample_data import get_sample_price, SampleData



sample_data = SampleData()
#sample_prediction_request = PredictionRequest(**sample_data.prediction_request)
#sample_prediction_response = PredictionResponse(**sample_data.prediction_response)


class TestPredictEndpoint(unittest.TestCase):

    def setUp(self):
        self.endpoint = "/predict"
        self.test_client = TestClient(app)

    @patch("housing.main.predict_housing_price", return_value=sample_data.prediction_response)
    def test_post_predict(self, predict_func):
        response = self.test_client.post(self.endpoint, json=sample_data.prediction_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), sample_data.prediction_response)
        predict_func.assert_called_once_with(**sample_data.prediction_request)

    @patch("housing.main.predict_housing_price", return_value=sample_data.prediction_response)
    def test_post_predict_input_missing(self, predict_func):
        missing_column = "inference_data"
        test_request_data = {
            missing_column: {"sqfeet": sample_data.price}, "model_selector": sample_data.model_selector
        }
        response = self.test_client.post(self.endpoint, json=test_request_data)
        self.assertEqual(response.status_code, 422)
        predict_func.assert_not_called()
