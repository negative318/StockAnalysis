import numpy as np
import pandas as pd
from utils import get_stock_price_data, date_range, get_by_date
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def get_trend(symbol: str = "VCB", start_date: str = '2024-06-30', end_date: str = '2024-09-30', based_on='close', visualize: bool = False):
    """
    Calculate the linear trend of a stock's price over a specified period.

    Args:
        symbol : str, optional
            The stock symbol to analyze (default is "VCB").
        start_date : str, optional
            The start date for the analysis in 'YYYY-MM-DD' format (default is '2024-06-30').
        end_date : str, optional
            The end date for the analysis in 'YYYY-MM-DD' format (default is '2024-09-30').
        based_on : str, optional
            The price type to base the trend on (e.g., 'close', 'open', 'high', 'low') (default is 'close').
        visualize : bool, optional
            Whether to display a plot of the actual prices and trend line (default is False).

    Returns
    tuple
        A tuple containing:
        - float: The slope of the trend line (coefficient of the linear regression).
        - float: The intercept of the trend line (y-intercept of the linear regression).
    """
    df_price = get_stock_price_data(symbol, start_date, end_date)
    
    closing_prices = []
    valid_dates = []
    
    for date in date_range(start_date, end_date):
        daily_data = get_by_date(df_price, date)
        if daily_data is not None:
            closing_prices.append(daily_data[based_on].values[0])
            valid_dates.append(date)
    
    if not closing_prices:
        print("No data.")
        return
    
    day_indices = np.arange(len(closing_prices)).reshape(-1, 1)
    closing_prices_array = np.array(closing_prices).reshape(-1, 1)

    regression_model = LinearRegression().fit(day_indices, closing_prices_array)
    
    if visualize:
        trend_line = regression_model.predict(day_indices)
        plt.figure(figsize=(10, 5))
        plt.plot(valid_dates, closing_prices, label=f"Actual {based_on} prices", marker='o')
        plt.plot(valid_dates, trend_line.flatten(), label="Trend Line", linestyle='--', color='red')
        
        plt.title(f"{symbol} Closing Price Trend from {start_date} to {end_date}")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.grid(True)
        plt.show()
    slope, intercept = regression_model.coef_[0][0], regression_model.intercept_[0]
    res = 'sideways'
    if slope >= 0.02:
        res = 'up'
    elif slope <= -0.02:
        res = 'down'
    return slope, intercept, res

if __name__ == '__main__':
    print(get_trend(based_on='close', visualize=True))
    print(get_trend(symbol='VCB', start_date='2024-12-23', end_date='2025-02-18', based_on='close', visualize=True))