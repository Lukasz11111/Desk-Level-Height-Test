
from time import sleep
import serial.tools.list_ports
import logging

# ========================================================================================
def connect_to_com_port():
    # Get a list of available COM ports
    ports = list(serial.tools.list_ports.comports())

    # Reverse the list of COM ports
    ports.reverse()

    # Iterate through the COM ports
    for p in ports:
        try:
            # Try to establish a connection with the current COM port
            conn = serial.Serial(port=p.device, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)

            # Print the name of the connected port
            logging.info(conn.name)

            # Wait for 2 seconds to give the device time to initialize
            sleep(2)

            # Read a line of data from the COM port and decode it using UTF-8 encoding
            str_ = conn.readline().decode('utf-8')

            # Check if the decoded string contains the substring "Hello babe"
            if "Hello babe" in str_:
                # If found, print "love" and return the serial connection
                logging.info("love")
                return conn

            # If the substring is not found, close the serial connection
            conn.close()

        except Exception as e:
            # If an exception occurs during the process, print the exception message
            logging.info(e)