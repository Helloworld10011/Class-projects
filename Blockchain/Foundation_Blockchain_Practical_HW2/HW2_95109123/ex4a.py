from sys import exit
from bitcoin.core.script import *

from utils import *
from config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type, alice_address_BTC)
from ex1 import send_from_P2PKH_transaction

address4= alice_address_BTC

######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 2
# My ID 95109123, so I changed it to 95109124 so x and y would be integers.
Q4a_txout_scriptPubKey = [
    1577274600, OP_CHECKLOCKTIMEVERIFY, OP_DROP, OP_DUP, OP_HASH160, address4, OP_EQUALVERIFY, OP_CHECKSIG
    ]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.0005# amount of BTC in the output you're splitting minus fee
    txid_to_spend = (
        'fb51a943332119b51bd383255703b2bc258af8a6787cc4fdbcdd24a1f4661e41')
    utxo_index = 1 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        Q4a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
