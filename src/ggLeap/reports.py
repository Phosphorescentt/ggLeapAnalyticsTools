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
    if login_days != logout_days:
        raise Exception("Unable to parse data.")

    distns: list[tuple[list, list]] = []
    for i in range(len(login_days)):
        login_distn_current = login_distns[i]
        logout_distn_current = logout_distns[i]

        login_times = login_distn_current[0]
        logout_times = logout_distn_current[0]

        total = len(login_times) + len(logout_times)

        print(f"Len login times: {len(login_times)}")
        print(f"Len logout times: {len(logout_times)}")
        print(f"Total: {total}")

        temp_cum_actions: tuple[list, list] = ([], [])
        a = 0
        b = 0
        current_users = 0
        for j in range(total):
            print(f"j: {j}")
            print(f"a: {a}")
            print(f"b: {b}")
            print("======")

            try:
                login_time = login_times[a]
                logout_time = logout_times[b]
                if login_time < logout_time:
                    a += 1
                    current_users += 1

                    temp_cum_actions[0].append(login_time)
                    temp_cum_actions[1].append(current_users)
                elif logout_time < login_time:
                    b += 1
                    current_users -= 1

                    temp_cum_actions[0].append(logout_time)
                    temp_cum_actions[1].append(current_users)
                elif login_time == logout_time:
                    a += 1
                    b += 1
                    current_users += 0

                    temp_cum_actions[0].append(login_time)
                    temp_cum_actions[1].append(current_users)
                else:
                    raise Exception("Something went wrong.")
            except:
                temp_cum_actions[0].append(login_time)
                temp_cum_actions[1].append(current_users)

        distns.append(temp_cum_actions)

    return login_days, distns
