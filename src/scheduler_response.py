
class SchedulerResponse(object):
    """
    *SchedulerResponse*

    solution_schedule: Dict (key1, key2, key3) Definition
    solution_schedule: Dict (key1, key2, key3) Definition
    solution_schedule: Dict (key1, key2, key3) Definition
    solution_schedule: Dict (key1, key2, key3) Definition

    """

    def __init__(self) -> None:
        self.__solution_schedule = None
        self.__solution_equipment = None
        self.__solution_cip = None
        self.__solution_cost_summary = None

    def get_solution_cost_summary(self):
        return self.__solution_cost_summary

    def set_solution_cost_summary(self, cost_summary):
        self.__solution_cost_summary = cost_summary
