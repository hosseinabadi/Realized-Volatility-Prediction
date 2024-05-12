import requests
import pandas as pd
import json
from dateutil import rrule, parser
import os
from datetime import timedelta


def get_data_alpha_vantage(start_date, end_date, stock_symbol):
    # Generate a list of all months between the start and end dates
    months = list(rrule.rrule(rrule.MONTHLY, dtstart=parser.parse(start_date), until=parser.parse(end_date)))

    # Initialize an empty list to store the DataFrames
    dfs = []

    # Loop over the list of months
    for month in months:
        # Format the current month into the required format for the API request
        formatted_month = month.strftime("%Y-%m")

        # Make the API request and get the response
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=5min&month={formatted_month}&outputsize=full&apikey=V9AMYI6A7YVMUUZZ"
        r = requests.get(url)
        monthly_data = r.json()
        try:
            df = pd.DataFrame(monthly_data["Time Series (5min)"]).transpose()[::-1]
        except:
            print(month)
            print(monthly_data)
            data = pd.concat(dfs)
            break
        # Convert the response JSON into a DataFrame and transpose it
        # Append the DataFrame to the list of DataFrames
        dfs.append(df)

    # Concatenate all the DataFrames in the list into a single DataFrame
    data = pd.concat(dfs)
    return data


def merge_data_alpha_vantage(data_directory, stock_symbol):
    # List to store DataFrames
    dfs = []

    data_directory = os.path.join(data_directory, stock_symbol)

    # Iterate over files in the directory
    for file in os.listdir(data_directory):
        if file.endswith(".csv") and file.startswith("data_"):
            # Read CSV file into DataFrame with the first column as index and parse dates
            file_path = os.path.join(data_directory, file)
            df = pd.read_csv(file_path, index_col=0, parse_dates=[0])

            # Append DataFrame to the list
            dfs.append(df)

    # Concatenate all DataFrames
    concatenated_df = pd.concat(dfs)
    concatenated_df.drop_duplicates(inplace=True)

    # Sort the index based on the date
    concatenated_df.sort_index(inplace=True)

    return concatenated_df


def get_data_twelve_data(stock_symbol, start_date, end_date):
    # Define start and end dates

    # Initialize an empty list to store dataframes
    dfs = []

    # Define the interval for each request (3 months)
    interval = timedelta(days=3 * 30)

    # Make requests in a loop
    while start_date < end_date:
        # Define end date for the current request (3 months ahead)
        request_end_date = min(start_date + interval, end_date)

        # Format dates as strings
        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        request_end_date_str = request_end_date.strftime("%Y-%m-%d %H:%M:%S")

        # Make request
        response = requests.get(
            f"https://api.twelvedata.com/time_series?apikey=92e1895b6d9140719689a551a2a7ddcf&interval=5min&symbol={stock_symbol}&start_date={start_date_str}&end_date={request_end_date_str}&format=JSON")

        # Convert response to JSON format
        json_data = response.json()

        # Convert JSON data to DataFrame
        data = pd.DataFrame(json_data['values'])[::-1]

        # Set datetime column as index
        data['datetime'] = pd.to_datetime(data['datetime'])
        data.set_index('datetime', inplace=True)

        # Append dataframe to the list
        dfs.append(data)

        # Update start date for the next request
        start_date = request_end_date

        # Pause to ensure at most 6 requests per minute
        time.sleep(10)  # Adjust as needed to ensure 6 requests per minute

    # Concatenate all dataframes
    merged_df = pd.concat(dfs)

    merged_df = merged_df.drop_duplicates()
    # Print the merged dataframe
    return merged_df
