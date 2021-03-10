#!/usr/bin/env python3

import hashlib
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto

# Federated learner configuration
##################################
# BATCH_SIZE = 16
# EPOCHS = 250
# INTERVAL_STEPS = 1  # Steps between averages
# WAIT_TIME = 15  # How many seconds to wait for new workers to connect
# CHIEF_PUBLIC_IP = '127.0.0.1:7777'  # Public IP of the chief worker
# CHIEF_PRIVATE_IP = '127.0.0.1:7777'  # Private IP of the chief worker
# Set this variable to match the number of participants. 10 is for 1 chief and 9 workers
TOTAL_WORKERS = 10


# BSMD configuration
######################
asset_id = 'fedcoin#federated'
# Replace localhost with an IP address of a node running the blockchain
network = IrohaGrpc('127.0.0.1:50051')
domain_id = 'federated'
admin_private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
iroha_admin = Iroha('admin@test')
default_role = 'user'
asset_name = 'fedcoin'
asset_precision = 2


