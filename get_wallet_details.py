import os
from dotenv import load_dotenv

import requests
from solders.pubkey import Pubkey
from solana.rpc.api import Client

load_dotenv()


# Define Solana cluster RPC endpoint
RPC_ENDPOINT = "https://api.mainnet-beta.solana.com"
client = Client(RPC_ENDPOINT)

def get_solana_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        # TODO: Add btc value
        params = {
            "ids": "solana",  # Cryptocurrency ID for Solana
            "vs_currencies": "usd"  # Fiat currency for conversion
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data["solana"]["usd"]
        else:
            return None
    except Exception as e:
        print(f"Error fetching SOL price: {e}")
        return None


def get_wallet_balance(public_key):
    #Fetch a request of getting balance (returns in lamports)
    response = client.get_balance(public_key) 
    # Check response value
    if response.value is not None:
        # Convert lamports to SOL
        sol_balance = response.value / 1_000_000_000
        return sol_balance
    else:
        print("Error: Could not fetch balance.")
        return None


def get_recent_wallet_transactions(public_key, limit): 
    # Request confirmed signatures for the wallet
    response = client.get_signatures_for_address(public_key, limit=limit)
    
    # Access the 'value' property of the response
    if response.value:
        return response.value
    else:
        print("No transactions found.")
        return []

# Function to get recent transactions for a wallet
def get_wallet_details(wallet_address, limit=2):
    """Fetch recent transactions of the given wallet address."""
    try:
        # Convert the wallet address string to a Pubkey object
        public_key = Pubkey.from_string(wallet_address)

        #Get wallet balance
        wallet_sol_balance = get_wallet_balance(public_key)

        # Get recent wallet transactions
        recent_trans = get_recent_wallet_transactions(public_key, limit)

        solana_price = get_solana_price()
        return {"Sol": wallet_sol_balance, "USD": wallet_sol_balance * solana_price, "sol_price": solana_price}

    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return []

# Example usage
wallet_address = os.getenv('WALLET_ADDRESS')  # Public wallet address for testing
transactions = get_wallet_details(wallet_address)
print(transactions)
