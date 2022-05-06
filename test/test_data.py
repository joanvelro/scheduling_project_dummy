"""
.. module:: test.test_data
   :synopsis: TBD

.. moduleauthor:: (C) Capgemini Engineering - Hybrid Intelligence 2022
"""

import logging
import os
import unittest

import src.model_data_factory
from src.utils import initialize_logger, list_to_reason

path_logger = os.path.join(os.path.dirname(__file__), '..//reports//logs//')
logger_object = initialize_logger(path_logger + 'test_data_log')


class DataTest(unittest.TestCase):
    """
    *Data Test*

    This class defines the unitary test for the input data instance of scheduler


    """

    def __tearDown(self):
        """
        *Tear Down*

        It evaluates the result of the current test and  if error or failure occurs a message is logged.
        """
        # get test result
        if hasattr(self, '_outcome'):  # python 3.4+
            result = self.defaultTestResult()
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)

        error = self.list_to_reason(result.errors)
        failure = self.list_to_reason(result.failures)
        ok = not error and not failure

        # report error / failure
        if not ok:
            _, text = ('ERROR', error) if error else ('FAIL', failure)
            message = [x for x in text.split('\n')[1:] if not x.startswith(' ')][0]
            logger_object.info('Test failed! ' + message)

    def test_data_input(self):
        """
        *Test Data Input*

        Test if some input data instances are feasible plant configuration for the scheduler engine

        Input data instances:
                * example_test_1.json
                * example_test_2.json
                * example_test_3.json
        """

        data_filename = 'data/example_test.json'

        self.data = src.model_data_factory.ModelDataFactory.create(request_path=data_filename)

        #############################################
        # Schedule configuration data entry methods
        #############################################
        self.schedule_config = self.data.get_schedule_configs()
        self.schedule_config_expected_dict_keys = ['objective', 'product_order', 'plant_calendar',
                                                   'starting_date', 'max_time_horizon']
        self.schedule_config_expected_dict_keys_type = [str, list, str, str, str]
        self.schedule_config_product_order_expected_items_type = str

        logger_object.info('Checking that the schedule configurations come in a list...')
        self.__check_schedule_config_is_list()
        logger_object.info('OK!')

        logger_object.info('Checking the number of schedule configurations...')
        self.__check_number_of_schedule_config()
        logger_object.info('OK!')

        logger_object.info('Checking that the list of schedule configurations contains only dictionaries...')
        for i in range(0, len(self.schedule_config)):  # run through all elements in the list of schedule config
            self.__check_schedule_config_type(i)
        logger_object.info('OK!')

        logger_object.info('Checking that the dictionaries in schedule configurations have the expected keys...')
        for i in range(0, len(self.schedule_config)):  # run through all elements in the list of schedule config
            self.__check_schedule_config_dict_keys(i)
        logger_object.info('OK!')

        logger_object.info('Checking that all values in the schedule configurations dictionaries are not empty...')
        for i in range(0, len(self.schedule_config)):  # run through all elements in the list of schedule config
            # run through all keys in the current dict (schedule config)
            for key in self.schedule_config_expected_dict_keys:
                # values in the dictionary (schedule config) can be strings or lists
                if isinstance(self.schedule_config[i][key], list):
                    self.__check_not_empty_values_in_list(self.schedule_config[i][key])
                else:
                    self.__check_not_empty_value(self.schedule_config[i][key])
        logger_object.info('OK!')

        logger_object.info('Checking that the dictionaries in schedule configurations '
                           'have the expected type of values...')
        for i in range(0, len(self.schedule_config)):  # run through all elements in the list of schedule config
            # run through all keys in the current dict (schedule config)
            for key in range(0, len(self.schedule_config_expected_dict_keys)):
                self.__check_schedule_config_dict_values_type(i, key)
        logger_object.info('OK!')

        logger_object.info('Checking that the product order list in schedule configurations has only strings...')
        for i in range(0, len(self.schedule_config)):  # run through all elements in the list of schedule config
            self.__check_schedule_config_product_order_type(i)
        logger_object.info('OK!')

        #############################################
        # Equipments data entry methods
        #############################################
        self.equipments = self.data.get_equipments()
        self.equipments_expected_dict_keys = ['name', 'id', 'input', 'output',
                                              'volume', 'volume_to_empty', 'subprocess']
        self.equipments_expected_dict_keys_type = [str, str, int, int, int, int, list]
        self.equipments_subprocess_expected_items_type = str

        logger_object.info('Checking that the equipments come in a list...')
        self.__check_equipments_is_list()
        logger_object.info('OK!')

        logger_object.info('Checking the number of equipments...')
        self.__check_number_of_equipments()
        logger_object.info('OK!')

        logger_object.info('Checking that the list of equipments contains only dictionaries...')
        for i in range(0, len(self.equipments)):  # run through all elements in the list of equipments
            self.__check_equipments_type(i)
        logger_object.info('OK!')

        logger_object.info('Checking that the dictionaries in equipments have the expected keys...')
        for i in range(0, len(self.equipments)):  # run through all elements in the list of equipments
            self.__check_equipments_dict_keys(i)
        logger_object.info('OK!')

        logger_object.info('Checking that all values in the equipments dictionaries are not empty...')
        for i in range(0, len(self.equipments)):  # run through all elements in the list of equipments
            # run through all keys in the current dict (equipment)
            for key in self.equipments_expected_dict_keys:
                # values in the dictionary (equipment) can be strings, lists or integers
                if isinstance(self.equipments[i][key], list):
                    self.__check_not_empty_values_in_list(self.equipments[i][key])
                else:
                    self.__check_not_empty_value(self.equipments[i][key])
        logger_object.info('OK!')

        logger_object.info('Checking that the dictionaries in equipments have the expected type of values...')
        for i in range(0, len(self.equipments)):  # run through all elements in the list of equipments
            # run through all keys in the current dict (equipment)
            for key in range(0, len(self.equipments_expected_dict_keys)):
                self.__check_equipments_dict_values_type(i, key)
        logger_object.info('OK!')

        logger_object.info('Checking that the subprocess list in equipments has only strings...')
        for i in range(0, len(self.equipments)):  # run through all elements in the list of equipments
            self.__check_equipments_subprocess_type(i)
        logger_object.info('OK!')

        #############################################
        # Workflows data entry methods
        #############################################
        self.workflows = self.data.get_workflow_graph()

        logger_object.info('Checking that the workflows come in a list...')
        self.__check_workflows_is_list()
        logger_object.info('OK!')
        logger_object.info('Checking the number of workflows...')
        self.__check_number_of_workflows()
        logger_object.info('OK!')
        logger_object.info('Checking that the list of workflows contains only dictionaries...')
        for i in range(0, len(self.workflows)):
            self.__check_workflows_type(i)
        logger_object.info('OK!')

        #############################################
        # Products data entry methods
        #############################################
        self.products = self.data.get_products()

        logger_object.info('Checking that the products come in a list...')
        self.__check_products_is_list()
        logger_object.info('OK!')
        logger_object.info('Checking the number of products...')
        self.__check_number_of_products()
        logger_object.info('OK!')
        logger_object.info('Checking that the list of products contains only dictionaries...')
        for i in range(0, len(self.products)):
            self.__check_products_type(i)
        logger_object.info('OK!')

        #############################################
        # Demands data entry methods
        #############################################
        self.demands = self.data.get_demands()
        self.demands_expected_dict_keys = ['product_name', 'product_id', 'due_date', 'amount']
        self.demands_expected_dict_keys_type = [str, int, str, int]

        logger_object.info('Checking that the demands come in a list...')
        self.__check_demands_is_list()
        logger_object.info('OK!')
        logger_object.info('Checking the number of demands...')
        self.__check_number_of_demands()
        logger_object.info('OK!')
        logger_object.info('Checking that the list of demands contains only dictionaries...')
        for i in range(0, len(self.demands)):  # run through all elements in the list of demands
            self.__check_demands_type(i)
        logger_object.info('OK!')

        logger_object.info('Checking that the dictionaries in demands have the expected keys...')
        for i in range(0, len(self.demands)):  # run through all elements in the list of demands
            self.__check_demands_dict_keys(i)
        logger_object.info('OK!')

        logger_object.info('Checking that all values in the demands dictionaries are not empty...')
        for i in range(0, len(self.demands)):  # run through all elements in the list of demands
            # run through all keys in the current dict (demand)
            for key in self.demands_expected_dict_keys:
                # values in the dictionary (demand) can be strings or ints
                self.__check_not_empty_value(self.demands[i][key])
        logger_object.info('OK!')

        logger_object.info('Checking that the dictionaries in demands have the expected type of values...')
        for i in range(0, len(self.demands)):  # run through all elements in the list of demands
            # run through all keys in the current dict (demand)
            for key in range(0, len(self.demands_expected_dict_keys)):
                self.__check_demands_dict_values_type(i, key)
        logger_object.info('OK!')

        #############################################
        # CIPs data entry methods
        #############################################
        self.cips = self.data.get_cips()

        logger_object.info('Checking that the CIPs come in a list...')
        self.__check_cips_is_list()
        logger_object.info('OK!')
        logger_object.info('Checking the number of CIPs...')
        self.__check_number_of_cips()
        logger_object.info('OK!')
        logger_object.info('Checking that the list of CIPs contains only dictionaries...')
        for i in range(0, len(self.cips)):
            self.__check_cips_type(i)
        logger_object.info('OK!')

        logger_object.info('All tests passed!')

    def __check_schedule_config_is_list(self):
        """
        *check schedule config is list*
        Test...
        """

        self.assertEqual(type(self.schedule_config), list)

    def __check_number_of_schedule_config(self):
        """
        *Check the number of schedule configurations*
        """

        self.assertTrue(len(self.schedule_config) == 1)

    def __check_schedule_config_type(self, i):
        """
        *Check schedule config*
        CHeck that the list of schedule configurations contains data of type dict
        """

        self.assertEqual(type(self.schedule_config[i]), dict)

    def __check_schedule_config_dict_keys(self, i):
        """
        *check schedule config dict keys*
        Check that the dictionaries in the schedule configurations list have the expected keys
        """

        self.assertTrue(all(key in self.schedule_config[i]
                            for key in self.schedule_config_expected_dict_keys))

    def __check_schedule_config_dict_values_type(self, i, j):
        """
        *check schedule config dict values type*
        Check that the dictionaries in schedule configurations have the expected type of values
        """

        self.assertEqual(type(self.schedule_config[i][self.schedule_config_expected_dict_keys[j]]),
                         self.schedule_config_expected_dict_keys_type[j])

    def __check_schedule_config_product_order_type(self, i):
        """
        **Check product order type*
        Check that the product order list in schedule configurations has only strings
        """

        self.assertTrue(all(isinstance(item, self.schedule_config_product_order_expected_items_type)
                            for item in self.schedule_config[i]['product_order']))

    def __check_equipments_is_list(self):
        """
        Check that the equipments come in a list
        """

        self.assertEqual(type(self.equipments), list)

    def __check_number_of_equipments(self):
        """
        Check the number of equipments
        """

        self.assertTrue(len(self.equipments) == 3)

    def __check_equipments_type(self, i):
        """
        Check that the list of equipments contains data of type dict
        """

        self.assertEqual(type(self.equipments[i]), dict)

    def __check_equipments_dict_keys(self, i):
        """
        Check that the dictionaries in the equipments list have the expected keys
        """

        self.assertTrue(all(key in self.equipments[i]
                            for key in self.equipments_expected_dict_keys))

    def __check_equipments_dict_values_type(self, i, j):
        """
        Check that the dictionaries in equipments have the expected type of values
        """

        self.assertEqual(type(self.equipments[i][self.equipments_expected_dict_keys[j]]),
                         self.equipments_expected_dict_keys_type[j])

    def __check_equipments_subprocess_type(self, i):
        """
        Check that the subprocess list in equipments has only strings
        """

        self.assertTrue(all(isinstance(item, self.equipments_subprocess_expected_items_type)
                            for item in self.equipments[i]['subprocess']))

    def __check_workflows_is_list(self):
        """
        Check that the workflows come in a list
        """

        self.assertEqual(type(self.workflows), list)

    def __check_number_of_workflows(self):
        """
        Check the number of workflows
        """

        self.assertTrue(len(self.workflows) == 1)

    def __check_workflows_type(self, i):
        """
        Check that the list of workflows contains data of type dict
        """

        self.assertEqual(type(self.workflows[i]), dict)

    def __check_products_is_list(self):
        """
        Check that the products come in a list
        """

        self.assertEqual(type(self.products), list)

    def __check_number_of_products(self):
        """
        Check the number of products
        """

        self.assertTrue(len(self.products) == 2)

    def __check_products_type(self, i):
        """
        Check that the list of products contains data of type dict
        """

        self.assertEqual(type(self.products[i]), dict)

    def __check_demands_is_list(self):
        """
        Check that the demands come in a list
        """

        self.assertEqual(type(self.demands), list)

    def __check_number_of_demands(self):
        """
        Check the number of demands
        """

        self.assertTrue(len(self.demands) == 1)

    def __check_demands_type(self, i):
        """
        Check that the list of demands contains data of type dict
        """

        self.assertEqual(type(self.demands[i]), dict)

    def __check_demands_dict_keys(self, i):
        """
        Check that the dictionaries in the demands list have the expected keys
        """

        self.assertTrue(all(key in self.demands[i]
                            for key in self.demands_expected_dict_keys))

    def __check_demands_dict_values_type(self, i, j):
        """
        Check that the dictionaries in demands have the expected type of values
        """

        self.assertEqual(type(self.demands[i][self.demands_expected_dict_keys[j]]),
                         self.demands_expected_dict_keys_type[j])

    def __check_cips_is_list(self):
        """
        Check that the CIPs come in a list
        """

        self.assertEqual(type(self.cips), list)

    def __check_number_of_cips(self):
        """
        Check the number of CIPs
        """

        self.assertTrue(len(self.cips) == 2)

    def __check_cips_type(self, i):
        """
        Check that the list of CIPs contains data of type dict
        """

        self.assertEqual(type(self.cips[i]), dict)

    def __check_not_empty_value(self, value):
        """
        Check that a value is not empty
        """

        self.assertTrue(value)

    def __check_not_empty_values_in_list(self, list_of_values):
        """
        Check that a list has no empty items
        """

        self.assertTrue(all(value for value in list_of_values))

    def test_connectivity(self):
        """
        *Test Connectivity of the plant configuration*

        Test if the equipment of the plant configuration is connected to the rest of the equipment of the workflow
        """

    def test_consistency(self):
        """
        *Test consistency of the workflows*

        Test if the workflows defined are consistent
        """

    def test_feasible_time_horizon(self):
        """
        *Test feasible time horizon*

        Test if the time horizon provided is feasible to allocate the longest schedule
        """