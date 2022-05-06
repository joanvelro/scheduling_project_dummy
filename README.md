# GEA - Scheduler
 


```
│
├── README.md                            # This file
│
├── data                                 # data folder 
│                              
├── docs                                 # Auto-generated documentation        
│
├── notebooks                            # Notebooks folder
│
├── reports                              # output results and figures 
│    └── figures                         # figures folder 
│    └── logs                            # logs folder 
│    └── results                         # results folder 
│                              
├── src                                 
│    └── __init__.py                    # make it a package
│    └── main.py                        # main program that execute all
│    └── engine.py                      # optimization engine class
│    └── model_data.py                  # class for data model 
│    └── model_data_factory.py          # class to build data model
│    └── scheduling_response.py         # class for the response
│    └── scheduling_response_factory.py # class for build the response
│    └── visualize.py                   # class for plot results
│
│
├── test
│    └── __init__.py                    # make it a package
│    └── test_data.py                   # unitary test for data consistency
│    └── test_engine.py                 # uniutary test for engine
│
│
├── requirements.txt                     # python library dependencies
└── 
```


### Before commit, check PEP8 style!
```
python -m flake8 --max-line-length 12 --statistics
```
### Export test results
```
python -m pytest ../test --junitxml=test-results.xml --cov=. --cov-report=xml

```

### Auto-documentation management: Sphinx Tutorial
*  Install Sphinx and Rinohtype (if not installex)  in the virtual environment of the project you’re working on use the following commands below.
```
conda activate env_name
pip install Sphinx
pip install rinohtype
```
*  Create a docs directory and cd into this directory.
```
mkdir docs
cd docs
```
* Setup Sphinx
```
sphinx-quickstart
```
* Open source/conf.py
* Configure path to root directory
* Add extensions
```
make ```
* Open the index.rst and change the content to the following. (Click the index.rst  link for full content)
```
Documentation for module
**************************
.. toctree::
   :maxdepth: 2
   :caption: Contents:

Module
===================
.. automodule:: src
   :members:


utils
===================
.. automodule:: src.utils
   :members:

main
===================
.. automodule:: src.main
   :members:


Documentation for testing
**************************
.. toctree::
   :maxdepth: 2
   :caption: Test Contents:

Test
===================
.. automodule:: test.test
   :members:

```

* where automodule correspond with the name of the python file 
```
"""
.. module:: src.main
   :synopsis: define the functionality

.. moduleauthor:: (C) your name - 2021
"""
```

* Still inside the docs directory run, Create the HTML documentation files.
```
make html
```
* Create the latex documentation files
```
make latex
```
* Create the PDF documentation files
```
sphinx-build -b rinoh source _build/rinoh
```


(C) Capgemini Engineering Spain - Hybrid Intelligence - 2022
