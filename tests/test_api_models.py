
import unittest

import pydantic
from faker import Faker

from housing.api_models.models import ModelSelector
from housing.api_models.sample_data import get_sample_state, get_sample_season
from housing.api_models.parameters import *


PyDanticValidationError = pydantic.error_wrappers.ValidationError
fake = Faker(SEED)


class TestModelSelector(unittest.TestCase):
    def setUp(self):
        self.state = get_sample_state()
        self.season = get_sample_season()

    def test_model_selector_has_both_valid_state_and_season(self):
        model_selector = ModelSelector(state=self.state, season=self.season)
        self.assertEqual(model_selector.state, self.state)
        self.assertEqual(model_selector.season, self.season)

    def test_model_selector_has_invalid_state(self):
        with self.assertRaises(PyDanticValidationError):
            ModelSelector(state=fake.pystr(), season=self.season)

    def test_model_selector_has_invalid_season(self):
        with self.assertRaises(PyDanticValidationError):
            ModelSelector(state=self.state, season=fake.pystr())
