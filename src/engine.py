"""
.. module:: src.engine
   :synopsis: This class defines the scheduler optimization engine.

.. moduleauthor:: (C) Capgemini Engineering - Hybrid Intelligence 2022
"""

import logging
import shutil
import sys
import os.path
import traceback
import time
import numpy as np

from ortools.sat.python import cp_model

from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib as mpl

from src.model_data import ModelData
from src.model_data_factory import ModelDataFactory
from src.scheduler_response_factory import SchedulerResponseFactory
from src.constants import EPSILON, PRECISION


class SchedulerEngine(object):
    """
        *Scheduler Engine*

        This class defines the scheduler optimization engine.

              Attributes:
                  results:     Results of the pyomo execution.

                  name:        Name of the model.

                  data:        Model data instance.

                  response:    Scheduler instance.
              """

    def __init__(self, data: ModelData) -> None:
        self.data = data
        self.model = cp_model.CpModel()
        self.results = None
        self.response = None

    def execute(self):
        """
        *Execute*

        This method execute the engine module which comprise the following sub-methods:

            * Data Analyzer: Check the integrity of the input data instance.

            * Build Model: Build the engine scheduler model.

            * Solve: Solve the optimziation model.

            * Build Solution: Invoke the scheduler data factory to build the schedule output solution
        """
        try:
            self.__check_data()
            self.__build_model()
            self.__solve()
            self.__build_solution()
            print('\nScheduling completed!')

        except Exception:
            print('There was an error running the Scheduling engine')

    def __check_data(self):
        """
        check data integrity
        """
        try:
            self.__check_data_method_1()
        except Exception as err:
            print("Data error: {err}".format(err=err))
            self.data = None
            raise

    def __solve(self):
        """
        solve model
        """
        try:
            print('Solving Scheduling...')

        except Exception as err:
            print(
                "Error Solving Scheduling: {err}\n{traceback}".format(err=err,
                                                                      traceback=traceback.format_exc()))
            self.results = None
            raise

    def __build_solution(self):
        self.response = SchedulerResponseFactory.create(
            self.model) if self.__has_solution() else None

    def __build_model(self):
        print('Building Scheduler model...')
        start = 0
        try:
            self.__build_batches()
            self.__build_sets()
            self.__build_parameters()
            self.__build_variables()
            self.__build_expressions()
            self.__build_constraints()
            self.__build_objective()

        except Exception as err:
            print(
                "Error building Scheduler model: {err}\n{traceback}".format(
                    err=err, traceback=traceback.format_exc()))
            self.model = None
            raise

        end = time.time()
        print('done! It took {time} seconds\n'.format(
            time=round(end - start, 3)))

    def __build_batches(self):
        demands = self.data.get_demands()
        equipments = self.data.get_equipments()
        workflows = self.data.get_workflows()

        self.B_min = {(k, j['product_name']): d['min_volume']
                      for i in workflows for k in i['equipments'] for j in
                      demands for d in equipments if d['name'] in k
                      }

        self.B_max = {(k, j['product_name']): d['max_volume']
                      for i in workflows for k in i['equipments'] for j in
                      demands for d in equipments if d['name'] in k
                      }
        lower_bound = {j['product_name']: np.ceil(j['amount'] /
                                                  max((k1, v) for (k1, k2), v
                                                      in self.B_max.items()
                                                      if
                                                      k2 == j['product_name'])[
                                                      1]) for j in demands}
        upper_bound = {j['product_name']: np.ceil(j['amount'] /
                                                  min((k1, v) for (k1, k2), v
                                                      in self.B_min.items()
                                                      if
                                                      k2 == j['product_name'])[
                                                      1]) for j in demands}
        # EN EL UPPER BOUND VA A HABER PROBLEMAS SI EL MINIMO ES 0, HAY QUE
        # AÑADIR ALGUNA EXCEPCIÓN.

        self.N = {j['product_name']:
                      int(np.ceil((upper_bound[j['product_name']] +
                                   lower_bound[j['product_name']]) / 2)) for j in
                  demands}
        self.demand_amounts = {j['product_name']:
                                   j['amount'] for j in demands}
        print(self.demand_amounts)

    def __build_sets(self):
        """
        Los índices en principio son sobre los subprocesos, sobre los batches, 
        sobre los productos y workflows
        """
        equipments = self.data.get_equipments()
        workflows = self.data.get_workflows()
        products = self.data.get_products()
        demands = self.data.get_demands()
        cips = self.data.get_cips()

        self.model.SUBPROCESS = [(i['name'], j) for i in equipments
                                 for j in i['subprocess']]
        self.model.OUTPUT_PRODUCTS = [i['product_name'] for i in demands]
        self.model.BATCHES = range(sum(self.N.values()))
        # Workflows y output products son 1:1 en este modelo V0

    def __build_parameters(self):
        workflows = self.data.get_workflows()
        equipments = self.data.get_equipments()
        self.time_horizon = int(1e6)
        self.time_start = 0

        # Volumen de un batch del producto p
        self.model.V = {p: int(np.ceil(self.demand_amounts[p] / self.N[p]))
                        for p in self.model.OUTPUT_PRODUCTS}

        # Volumen maximo del subproceso j
        self.model.MAX_V = {(i['name'], j): i['max_volume']
                            for i in equipments for j in i['subprocess']}

        # Duración del subproceso
        self.model.D_SUBPROCESS = {(p, m): 0
                                   for p in self.model.OUTPUT_PRODUCTS
                                   for m in self.model.SUBPROCESS}
        for p in workflows:
            for n in p['nodes']:
                if n['duration_type'] == 'variable':
                    self.model.D_SUBPROCESS[p['output_product'][0], (
                        n['name'], n['subprocess'])] = self.model.NewIntVar(
                        self.time_start, self.time_horizon, '')
                if n['duration_type'] == 'fixed':
                    self.model.D_SUBPROCESS[p['output_product'][0],
                                            (n['name'], n['subprocess'])] = n['duration']

        # Duracion de la conexión del subproceso m a n
        self.model.D_CONNECTIONS = {(p, m, n): 0
                                    for p in self.model.OUTPUT_PRODUCTS
                                    for m in self.model.SUBPROCESS
                                    for n in self.model.SUBPROCESS}

        for p in workflows:
            for n in p['edges']:
                if n['flow']:
                    self.model.D_CONNECTIONS[p['output_product'][0],
                                             (n['name_origin'], n['subprocess_origin']),
                                             (n['name_destination'], n['subprocess_destination'])] = \
                        int(np.ceil(self.model.V[p['output_product'][0]] / n['flowrate']))
                    # TRABAJA SOBRE LOS ENTEROS, ESTO DA PROBLEMAS
                if not n['flow']:
                    self.model.D_CONNECTIONS[p['output_product'][0],
                                             (n['name_origin'], n['subprocess_origin']),
                                             (n['name_destination'], n['subprocess_destination'])] = 0

        # Delay de la conexión de m a n
        self.model.R = {(p, m, n): 0
                        for p in self.model.OUTPUT_PRODUCTS
                        for m in self.model.SUBPROCESS
                        for n in self.model.SUBPROCESS}

        for p in workflows:
            for n in p['edges']:
                self.model.R[p['output_product'][0],
                             (n['name_origin'],
                              n['subprocess_origin']),
                             (n['name_destination'],
                              n['subprocess_destination'])] = n['delay']

        # Grafo de dependencias
        self.model.G = {(p, m, n): None
                        for p in self.model.OUTPUT_PRODUCTS
                        for m in self.model.SUBPROCESS
                        for n in self.model.SUBPROCESS}

        for p in workflows:
            for n in p['edges']:
                self.model.G[p['output_product'][0],
                             (n['name_origin'],
                              n['subprocess_origin']),
                             (n['name_destination'],
                              n['subprocess_destination'])] = n['connection']

        # Matriz que indica si 2 subprocesos son del mismo equipo
        self.model.P = {(m, n): 1 if m[0] == n[0] else 0
                        for m in self.model.SUBPROCESS
                        for n in self.model.SUBPROCESS}

    def __build_variables(self):
        # Indica a que producto pertenece el batch i
        self.model.A = {(i, p): self.model.NewBoolVar('')
                        for i in self.model.BATCHES
                        for p in self.model.OUTPUT_PRODUCTS}

        # Variable de inicio de subproceso
        self.model.S = {(i, n): self.model.NewIntVar(self.time_start,
                                                     self.time_horizon, '')
                        for i in self.model.BATCHES
                        for n in self.model.SUBPROCESS}

        # Variable de fin de subproceso
        self.model.E = {(i, n): self.model.NewIntVar(self.time_start,
                                                     self.time_horizon, '')
                        for i in self.model.BATCHES
                        for n in self.model.SUBPROCESS}

        # Variable indicadora
        self.model.D_I = {(i, n): self.model.NewIntVar(self.time_start,
                                                       self.time_horizon, '')
                          for i in self.model.BATCHES
                          for n in self.model.SUBPROCESS}

        # Variable de duración máxima de un batch
        self.model.D_MAX = {(i, n): self.model.NewIntVar(self.time_start,
                                                         self.time_horizon, '')
                            for i in self.model.BATCHES
                            for n in self.model.SUBPROCESS}

        # Variable de intervalo de batches
        self.model.B = {(i, n): self.model.NewIntervalVar(self.model.S[i, n],
                                                          self.model.D_MAX[i, n],
                                                          self.model.E[i, n],
                                                          '')
                        for i in self.model.BATCHES
                        for n in self.model.SUBPROCESS}

        # Variable que transforma de volumen por producto a volumen por indice de batch
        self.model.V_FROM_P_TO_I = {i: self.model.NewIntVar(0,
                                                            max(self.model.V.values()), '')
                                    for i in self.model.BATCHES}

        # Variable que indica donde puede empezar el volumen
        self.model.V_START = {(i, n): self.model.NewIntVar(0,
                                                           self.model.MAX_V[n], '')
                              for i in self.model.BATCHES
                              for n in self.model.SUBPROCESS}

        # Variable que indica donde puede acabar el volumen
        self.model.V_END = {(i, n): self.model.NewIntVar(
            0, self.model.MAX_V[n], '')
            for i in self.model.BATCHES
            for n in self.model.SUBPROCESS}

        # Variable de intervalo del volumen
        self.model.V_INTERVAL = {(i, n): self.model.NewIntervalVar(
            self.model.V_START[i, n],
            self.model.V_FROM_P_TO_I[i],
            self.model.V_END[i, n], '')
            for i in self.model.BATCHES
            for n in self.model.SUBPROCESS}

        # Variable indicadora
        self.model.A_I = {(i, j, p): self.model.NewBoolVar('')
                          for i in self.model.BATCHES
                          for j in self.model.BATCHES
                          for p in self.model.OUTPUT_PRODUCTS}

    def __build_expressions(self):
        print('build expressions')

    def __build_constraints(self):
        """"
        Agrupar todos los bucles posibles para mejorar performance.
        """
        for i in self.model.BATCHES:
            self.model.Add(sum(self.model.A[i, p] for p in
                               self.model.OUTPUT_PRODUCTS) == 1)

        for p in self.model.OUTPUT_PRODUCTS:
            self.model.Add(sum(self.model.A[i, p] for i in
                               self.model.BATCHES) == self.N[p])

        for i in self.model.BATCHES:
            for m in self.model.SUBPROCESS:
                for p in self.model.OUTPUT_PRODUCTS:
                    self.model.AddMaxEquality(self.model.D_I[i, m],
                                              [self.model.D_CONNECTIONS[p, m, l]
                                               for l in self.model.SUBPROCESS])
                    self.model.Add(self.model.D_MAX[i, m] ==
                                   self.model.D_I[i, m]).OnlyEnforceIf(self.model.A[i, p])

        for i in self.model.BATCHES:
            for n in self.model.SUBPROCESS:
                for m in self.model.SUBPROCESS:
                    for p in self.model.OUTPUT_PRODUCTS:
                        if self.model.G[p, m, n] == 'FS':
                            self.model.Add(self.model.S[i, n] ==
                                           self.model.S[i, m] +
                                           self.model.D_SUBPROCESS[p, m] +
                                           self.model.D_CONNECTIONS[p, m, n] +
                                           self.model.R[p, m, n]).OnlyEnforceIf(self.model.A[i, p])
                        if self.model.G[p, m, n] == 'SS':
                            self.model.Add(self.model.S[i, n] ==
                                           self.model.S[i, m] +
                                           self.model.R[p, m, n]).OnlyEnforceIf(self.model.A[i, p])

        for i in self.model.BATCHES:
            for j in self.model.BATCHES:
                for p in self.model.OUTPUT_PRODUCTS:
                    # x and y implies p, rewrite as not(x and y) or p
                    self.model.AddBoolOr([self.model.A[i, p],
                                          self.model.A[j, p].Not(),
                                          self.model.A_I[i, j, p]])

                    # p implies x and y, expanded into two implication
                    self.model.AddImplication(self.model.A_I[i, j, p],
                                              self.model.A[i, p].Not())
                    self.model.AddImplication(self.model.A_I[i, j, p],
                                              self.model.A[j, p])

        # for i in self.model.BATCHES:
        #     for j in self.model.BATCHES:
        #         if j < i:
        #             for m in self.model.SUBPROCESS:
        #                 for n in self.model.SUBPROCESS:
        #                     if self.model.P[m, n] == 1:
        #                         for l in self.model.SUBPROCESS:
        #                             for p in self.model.OUTPUT_PRODUCTS:
        #                                 self.model.Add(self.model.S[i, n] >=
        #                                                self.model.S[j, m] +
        #                                                self.model.D_SUBPROCESS[p, m] +
        #                                                self.model.D_CONNECTIONS[p, m, l]).OnlyEnforceIf(
        #                                     self.model.A_I[i, j, p]
        #                                 )

        for i in self.model.BATCHES:
            for p in self.model.OUTPUT_PRODUCTS:
                self.model.Add(self.model.V_FROM_P_TO_I[i] ==
                               self.model.V[p]).OnlyEnforceIf(self.model.A[i, p])

        for n in self.model.SUBPROCESS:
            list_of_volume_variables_over_i = []
            list_of_time_variables_over_i = []
            for i in self.model.BATCHES:
                list_of_volume_variables_over_i.append(
                    self.model.V_INTERVAL[i, n]
                )
                list_of_time_variables_over_i.append(
                    self.model.B[i, n]
                )
            self.model.AddNoOverlap2D(list_of_time_variables_over_i,
                                      list_of_volume_variables_over_i)

    def __build_objective(self):
        # maximum time to minimize:
        self.model.MAX_E = self.model.NewIntVar(self.time_start,
                                                self.time_horizon,
                                                '')
        # Equal max_E with the maximum of the E variables
        self.model.AddMaxEquality(self.model.MAX_E, self.model.E.values())
        # minimize the largest ending time
        self.model.Minimize(self.model.MAX_E)
        self.solver = cp_model.CpSolver()
        self.status = self.solver.Solve(self.model)

    def __check_data_method_1(self):
        """
        Check data method
        """
        try:
            print('Check data')

        except KeyError as err:
            raise ValueError(
                '{key} from Movements is not defined in Transports'.format(
                    key=err))

    def __has_solution(self):
        if self.status == cp_model.OPTIMAL or self.status == cp_model.FEASIBLE:
            print(f'Objective function value: {self.solver.ObjectiveValue()}\n')
            df = DataFrame({
                'Start Empty': [self.solver.Value(self.model.S[i, ('Tank A', 'Emptying')]) for i in
                                self.model.BATCHES],
                'Start Fill': [self.solver.Value(self.model.S[i, ('Tank B', 'Filling')]) for i in
                               self.model.BATCHES]
            })

            print(self.model.SUBPROCESS[-1])
            print(max(self.model.D_CONNECTIONS.values()))
            print(df)

        else:
            print('No solution found.')
