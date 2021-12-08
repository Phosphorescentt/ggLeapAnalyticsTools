import pandas as pd

from . import data_aggregation
from . import data_collectoin
from . import importing 
from . import reports


class DataHandler:
    """ The main part of this package - an object to handle all the data. """
    def __init__(self, data=None):
        if data is not None:
            # Load the data somehow
            pass
