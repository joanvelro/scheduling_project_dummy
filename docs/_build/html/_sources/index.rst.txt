.. GEA documentation master file, created by
   sphinx-quickstart on Tue Mar 15 15:51:05 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GEA Schedeus - Scheduler Documentation - V.0.1
===============================

.. image:: /images/logos.png
  :width: 500


The scheduler optimization module is formulated as a Mixed-Integer Programming problem (MIP) using the framework ORTools and Python as programming
language.

.. math::

   min_{x \in \mathbb{R}, y \in (0,1)} \ f(x,y)

.. math::

   st: \ g(x,y) <=0

The module evaluates whether a certain plant configuration is able to satisfy a certain product demand within a given time frame (both also given as an input parameter)
according to some solution criterion to be clarified below.

Within the  scheduler module, an initial pre-check (input data analyzer) is executed before starting the scheduling problem to identify
possible data inconsistencies and will communicate the possible warnings or errors founded in the output of the scheduler.



If there exists a feasible schedule for the input plant configuration, the scheduler provides a schedule-type output, which will later be used
to construct one Gantt chart (the construction is out of this scope).


If no feasible schedule exists, then the relaxed schedule-type output is provided, and the list of the equipment involved with their utilization
ratios will be provided. This will be obtained  by relaxing certain constraints until a feasible problem can be reached to follow the same procedure
as with bottleneck identification.



If the input data instance is not consistent (exist errors) then no schedule-type output is provided. The error message will indicate clearly the
reason of failure.


The output will contain a list of possible warnings and error (data inconsistencies) messages.



This version includes:

* Batch/continuous processes.
* Already running equipment.
* Multi-product/Multi-workflows.

This version DOES NOT includes:

* CIPs.
* Product Order.
* Clusters.
* Split Workflows.

Scheduler Module Documentation
==============================

.. toctree::
   :maxdepth: 4
   :caption: Scheduler Contents:

Model Data
***********
.. automodule:: src.model_data
   :members:

Scheduler Response
********************
.. automodule:: src.scheduler_response
   :members:

Scheduler Engine
*******************
.. automodule:: src.engine
   :members:

Model Data Factory
*******************
.. automodule:: src.model_data_factory
   :members:


Scheduler Response Factory
***************************
.. automodule:: src.scheduler_response_factory
   :members:

Utils
*******
.. automodule:: src.utils
   :members:

Unit Testing Documentation
==========================
.. toctree::
   :maxdepth: 3
   :caption: Test Contents:


Data Test
**********
.. automodule:: test.test_data
   :members:

Engine Test
************
.. automodule:: test.test_engine
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
