# Open the Tutorial for instructions.
from codes import cleanup_tx


lock_tx_parts = """
version: 02000000
num inputs: 01
  txid: 9aef57862f85a169f6e154e3df34a53bcac8511b33882a6ec1d64e618e268570
  vout: 00000000
  scriptSig: 00
  sequence: feffffff
num outputs: 01
  amount: 3ef0052a01000000
  scriptPubKey: 232103c8edf725b59d9f370870a5dcd5e70b0baea493a5b85cb227c1ef6a8e8cdad8fbac
locktime: 00000000
"""

spend_tx_parts = """
version: 02000000
num inputs: 01
  txid: 4d101e8cb94f79ace7e7b502a1f0ac61d2e6a71f4cdac3563390597fa72dbc18
  vout: 00000000
  scriptSig: 00
  sequence: feffffff
num outputs: 01
  amount: 7cee052a01000000
  scriptPubKey: 1600142e280d852d48fc17784b4b1e39764fb34949cbf8
locktime: 00000000
"""


p2pk_info = {
  # Fill this in with your private key
  'private_key': 888,
  # Fill this in with the pubkey for your private key, compressed
  'pubkey': '03c8edf725b59d9f370870a5dcd5e70b0baea493a5b85cb227c1ef6a8e8cdad8fb',
  # Fill this in with the P2PK script for your pubkey
  'p2pk_script': '2103c8edf725b59d9f370870a5dcd5e70b0baea493a5b85cb227c1ef6a8e8cdad8fbac',
  # Add a scriptPubKey and amount to the `tx_parts`, above.
  'tx': cleanup_tx(lock_tx_parts),
  # TXID of the signed and sent transaction
  'sent_txid': '18bc2da77f59903356c3da4c1fa7e6d261acf0a102b5e7e7ac794fb98c1e104d',
  # TX that spends the above txid
  'spend_tx': cleanup_tx(spend_tx_parts),
}

print("Locking TX:", cleanup_tx(lock_tx_parts))
print("Spending TX:", cleanup_tx(spend_tx_parts))