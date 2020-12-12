from sys import exit
from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress

from utils import *
from config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from ex1 import send_from_P2PKH_transaction

Ata_seckey= CBitcoinSecret('cPzHxK32tgSSqFvmPkJUjDjL6KAQxTmWfTUinLw6nnUG7BrfQPwd')
Ata_Pubkey= Ata_seckey.pub

Faraz_seckey= CBitcoinSecret('cNEQm2Mvn6HCw572UpR8ijZ92Ef3YCXqpT4s7LDwppZoXSEkLTcR')
Faraz_Pubkey= Faraz_seckey.pub

share1_seckey= CBitcoinSecret('cUzqrtwS7wC8YZJsN2UKiymqhfT8rBoVFDBUJGJpYM8b2zEH7657')
share1_Pubkey= share1_seckey.pub

share2_seckey= CBitcoinSecret('cQwqf6us54pcfg7PFnkjg1qDF5K8Bf4VjyEAwsiu5ypjB43aJNU1')
share2_Pubkey=share2_seckey.pub

share3_seckey= CBitcoinSecret('cQkoNb5w7Bob7PFWKJDUgx7WezpZTV1cJ1PvXQkjBetCTjMAqXEj')
share3_Pubkey= share3_seckey.pub

share4_seckey= CBitcoinSecret('cRD72eZLdshTJyiczzbFwDgYg3ZHdW2KQ3ubYcg4toanywvhErWN')
share4_Pubkey= share4_seckey.pub

share5_seckey= CBitcoinSecret('cVGc6myXwV41VWQxPMk7NeXtD1JhCD5KFAqAsNgecxRtxmL9WEQc')
share5_Pubkey= share5_seckey.pub

######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 2
# My ID 95109123, so I changed it to 95109124 so x and y would be integers.
Q31b_txout_scriptPubKey = [
    1, Ata_Pubkey, Faraz_Pubkey,
    2, OP_CHECKMULTISIGVERIFY, 3, share1_Pubkey, share2_Pubkey, share3_Pubkey, share4_Pubkey, share5_Pubkey, 5,
    OP_CHECKMULTISIG
    ]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.002 # amount of BTC in the output you're splitting minus fee
    txid_to_spend = (
        '97fee5d3d78dd1e154c484df19fe36923b6bc78a8432e61643db8d84ad6ed41d')
    utxo_index = 1 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        Q31b_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
