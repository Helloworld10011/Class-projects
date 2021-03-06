from sys import exit
from bitcoin.core.script import *

from utils import *
from config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from ex1 import P2PKH_scriptPubKey
from ex31a import (Q31a_txout_scriptPubKey, Ata_seckey, Faraz_seckey, share1_seckey, share2_seckey, share3_seckey,
                    share4_seckey, share5_seckey)


######################################################################
# TODO: set these parameters correctly
amount_to_send = 0.00001 # amount of BTC in the output you're splitting minus fee
txid_to_spend = (
        '6c4dde70757b1c74c9ce8a8c6d424704151f7fd9da742117e70bf7f446ea20e6')
utxo_index = 0 # index of the output you are spending, indices start at 0
######################################################################
txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)

txin = create_txin(txid_to_spend, utxo_index)
txout = create_txout(amount_to_send, txout_scriptPubKey)

txin_scriptPubKey = Q31a_txout_scriptPubKey

Ata_sig= create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, Ata_seckey)
Faraz_sig= create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, Faraz_seckey)

######################################################################
# TODO: implement the scriptSig for redeeming the transaction created
# in  Exercise 2a.
txin_scriptSig = [
    1, Ata_sig, Faraz_sig
]
######################################################################


response = send_from_custom_transaction(
    amount_to_send, txid_to_spend, utxo_index,
    txin_scriptPubKey, txin_scriptSig, txout_scriptPubKey, network_type)
print(response.status_code, response.reason)
print(response.text)
