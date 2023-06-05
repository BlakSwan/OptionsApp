import schedule
import multiprocessing
import data_gather
import config
import time
import os

if __name__ == '__main__':
    def run_script():
        # Add the symbols you want to track
        symbols = ['AAPL', 'TSLA', 'MSFT']  

        # Create a list to hold the process objects
        processes = []

        # Spawn multiple instances of the script
        for symbol in symbols:
            print(f"Starting {symbol}!")
            process = multiprocessing.Process(target=data_gather.get_data, args=(symbol,))
            process.start()
            processes.append(process)
            start_message = "Starting!"
            os.system(
                "osascript sendMessage.applescript {} {}".format(config.phone_number, start_message))

        # Wait for all processes to finish
        for process in processes:
            process.join()

    # # Schedule the script to run every weekday at 9:30 AM
    schedule.every().day.at("09:30").do(run_script)

    while True:
        schedule.run_pending()
        time.sleep(100)

# Run the script manually
    # run_script()

