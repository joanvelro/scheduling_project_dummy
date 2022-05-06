"""
.. module:: src.utils
   :synopsis: This module defines common functionalities used in the whole module

.. moduleauthor:: (C) Capgemini Engineering - Hybrid Intelligence 2022
"""

import os
import shutil
import os
import sys
import logging


def list_to_reason(self, exception_list):
    """
    *List to Reason*

    Raise an exception list
    """
    if exception_list and exception_list[-1][0] is self:
        return exception_list[-1][1]


def to_list_dic(df, index=None, header=None):
    df = df.set_index(index) if index is not None else df
    df_dict = df.apply(list).to_dict() if len(df) > 0 else {}
    return df_dict[header] if header is not None and len(df) > 0 else df_dict


def to_list_preserving_order(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def to_dict(df, index=None):
    """
    *To dict*

    """
    df = df.set_index(index) if index is not None else df
    return df.T.apply(tuple).to_dict()


def check_environment():
    """
    *Check Environment*

    Check if the python environment is correctly configured
    """
    if not shutil.which("pyomo"):
        os.system('pip install -q pyomo')
        assert (shutil.which("pyomo"))

    if not (shutil.which("cbc") or os.path.isfile("cbc")):
        if "google.colab" in sys.modules:
            os.system('apt-get install -y -qq coinor-cbc')
        else:
            try:
                os.system('conda install -c conda-forge coincbc')
            except:
                pass

    assert (shutil.which("cbc") or os.path.isfile("cbc"))


def initialize_logger(name):
    """
    *Initialize Logger*

    Initialize the logger functionality to capture the progress of the execution
    """
    logger = logging.getLogger('{}'.format(name))
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('{}.log'.format(name))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logging.getLogger().addHandler(logging.StreamHandler())  # to display in console message
    # logger.debug('mensaje debug')
    # logger.info('mensaje info')
    # logger.warning('mensaje warning')
    # logger.error('mensaje error')
    # logger.critical('mensaje critical')
    return logger
