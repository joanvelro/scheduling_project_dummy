"""
.. module:: src.main
   :synopsis: TBD

.. moduleauthor:: (C) Capgemini Engineering - Hybrid Intelligence 2022
"""

from model_data_factory import ModelDataFactory
import os

from src.engine import SchedulerEngine

DATA_FILENAME = 'input_data_instance_v1.json'  # data for POL problem

request_path = os.path.join('..\\data', DATA_FILENAME)


if __name__ == "__main__":
    data = ModelDataFactory.create(request_path=request_path)
    engine = SchedulerEngine(data)
    engine.execute()
