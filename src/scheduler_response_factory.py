"""
.. module:: src.scheduler_response_factory
   :synopsis: This class creates an instance of the Schedule Response class with the output of the scheduler engine

.. moduleauthor:: (C) Capgemini Engineering - Hybrid Intelligence 2022
"""

import traceback

from src.model_data import ModelData
from src.scheduler_response import SchedulerResponse


class SchedulerResponseFactory(object):
    """
           *Scheduler Response Factory*

           This class creates an instance of the Schedule Response class with the output of the scheduler engine.

              Attributes:
                  response:                     scheduler data class.

                  model:                        Scheduler engine class.

                  data:                         model data class.


       """

    def __init__(self, model, data: ModelData) -> None:
        self.response = SchedulerResponse()
        self.model = model
        self.data = data

    @staticmethod
    def create(model, data):
        """
        *Create*

        This method creates an instance of the schedule response data class with the solution provided by the engine
        scheduler.
         Attributes:
                  data:                 Receive the model data class of the schedule.
        """
        return SchedulerResponseFactory(model, data).__create()

    def __create(self):
        try:
            self.__build_solution_layout()
            self.__build_solution_schedule()
            self.__build_solution_cost_summary()

        except Exception as err:
            print("Error building scheduler response: {err}\n{traceback}".format(err=err,
                                                                                 traceback=traceback.format_exc()))
            self.response = None
            raise

        return self.response

    def __build_solution_layout(self):
        """
        *Build solution layout*

        This method ...
        """
        pass

    def __build_solution_schedule(self):
        """
        *Build solution schedule*

        This method ...
        """
        pass

    def __build_solution_cost_summary(self):
        """
        * Build solution cost summary*

        This method ...
        """
        pass
