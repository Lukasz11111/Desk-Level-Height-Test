
import time 
from datetime import datetime
import os

import serial.serialutil
import json
from datetime import date
import json
from datetime import datetime, timedelta
import connector 
import logging
# ========================================================================================
logging.basicConfig(level=logging.INFO)
# ========================================================================================

def read_data_from_json():
    # Initialize the result dictionary to store data for different time periods
    result = {
        "last_day": [],
        "last_week": [],
        "last_month": [],
        "all": []
    }
    # Open the "data.json" file and load its contents into the 'data' variable
    with open("data.json") as file:
        data = json.load(file)
    # Get today's date in the format "dd-mm-yyyy"
    today = datetime.now().strftime("%d-%m-%Y")
    # Check and add values for the current day's key ('last_day')
    if today in data:
        result["last_day"].append(data[today])
    # Get keys from the last 7 days and add their corresponding values to 'last_week'
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime("%d-%m-%Y")
        if date in data:
            result["last_week"].append(data[date])
    # Get keys from the last 30 days and add their corresponding values to 'last_month'
    for i in range(30):
        date = (datetime.now() - timedelta(days=i)).strftime("%d-%m-%Y")
        if date in data:
            result["last_month"].append(data[date])
    # Get all keys from 'data' and add their corresponding values to 'all'
    for key in data:
        result["all"].append(data[key])
    # Return the 'result' dictionary containing data for different time periods
    return result

# ========================================================================================
def aggregate_data_from_json():
    # Initialize the result dictionary to store aggregated data for different time periods
    result = {
        "last_day": [],
        "last_week": [],
        "last_month": [],
        "all": []
    }
    # Call the 'read_data_from_json()' function to retrieve data from the JSON file
    data = read_data_from_json()
    # Aggregate the values from the lists and store them in the result dictionary
    # for the corresponding time periods: 'last_day', 'last_week', 'last_month', and 'all'
    # The 'sum()' function is used to calculate the total sum of values in each list.
    result["last_day"] = sum(data["last_day"])
    result["last_week"] = sum(data["last_week"])
    result["last_month"] = sum(data["last_month"])
    result["all"] = sum(data["all"])
    # Return the 'result' dictionary containing aggregated data for different time periods
    return result

# ========================================================================================
def convert_seconds_to_minutes_hours(minutes):
    # Calculate the number of hours by integer division (//) of minutes by 60
    hours = minutes // 60
    # Calculate the remaining minutes after converting to hours using the modulo operator (%)
    remaining_minutes = minutes % 60
    # Return the formatted string with hours and remaining minutes
    return f"{hours}h:{remaining_minutes}m"

# ========================================================================================
def print_data_table():
    data = aggregate_data_from_json()

    # Clear the console screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Logging the table headers
    logging.info("Dzień\t| Tydzień\t| Miesiąc\t| Wszystko")
    logging.info("-----------------------------------------------")
    
    # Logging the values in the table
    logging.info(f"{convert_seconds_to_minutes_hours(data['last_day'])}\t| {convert_seconds_to_minutes_hours(data['last_week'])}\t| {convert_seconds_to_minutes_hours(data['last_month'])}\t| {convert_seconds_to_minutes_hours(data['all'])}")

# ========================================================================================
def add_value_to_data(parameter):
    # Get the current date in the format "dd-mm-yyyy"
    today_date = date.today().strftime("%d-%m-%Y")

    try:
        # Try to open and read the existing data from the "data.json" file
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize the data dictionary as an empty dictionary
        data = {}

    if today_date in data:
        # If the current date is already present in the data dictionary,
        # get the old value and add the parameter value to it to get the new value
        old_value = int(data[today_date])
        new_value = old_value + parameter
    else:
        # If the current date is not present in the data dictionary,
        # set the new value as the same as the parameter value
        new_value = parameter

    # Update the data dictionary with the new value for the current date
    data[today_date] = new_value

    # Write the updated data dictionary back to the "data.json" file
    with open("data.json", "w") as file:
        json.dump(data, file)

        
# ========================================================================================
def ifStand(numbers, x, threshold):
    # Check if the length of 'numbers' is less than or equal to 2 * x
    if len(numbers) <= 2 * x:
        return None
    # Sort the 'numbers' list in ascending order
    numbers.sort()
    # Trim the sorted 'numbers' list by removing the first 'x' and last 'x' elements
    numbers = numbers[x:-x]
    # Calculate the average of the trimmed 'numbers' list
    average = sum(numbers) / len(numbers)
    if average > threshold:
        # If the average is greater than the threshold, add 1 to the data for the current date in "dane.json"
        add_value_to_data(1)
        try:
            # Try to print the updated data table
            print_data_table()
        except Exception as ea: 
            # If an exception occurs during printing, print the exception message
           logging.info(ea)
    else:
        try:
            # If the average is not greater than the threshold, print the data table as usual
            print_data_table()
        except Exception as ea: 
            # If an exception occurs during printing, print the exception message
           logging.info(ea)

    # Return the calculated average
    return average

# ========================================================================================
def add_to_list(value, my_list):
    # Check if the 'value' is greater than or equal to 55
    if value >= 55:
        # If true, append the 'value' to 'my_list'
        my_list.append(value)

    # Check if the length of 'my_list' is a multiple of 60
    if len(my_list) % 60 == 0:
        # If true, call the 'ifStand()' function with 'my_list', '2', and '85' as arguments
        ifStand(my_list, 2, 85)

        # Clear the 'my_list' after calling the 'ifStand()' function
        my_list.clear()

    # Return the updated 'my_list'
    return my_list


# ========================================================================================
# Establish a connection to the COM port using the 'connect_to_com_port()' function
conn = connector.connect_to_com_port()

# Start an infinite loop to continuously read data from the COM port
while True:
    # Check if the connection to the COM port is successful (not None)
    if not conn == None:
        try:
            # Initialize an empty list 'my_list'
            my_list = []

            # Start another loop to continuously read data from the COM port
            while True:
                # Read data from the COM port and process it using the 'add_to_list()' function
                # The data is decoded from bytes to a string and then split based on ':' to extract the value
                # The extracted value is converted to an integer before being added to 'my_list'
                my_list = add_to_list(int(conn.readline().decode('utf-8').split(':')[1]), my_list)

                # Wait for 1 second before reading the next data
                time.sleep(1)
    
        except serial.serialutil.SerialException as se:
            # If the connection to the COM port is unsuccessful (None), wait for 120 seconds (2 minutes)
            # before attempting to reconnect to the COM port using 'connect_to_com_port()'
            logging.error("Lost connection")
            time.sleep(10)
            conn = connector.connect_to_com_port()
            
        except Exception as e:
            # If any exception occurs during reading or processing data, print the exception message
           logging.info(e)

    else:
        # If the connection to the COM port is unsuccessful (None), wait for 120 seconds (2 minutes)
        # before attempting to reconnect to the COM port using 'connect_to_com_port()'
        logging.error("Lost connection")
        time.sleep(120)
        conn = connector.connect_to_com_port()
    