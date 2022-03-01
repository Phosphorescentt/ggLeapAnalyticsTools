def test_collect_actions_dates_lineup():
    from ggLeap.helpers import read_csv
    from ggLeap.data_aggregation import remove_weeks, collect_actions

    data = read_csv("data/week.csv")

    data, _ = remove_weeks(data.copy())

    dates, distns = collect_actions(data, "LoggedIn")

    for i, day in enumerate(dates):
        distn_date = distns[i][0].date()
        assert day == distn_date


def test_collect_actions_dates_sorted():
    from ggLeap.helpers import read_csv
    from ggLeap.data_aggregation import remove_weeks, collect_actions

    data = read_csv("data/week.csv")
    data, _ = remove_weeks(data)
    dates, _ = collect_actions(data, "LoggedIn")
    dates_unsorted = dates.copy()
    dates.sort()

    for i, date in enumerate(dates):
        assert date == dates_unsorted[i]
