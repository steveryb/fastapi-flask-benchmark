from datetime import timedelta, datetime

import ergo
import pandas as pd
from scipy import stats

"""
This file is modified from a model hosted in ergo here: https://github.com/oughtinc/ergo/blob/f3d28f989ccf16586d58dc4b63106e9065dc4afa/notebooks/covid-19-tests-august-2020.ipynb
"""


class Covid19TestsModel(object):
    def __init__(self, testing_data):
        self.testing_data = testing_data

        self.current_date = testing_data["date"].max()

        self.last_month = self.current_date - timedelta(days=30)
        # if there's multiple entries for a day for whatever reason, take the first
        self.current_test_number = testing_data.loc[testing_data["date"] == self.current_date]["totalTestResults"][0]

        # data subsets
        self.test_data_over_last_month = self.testing_data[
            testing_data['date'].between(self.last_month, self.current_date)]

        # calculate slope
        test_data_worth_looking_at = testing_data[testing_data['totalTestResults'] >= 100000]
        self.slope_of_test_increases = stats.linregress(
            test_data_worth_looking_at["days"],
            test_data_worth_looking_at["totalTestResultsIncrease"]).slope

    def test_results_increase_per_day(self):
        """
        Estimated test increase over the past day looking at increases over the last month
        """
        return ergo.random_choice(list(self.test_data_over_last_month["totalTestResultsIncrease"]))

    def estimated_slope(self):
        """
        Estimated slope of increase of tests per day looking at linear regression of test cases,
        and a log-normal prediction of the possible changes
        """
        return ergo.lognormal_from_interval(0.5, 2) * self.slope_of_test_increases

    def test_results_for_date_with_slope(self, date: datetime):
        """
        Estimated test results for date, estimating based on the number of estimated test results per day
        including the estimated rate of increase
        """
        number_of_days = (date - self.current_date).days
        return self.current_test_number + \
               sum(self.test_results_increase_per_day() + self.estimated_slope() * day for day in range(number_of_days))

    def test_results_for_deadline_with_slope(self):
        return self.test_results_for_date_with_slope(datetime(2022, 10, 7))


def run_model():
    testing_data = pd.read_csv("data/covid_tracker_daily_2020_10_05.csv")
    testing_data["date"] = testing_data["date"].apply(lambda d: datetime.strptime(str(d), "%Y%m%d"))
    testing_data = testing_data[["date", "totalTestResults", "totalTestResultsIncrease"]]
    first_date = testing_data["date"].min()
    testing_data["days"] = \
        testing_data["date"].apply(lambda d: (d - first_date).days)

    model = Covid19TestsModel(testing_data)

    return model.test_results_for_deadline_with_slope()


if __name__ == "__main__":
    print(run_model())
