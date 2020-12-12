from sys import exit
from bitcoin.core.script import *

from utils import *
from config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from ex1 import send_from_P2PKH_transaction


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 2
# My ID 95109123, so I changed it to 95109124 so x and y would be integers.
Q2a_txout_scriptPubKey = [
        OP_2DUP, OP_ADD, 9510, OP_EQUALVERIFY, OP_SUB, 9124, OP_EQUALVERIFY
    ]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.000015 # amount of BTC in the output you're splitting minus fee
    txid_to_spend = (
        '49861d71b09bc51cd2ed153438dad0dbd194655a79797f6c399ad453ac2851d4')
    utxo_index = 2 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        Q2a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
