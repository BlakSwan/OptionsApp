import schedule
import multiprocessing
import data_gather
import config
import time
import os

def run_script():
    # Add the symbols you want to track
    symbols = ['AAPL', 'TSLA', 'MSFT']  

    # Create a list to hold the process objects
    processes = []

    # Spawn multiple instances of the script
    for symbol in symbols:
        print(f"Starting {symbol}!")
        process = multiprocessing.Process(target=data_gather.run_script, args=(symbol,))
        process.start()
        processes.append(process)
        start_message = f"Starting {symbol}!"
        os.system(
            "osascript sendMessage.applescript {} {}".format(config.phone_number, start_message))

    # Wait for all processes to finish
    for process in processes:
        process.join()

    
# Schedule the script to run every weekday at 9:30 AM
schedule.every().day.at("10:51").do(run_script)

while True:
    schedule.run_pending()
    print("Waiting... the time is {}".format(time.ctime()))
    time.sleep(100)



