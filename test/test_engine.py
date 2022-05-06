"""
.. module:: test.test_engine
   :synopsis: TBD

.. moduleauthor:: (C) Capgemini Engineering - Hybrid Intelligence 2022
"""

import unittest

from src.model_data_factory import ModelDataFactory
from src.engine import SchedulerEngine


class EngineTest(unittest.TestCase):
    """
    *Engine Test*

    This class defines the unitary test for the engine scheduler


    """

    def test_engine(self):
        """
        *Test engine*

        Test scheduler engine with different input plant configurations. Check that the output schedule fulfill the
        expected functionalities.

        Input data instances:
                * example_test_1.json
                * example_test_2.json
                * example_test_3.json
        """
        filename = 'data/example_test.json'

        self.data = ModelDataFactory.create(request_path=filename)
        engine = SchedulerEngine(self.data)
        engine.execute()
        self.response = engine.get_response()

        self.__check_1()

    def __check_1(self):

        self.assertTrue(self.response is None, 'Error')
