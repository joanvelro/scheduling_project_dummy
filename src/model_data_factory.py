"""
.. module:: src.model_data_factory
   :synopsis: TBD

.. moduleauthor:: (C) Capgemini Engineering - Hybrid Intelligence 2022
"""


import json
import time
import traceback

from pandas import read_excel


from src.model_data import ModelData


class ModelDataFactory(object):
    """
       *Model Data Factory*

       This class creates an instance of the Model data class with the input of the scheduler engine.

              Attributes:
                  request_path                 path or json file
                  data                         model data class

       """

    def __init__(self, request_path) -> None:
        self.request_path = request_path
        self.data = ModelData()

    @staticmethod
    def create(request_path):
        """
        *Create*

        This method creates an instance of the model data class with the input json file provided
         Attributes:
                  request_path:                 input json file
        """
        return ModelDataFactory(request_path).__create()

    def __create(self):
        try:
            print('\nBuilding data model...')
            start = time.time()

            self.__build_schedule_configs()
            self.__build_equipments()
            self.__build_workflows()
            self.__build_products()
            self.__build_demands()
            self.__build_cips()

            end = time.time()
            print('Done! It took {time} seconds\n'.format(time=round(end - start, 3)))

            return self.data

        except TypeError as err:
            print("Unexpected error: {err}\n{traceback}".format(err=err, traceback=traceback.format_exc()))
            raise

    def __build_schedule_configs(self):
        schedule_configs_list = self.__read_request_data(sheet_name='ScheduleConfig')
        self.data.set_schedule_configs(schedule_configs=schedule_configs_list)

    def __build_equipments(self):
        equipments_list = self.__read_request_data(sheet_name='Equipments')
        self.data.set_equipments(equipments=equipments_list)

    def __build_workflows(self):
        workflow_list = self.__read_request_data(sheet_name='WorkFlows')
        self.data.set_workflows(workflows=workflow_list)

    def __build_products(self):
        products_list = self.__read_request_data(sheet_name='Products')
        self.data.set_products(products=products_list)

    def __build_demands(self):
        demands_list = self.__read_request_data(sheet_name='Demands')
        self.data.set_demands(demands=demands_list)

    def __build_cips(self):
        cips_list = self.__read_request_data(sheet_name='CIPs')
        self.data.set_cips(cips=cips_list)

    def __read_request_data(self, sheet_name, use_cols=range(0, 1)):
        if self.request_path[-4:] == 'xlsx':
            return read_excel(io=self.request_path, sheet_name=sheet_name,
                              engine='openpyxl', usecols=use_cols).dropna()
        elif self.request_path[-4:] == 'json':
            with open(self.request_path, 'r') as f:
                data_json = json.load(f)
            return data_json[sheet_name]
