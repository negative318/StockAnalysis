import pandas as pd
import os
import json
import datetime

LIST_STOCK = ['VCB', 'BID', 'CTG', 'TCB', 'VPB', 'SSI', 'VCI', 'VND', 'HCM', 'VIX', 'BVH', 'PVI', 'VNR', 'BIC', 'MIG', 'ACV', 'GMD', 
              'PHP', 'CII', 'MVN', 'VTP', 'HUT', 'VCG', 'CTR', 'HVN', 'VJC', 'SKG', 'BSG', 'VNS', 'DL1', 'VEA', 'GEE', 'GEX', 'RAL', 
              'PAC', 'VEF', 'TLG', 'BCG', 'TVC', 'ITS', 'VIC', 'VHM', 'BCM', 'VRE', 'SSH', 'VNM', 'MSN', 'QNS', 'VSF', 'KDC', 'MCH', 
              'VMD', 'SAB', 'SBB', 'SMB', 'SGT', 'MTA', 'FIT', 'CLX', 'DLG', 'LIX', 'KSD', 'VGI', 'FOX', 'TTN', 'MFS', 'ABC', 'SBD', 
              'FPT', 'CMG', 'ELC', 'FOC', 'SAM', 'UNI', 'ONE', 'PSD', 'VEC', 'ICT', 'ST8', 'HPG', 'KSV', 'MSR', 'HSG', 'NKG', 'DGC', 
              'DCM', 'DPM', 'CSV', 'VFG', 'THD', 'HT1', 'LIC', 'KSB', 'VLB', 'VIF', 'ACG', 'HHP', 'TEG', 'AAA', 'TDP', 'DHC', 'MZG', 
              'GVR', 'TCH', 'PHR', 'DPR', 'HHS', 'MWG', 'PNJ', 'FRT', 'DGW', 'IPA', 'VGC', 'DNP', 'NTP', 'VCS', 'ASM', 'VGT', 'MSH', 
              'TCM', 'TNG', 'STK', 'PTB', 'TTF', 'GDT', 'NAG', 'SAV', 'EVE', 'YEG', 'VNB', 'ODE', 'EID', 'VNG', 'VTR', 'DSN', 'GAS', 
              'BSR', 'PLX', 'OIL', 'SWC', 'PLC', 'PVS', 'PVD', 'PVT', 'TOS', 'TMB', 'CST', 'TVD', 'AAH', 'DDG', 'REE', 'POW', 'PGV', 
              'VSH', 'BWE', 'TDM', 'CNG', 'DHG', 'DHT', 'IMP', 'DVN', 'DBD', 'TNH', 'JVC']

def date_range(start_date_str: str, end_date_str: str):
    """
    Generates a sequence of date strings in 'YYYY-MM-DD' format
    from the start date to the end date (inclusive).

    Args:
        start_date_str: The start date as a string in 'YYYY-MM-DD' format.
        end_date_str: The end date as a string in 'YYYY-MM-DD' format.

    Yields:
        str: Each date in the range as a string in 'YYYY-MM-DD' format.
    """
    start_date = datetime.date.fromisoformat(start_date_str)
    end_date = datetime.date.fromisoformat(end_date_str)
    current_date = start_date
    while current_date <= end_date:
        yield current_date.isoformat()
        current_date += datetime.timedelta(days=1)

def get_stock_price_data(symbol:str = "VCB", start_date:str = '2020-12-31', end_date:str = '2030-12-31', with_ground_truth=False) -> pd.DataFrame:
    """
    Retrieves historical price data for a given stock symbol within a specified date range.

    Args:
        symbol (str, optional): The stock symbol to retrieve data for. Defaults to "VCB".
        start_date (str, optional): The starting date (inclusive) for the data in 'YYYY-MM-DD' format. Defaults to '2020-12-31'.
        end_date (str, optional): The ending date (inclusive) for the data in 'YYYY-MM-DD' format. Defaults to '2030-12-31'.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the historical price data for the specified symbol and date range.
                      The DataFrame is read from a CSV file located at 'data/data/{symbol}/history_price.csv' and
                      is filtered to include only rows where the 'time' column falls within the [start_date, end_date] interval.

    Raises:
        FileNotFoundError: If the CSV file for the given symbol does not exist at the specified path.
    """
    if with_ground_truth:
        path = f'./data/data/{symbol}/history_price_with_gt.csv'
    else:
        path = f'./data/data/{symbol}/history_price.csv'
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file for symbol {symbol} not found at {path}")
    df = pd.read_csv(path)
    df = df[df['time'] >= start_date]
    df = df[df['time'] <= end_date]
    return df

def get_stock_news_data(symbol:str = "VCB", start_date:str = '2020-12-31', end_date:str = '2030-12-31') -> pd.DataFrame:
    """
    Retrieves news articles for a given stock symbol within a specified date range.

    Args:
        symbol (str, optional): The stock symbol to retrieve data for. Defaults to "VCB".
        start_date (str, optional): The starting date (inclusive) for the data in 'YYYY-MM-DD' format. Defaults to '2020-12-31'.
        end_date (str, optional): The ending date (inclusive) for the data in 'YYYY-MM-DD' format. Defaults to '2030-12-31'.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the news articles for the specified symbol and date range.
                      The DataFrame is read from a JSON file located at 'data/data/{symbol}/news.json' and
                      is filtered to include only rows where the 'time' column falls within the [start_date, end_date] interval.

    Raises:
        FileNotFoundError: If the JSON file for the given symbol does not exist at the specified path.
    """
    start_date = datetime.date.fromisoformat(start_date)
    end_date = datetime.date.fromisoformat(end_date)
    path = f'./data/data/{symbol}/news.json'
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSON file for symbol {symbol} not found at '{path}'")
    with open(path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    data = {
        'time': [],
        'title': [],
        'content': []
    }
    df = pd.DataFrame(data)
    for date, value in json_data["news"].items():
        date = datetime.date.fromisoformat(date)
        if date >= start_date and date <= end_date:
            for item in value:
                data['time'].append(date.isoformat())
                data['title'].append(item['title'])
                data['content'].append(item['content'])
    data['time'].reverse()
    data['title'].reverse()
    data['content'].reverse()
    df = pd.DataFrame(data)
    return df

def get_by_date(price_df: pd.DataFrame, target_date: str) -> pd.DataFrame:
    df = price_df[price_df['time'] == target_date]
    if len(df) == 0:
        return None
    return df

if __name__ == '__main__':
    df_price = get_stock_price_data()
    df_news = get_stock_news_data()
    print(df_price.head(10))
    print(df_news.head(10))
    print(get_by_date(df_price, '2023-04-12'))
    print(get_by_date(df_news, '2021-09-01'))
    