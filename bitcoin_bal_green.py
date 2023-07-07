import requests
import json
import time
import os
from colorama import init, Fore

# Initialize colorama
init()

# Define the URL for the Blockstream API
URL_BALANCE = "https://blockstream.info/api/address/{}/utxo"
URL_PRICE = "https://api.coindesk.com/v1/bpi/currentprice.json"

# Define a function to play an audible alert
def play_alert():
    if os.name == 'nt':
        # For Windows users
        os.system("PowerShell -Command \"[console]::Beep(500,1000)\"")
    else:
        # For Linux users
        os.system("echo -e '\a'")

# Define the filename of the address list
filename = "addresses.txt"

# Open the file and read in the list of addresses
with open(filename) as f:
    addresses = f.read().splitlines()

# Loop through the list of addresses and check the balance using Blockstream API
for address in addresses:
    try:
        # Make a GET request to Blockstream API to get the unspent transaction outputs (utxos) of the address
        response = requests.get(URL_BALANCE.format(address))
        
        # Check the status code of the response to make sure it was successful
        if response.status_code == 200:
            # Parse the response and calculate the balance in BTC
            utxos = json.loads(response.content.decode())
            balance = sum([utxo["value"] for utxo in utxos]) / 100000000
            
            # Make a GET request to the Coindesk API to get the current Bitcoin price
            price_response = requests.get(URL_PRICE)
            price_response_data = json.loads(price_response.content.decode())
            price = price_response_data["bpi"]["USD"]["rate"]
            
            # If the balance is greater than zero, play an audible alert and change the font color to green
            if balance > 0:
                play_alert()
                print(Fore.GREEN, end="")
            
            # Print out the balance and the current Bitcoin price
            print("Address: {} Balance: {} BTC Price: {} USD".format(address, balance, price))
            
            # Reset the font color to the default
            print(Fore.RESET, end="")
        else:
            # If the response was not successful, print out the status code and response text
            print("Error processing address {}: API returned status code {}".format(address, response.status_code))
            print(response.text)
            
    except Exception as e:
        # If an exception occurred, print out the error message
        print("Error processing address {}: {}".format(address, str(e)))
        
    # Sleep for a second to avoid hitting the API rate limit
    time.sleep(2)
