from sys import exit
from bitcoin.core.script import *

from utils import *
from config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type, alice_secret_key_BTC, alice_public_key_BTC)
from ex1 import P2PKH_scriptPubKey
from ex4a import Q4a_txout_scriptPubKey


######################################################################
# TODO: set these parameters correctly
amount_to_send = 0.00001 # amount of BTC in the output you're splitting minus fee
txid_to_spend = (
        '7d83eb0933e7f68cc688cde783b9cf0a6889bd65cc6b974ad550922393b9fc89')
utxo_index = 0 # index of the output you are spending, indices start at 0
######################################################################
txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)
txin_scriptPubKey = Q4a_txout_scriptPubKey

txout = create_txout(amount_to_send, txout_scriptPubKey)
txin = create_txin(txid_to_spend, utxo_index)

Alice_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             alice_secret_key_BTC)
######################################################################
# TODO: implement the scriptSig for redeeming the transaction created
# in  Exercise 2a.
txin_scriptSig = [
    Alice_sig, alice_public_key_BTC
]
######################################################################


response = send_from_custom_transaction(
    amount_to_send, txid_to_spend, utxo_index,
    txin_scriptPubKey, txin_scriptSig, txout_scriptPubKey, network_type)
print(response.status_code, response.reason)
print(response.text)
