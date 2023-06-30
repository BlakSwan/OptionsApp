from yahooquery import Ticker
import pandas as pd
from datetime import datetime, time
import time as tm
import os
import config

def get_option_chain(ticker):
    """
    Returns the option chain for the specified ticker.
    """
    t = Ticker(ticker)
    df = pd.DataFrame(t.option_chain)
    return df


def get_data(symbol):
    # Define the start and end times for the API calls
    start_time = time(9, 30)
    end_time = time(16, 00)
    count = 0
    df_tracker = pd.DataFrame()
    while True:
        # Check if the current time is within market hours
        current_time = datetime.now().time()
        if current_time >= start_time and current_time <= end_time:
            # Make the API call 
            df = get_option_chain(symbol)
            # Remove the multi-index
            df = df.reset_index(drop=True)
            # Filter the data frame to include only calls
            df = df[df['contractSymbol'].str[10] =='C']
            # Add a timestamp column
            df['timestamp'] = datetime.now().strftime('%H:%M:%S')
            # Add the latest call to the data frame
            df_tracker = pd.concat([df_tracker, df])
            count += 1
            # Get today's date as a string in the format YYYY-MM-DD and add it to the output file name
            today = datetime.today().strftime('%Y-%m-%d')
            # Define the output file name and directory
            output_file = symbol + 'option_chain' + today + datetime.now().strftime('%H') + '.csv'
            directory = f'/Volumes/External Drive/data/{symbol}/'
            #Output to csv every hour
            if count % 12 == 0:
                df_tracker.to_csv(directory + output_file, index=False)
                df_tracker = pd.DataFrame()
        #Output to csv at the end of the day and send a text message
        elif current_time >= end_time:
            done_message = f"Done{symbol}!"
            if len(df_tracker) > 1:
                df_tracker.to_csv(directory + output_file, index=False)
            os.system(f"osascript sendMessage.applescript {config.phone_number} {done_message}")
            break
        
        # Wait 5 minutes before making the next API call
        tm.sleep(300)


