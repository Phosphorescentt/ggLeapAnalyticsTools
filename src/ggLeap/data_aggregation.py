from datetime import datetime, date

import pandas as pd
import numpy as np

from . import helpers
from . import DataHandler


def remove_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove dates from all datetimes in a dataframe
    """

    new_records = []
    for i in range(len(df)):
        current_record = df.loc[i].copy()
        date_string = current_record["Date"]
        dt = helpers.ggLeap_str_to_datetime(date_string)
        new_dt = helpers.remove_date_datetime(dt)
        current_record["Date"] = new_dt
        new_records.append(current_record.copy())

    return pd.DataFrame(new_records)


def remove_weeks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove all weeks from datetimes

    Change all dates in the DataFrame to the following:
    DD/MM/YY
    01/01/01 for a Monday
    02/01/01 for a Tuesday
    03/01/01 for a Wednesday
    04/01/01 for a Thursday
    05/01/01 for a Friday
    06/01/01 for a Saturday
    07/01/01 for a Sunday
    """

    dates = []
    new_records = []
    for i in range(len(df)):
        current_record = df.loc[i].copy()
        date_string = current_record["Date"]
        dt = helpers.ggLeap_str_to_datetime(date_string)
        new_dt = helpers.remove_week_datetime(dt)
        current_record["Date"] = new_dt
        new_records.append(current_record.copy())

        date = date_string.split(" ")[0]
        if date not in dates:
            dates.append(date)

    days = [0 for i in range(7)]
    for date in dates:
        day = helpers.ggLeap_get_weekday_no_time(date)
        days[day] += 1

    return pd.DataFrame(new_records.copy()), days


def collect_actions(df: pd.DataFrame, action: str) -> tuple[list, list]:
    """
    Takes data for either a single day or multiple days
    and generates cumulative distribution of the given
    action across those days. Returns a list of action
    distributions for each day
    """
    action_records = df.loc[df["Action"] == action]

    dates: list[date] = []
    action_dates_datetimes: list[list[date]] = []
    for i in range(len(action_records)):
        date = action_records.iloc[i]["Date"]
        date_no_time = date.date()

        if date_no_time in dates:
            j = dates.index(date_no_time)
            action_dates_datetimes[j].append(date)
        else:
            dates.append(date_no_time)
            action_dates_datetimes.append([])

            j = dates.index(date_no_time)
            action_dates_datetimes[j].append(date)

    return dates, action_dates_datetimes


def collect_logins(df: pd.DataFrame) -> tuple[list, list]:
    normal_dates, normal_datetimes = collect_actions(df, "LoggedIn")
    external_dates, external_datetimes = collect_actions(df, "ExternalLogin")

    date_set = list(set(normal_dates + external_dates))

    datetimes = []
    if len(normal_datetimes) == len(external_datetimes):
        for i in range(len(normal_datetimes)):
            datetimes.append(normal_datetimes[i] + external_datetimes[i])

    return date_set, datetimes


def collect_logouts(df: pd.DataFrame) -> tuple[list, list]:
    logout_dates, logout_datetimes = collect_actions(df, "LoggedOut")

    return logout_dates, logout_datetimes


def generate_cumulative_actions(
    action: str, open_time: date, close_time: date, divisions: int, coarseness: int
) -> tuple[list, list[np.ndarray]]:
    pass


def generate_cumulative_logins(
    open_time: date, close_time: date, divisions: int, coarseness: int
) -> tuple[list, list[np.ndarray]]:
    pass


def generate_cumulative_logouts(
    open_time: date, close_time: date, divisions: int, coarseness: int
) -> tuple[list, list[np.ndarray]]:
    pass


def total_user_seconds(dh: DataHandler.DataHandler, username: str) -> int:
    """
    Iterate across all of a user's logins and logouts to calculate
    the total amount of time that they've spent logged in
    """
    pass


def total_user_seconds_between(
    dh: DataHandler.DataHandler, username: str, start: int, end: int
) -> int:
    """
    Iterate across all of a user's logins and logouts to calculate
    the total amount of time that they've spent logged in between two times
    """
    pass
