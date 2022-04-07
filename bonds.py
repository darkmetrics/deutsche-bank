import numpy as np
import pandas as pd
import scipy.stats as ss
import scipy.optimize as optimize
import datetime
import matplotlib.pyplot as plt

from typing import Union
from datetime import datetime as dt


def ytm(issue_date: Union[datetime.date, str],
        maturity_date: Union[datetime.date, str],
        coupon: Union[float, int],
        par: Union[float, int],
        price: Union[float, int],
        coupon_freq: Union[float, int],
        days_in_year: int = 365,
        guess: float = 0.1) -> float:
    """
    Returns yield to maturity for bond, interest

    Parameters
    ----------
    issue_date: datetime.datetime.date or string
        Date of bond issuance, format: '%Y-%m-%d'
    maturity_date: datetime.datetime.date or string
        Date of bond maturity, format: '%Y-%m-%d'
    coupon: float or int
        Coupon amount
    par: float or int
        nominal amount
    price: float or int
        Current market bond price
    coupon_freq: float or int
        Frequency of coupon payments in days (coupon is paid
        every coupon_freq days)
    days_in_year: int
        Days in year convention
    guess: float
        YTM value guess for Newton optimizer
    """
    # convert dates to datetime.datetime.date from strings
    if isinstance(issue_date, str):
        issue_date = dt.strptime(issue_date, '%Y-%m-%d')
    if isinstance(maturity_date, str):
        maturity_date = dt.strptime(maturity_date, '%Y-%m-%d')

    # generate dates
    n_coupons = (maturity_date - issue_date).days // coupon_freq
    coupon_dates = [issue_date + datetime.timedelta(days=i * coupon_freq) \
                    for i in range(1, n_coupons + 1)]
    print(coupon_dates)
    remaining = list(filter(lambda x: x > dt.today(), coupon_dates))
    print(remaining)

    # generate discount factors

    d = [(i - dt.today()).days / days_in_year for i in remaining]
    print(d)
    ytm_func = lambda y: sum([coupon / (1 + y) ** (i) for i in d]) + par / (1 + y) ** (d[-1]) - price
    return optimize.newton(ytm_func, guess)


if __name__ == "__main__":
    test = ytm(issue_date='2012-08-01',
               maturity_date='2022-07-20',
               coupon=37.9,
               coupon_freq=182,
               par=1000,
               price=970.31)
    print(test)
