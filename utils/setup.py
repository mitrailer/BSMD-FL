#!/usr/bin/env python3
import binascii
import sys
import utils.iroha_functions as iroha_functions
import iroha_config
from iroha import Iroha, IrohaCrypto
import pandas as pd
import csv

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

# Create keys for all workers and chief
with open('../iroha_keys/keypairs.csv', mode='w') as csv_file:
    csv_file = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_file.writerow(['node', 'private_key', 'public_key'])
    for i in range(0, iroha_config.TOTAL_WORKERS):
        private_key = IrohaCrypto.private_key()
        public_key = IrohaCrypto.derive_public_key(private_key)
        # the rest of the code writes them into the file
        if i == 0:
            csv_file.writerow(['chief', private_key, public_key])
        else:
            csv_file.writerow(['worker' + str(i), private_key, public_key])

# Create domain and asset
iroha_functions.create_domain_and_asset()

# Get the keys from the chief and workers
key_pairs = pd.read_csv("../iroha_keys/keypairs.csv")

#################################
# nodes setup
################################
for i in range(0, iroha_config.TOTAL_WORKERS):
    if i == 0:
        iroha_functions.create_account_user('chief', key_pairs['public_key'][i],
                                            iroha_config.domain_id,
                                            '1000', iroha_config.asset_id)
    else:
        iroha_functions.create_account_user('worker' + str(i), key_pairs['public_key'][i],
                                        iroha_config.domain_id,
                                        '1000', iroha_config.asset_id)

##################################
# grant access
# ################################
# grant access so worker nodes can share us his information
for i in range(1, iroha_config.TOTAL_WORKERS):
    print(i)
    chief_name = 'chief'
    chief_account_id = chief_name + '@' + iroha_config.domain_id
    iroha_chief = Iroha('chief@federated')
    worker_name = 'worker' + str(i)
    worker_account_id = worker_name + '@' + iroha_config.domain_id
    p_key = key_pairs['private_key'][0]
    # print(iroha_chief,chief_account_id,str(key_pairs['private_key'][0]), worker_account_id)
    iroha_functions.grants_access_to_set_details(iroha_chief, chief_account_id,
                                                 p_key[2:-1], worker_account_id)

# grant access so worker node can share us his information
for i in range(1, iroha_config.TOTAL_WORKERS):
    chief_name = 'chief'
    chief_account_id = chief_name + '@' + iroha_config.domain_id
    iroha_chief = Iroha('chief@federated')
    worker_name = 'worker' + str(i)
    worker_account_id = worker_name + '@' + iroha_config.domain_id
    iroha_worker = Iroha(worker_account_id)
    p_key = key_pairs['private_key'][i]
    iroha_functions.grants_access_to_set_details(iroha_worker, worker_account_id,
                                                 p_key[2:-1], chief_account_id)

print('**********************************')
print('**********************************')
print('The BSMD is created and utils configured')
print('**********************************')
print('**********************************')