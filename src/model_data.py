"""
.. module:: src.model_data
   :synopsis: TBD

.. moduleauthor:: (C) Capgemini Engineering - Hybrid Intelligence 2022
"""


class ModelData(object):
    """
        *Model Data*

        This class defines the data model of the input instance. It contains the main attributes that the scheduler
        requires.It also contain the different methods required to work with the attributes.

               Attributes:
                   schedule_configs:     Dictionary that contain the schedule configuration:

                        objective:          objective to consider (1:makespan, 2:just-in-time). String.

                        product_order:      order of the products to be scheduled. List:

                        starting_date:      Starting date to consider in the schedule. Timestamp (dd-mm-yyyy hh:mm:ss).

                        max_time_horizon:   Max. number of days to consider in the schedule. Integer.

                        time_resolution:    Time resolution of the schedule (1-30 min). Integer

                        plant_ID:    Identifier for the plant configuration. It wil be used for the schedule_ID. String


                   equipment: Dictionary that contains the information of the equipment involved in the schedule.
                   Each register is a equipment.

                        equipment_ID: Identifier for the equipment.

                        no_inputs:  Number of inputs.

                        no_outputs: Number of outputs.

                        batch_max: Maximum batch size.

                        batch_min: Minimum batch size.

                        calendar: Equipment_calendar. Working horus. format: [24,7].

                   demand: Dictionary that contains the information of the product demand:

                        product_ID: Identifier for th product. Is a list.

                        due_data:   Dictionary that contain the due_date for each product.

                        amount: Dictionaty that contain the quantity demanded for each product
                   workflows: Dictionary that contains the information related to recipe/workflows:

                        workflow_ID:    Identifier for the workflow.

                        input_product:  Input product/s. [String].

                        output_product: Ouput product/s. [String].

                        recipe: Dictionary that contains the recipes (workflow graph)

                            node: Dictionary that contains:

                                node_ID

                                subprocess

                                duration_type

                                duration

                            edge:   Dictionary that contains:

                                node_origin_ID

                                node_destination_ID

                                subprocess_destination

                                subprocess_origin

                                product_origin

                                product_destination

                                flow_rate

                                delay

                                connection: Type of connection (SS, FF, FS, SF)



    """

    def __init__(self) -> None:
        self.__schedule_configs = []
        self.__equipments = []
        self.__workflows = []
        self.__products = []
        self.__demands = []
        self.__cips = []

    def set_schedule_configs(self, schedule_configs):
        self.__schedule_configs = schedule_configs

    def set_equipments(self, equipments):
        self.__equipments = equipments

    def set_workflows(self, workflows):
        self.__workflows = workflows

    def set_products(self, products):
        self.__products = products

    def set_demands(self, demands):
        self.__demands = demands

    def set_cips(self, cips):
        self.__cips = cips

    def get_schedule_configs(self):
        return self.__schedule_configs

    def get_equipments(self):
        return self.__equipments

    def get_workflows(self):
        return self.__workflows

    def get_products(self):
        return self.__products

    def get_demands(self):
        return self.__demands

    def get_cips(self):
        return self.__cips
