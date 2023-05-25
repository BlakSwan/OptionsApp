import schedule
import multiprocessing
import data_gather
import config
import time
import os

def run_script():
    # Define the number of instances you want to run
    num_instances = 3
    # Add the symbols you want to track
    symbols = ['AAPL', 'TSLA', 'MSFT']  

    # Create a list to hold the process objects
    processes = []

    # Spawn multiple instances of the script
    for symbol in symbols:
        for _ in range(num_instances):
            process = multiprocessing.Process(target=data_gather.run_script(symbol))
            process.start()
            processes.append(process)
            os.system(
                "osascript sendMessage.applescript {} {}".format(config.phone_number, f"Started {symbol}!"))

    # Wait for all processes to finish
    for process in processes:
        process.join()

# Schedule the script to run every weekday at 9:30 AM
schedule.every().day.at("09:30").do(run_script)

while True:
    schedule.run_pending()
    print("Waiting... the time is {}".format(time.ctime()))
    time.sleep(100)

