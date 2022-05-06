import json


class CreateData:

    def __init__(self, path):
        """
        Initializer

        :param: path: Path with the .json input file.
        """
        self.path = path

    def read_data(self, entry_type):
        """
        Function for reading and loading each main data category from the
        .json file

        :param: entry_type: Can be equal to 'equipment', 'recipes', 'workflow'
        or 'products'.
        """
        with open(self.path) as f:
            data_json = json.load(f)
            return data_json[entry_type]

    def get_unique_list_of_machines(self):
        """
        Function which returns the unique equipment list from the
        .json input file
        """
        equipment_data = self.read_data("equipment")
        list_of_machines = []
        for machine in equipment_data:
            list_of_machines.append(machine["name"])
        return list_of_machines

    def get_possible_workflow_graphs(self):
        workflow_data = self.read_data("workflow")
        equipment_data = self.read_data("equipment")
        dict_of_graph_list = {w["name"]: [] for w in workflow_data}
        for w in workflow_data:
            graph_dict = {tuple(k.split(";")): w["graph"][k]
                          for k in w["graph"]}

        return graph_dict

    def get_minimum_graph(self):
        recipe_data = self.read_data("recipes")
        list_of_machines = self.get_unique_list_of_machines()
        minimum_graph_list = []
        for recipe in recipe_data:
            minimum_graph = {(m, n): 0 for m in list_of_machines for n in
                             list_of_machines}
            for m in list_of_machines:
                for n in list_of_machines:
                    if recipe["equipment_list"].count(m) > 0 and \
                            recipe["equipment_list"].count(n) > 0:
                        if all(i[recipe["equipment_list"].index(m)][recipe["equipment_list"].index(n)] > 0 for i in
                               recipe["graph"]):
                            minimum_graph[m, n] = 1
            minimum_graph_list.append(minimum_graph)
        return minimum_graph_list


a = CreateData("../data/example.json")
print(a.get_possible_workflow_graphs())
