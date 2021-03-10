import os
import time

# modify this file to match the federated nodes you want to add
# --worker_name is the name of the federated node
# the server should be named 'chief' and the clients are worker1, worker2, etc
# make sure to put the 'sleep 3s' between clients
os.system('cd to some directory & '
          'source etc.... & '
          'taskset -c 0 python3 server.py chief'
          'sleep 7s &&'
          'taskset -c 1 python3 client.py worker1'
          'sleep 3s &&'
          'taskset -c 2 python3 client.py worker2'
          )
