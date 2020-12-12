from hashlib import sha256
import bitcoin.core
from bitcoin.core.script import *
from bitcoin.wallet import *
from config import (my_private_key, my_public_key, my_address,
                    network_type)
from ex1 import send_from_P2PKH_transaction, P2PKH_scriptPubKey


file_hash= sha256()
BLOCK_SIZE = 65536


with open("data.hex", 'rb') as file:
    fb = file.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
    while len(fb) > 0:  # While there is still data being read from the file
        file_hash.update(fb)  # Update the hash
        fb = file.read(BLOCK_SIZE)  # Read the next block from the file

pubkey= file_hash.digest()

pubkey_hash = bitcoin.core.Hash160(pubkey)
address5= P2PKHBitcoinAddress.from_bytes(pubkey_hash)

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.00000000 # amount of BTC in the output you're splitting minus fee
    txid_to_spend = (
        '49861d71b09bc51cd2ed153438dad0dbd194655a79797f6c399ad453ac2851d4')
    utxo_index = 6 # index of the output you are spending, indices start at 0
    ######################################################################

    """
    First Idea:
    txout_scriptPubKey = P2PKH_scriptPubKey(address5)

    response = send_from_P2PKH_transaction(
        amount_to_send,
        txid_to_spend,
        utxo_index,
        txout_scriptPubKey,
        my_private_key,
        network_type,
    )
    
    print(response.status_code, response.reason)
    print(response.text)
"""
    txout_scriptPubKey = [
        OP_RETURN, file_hash.hexdigest().encode('utf-8')
    ]
#second Idea:
    response = send_from_P2PKH_transaction(
        amount_to_send,
        txid_to_spend,
        utxo_index,
        txout_scriptPubKey,
        my_private_key,
        network_type,
    )

    print(response.status_code, response.reason)
    print(response.text)
