from datetime import datetime, date

import pandas as pd
import numpy as np

from . import helpers
from . import data_aggregation

"""
The functions in this file are designed to take a completely uncleaned
and unprocessed input and return something instantly useable self.

For example, feeding the concurrent_logins function data for a whole week
and it returns the concurrent logins for every day in that week which can
be instantly plotted onto a graph with matplotlib.
"""


def concurrent_logins(df: pd.DataFrame) -> pd.DataFrame:
    # Collect logins
    login_days, login_data = data_aggregation.collect_logins(df)
    logout_days, logout_data = data_aggregation.collect_logouts(df)

    # Generate cumulative distributions
    login_days, login_distns = data_aggregation.generate_cumulative_distribution(
        login_days, login_data
    )
    logout_days, logout_distns = data_aggregation.generate_cumulative_distribution(
        logout_days, logout_data
    )

    # Combine the two to get concurrent logins
    # Done?
    pass
