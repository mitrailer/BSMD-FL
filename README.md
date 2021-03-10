## Install 4 Iroha nodes in a Docker network

Install 4 iroha nodes with this [guide](https://github.com/LiTrans/iroha-nodes-for-BSMD)

## Set up the worker and chief nodes
In the file [iroha_config](utils/iroha_config.py) update the 'network' variable with the ip of the VM hosting the iroha nodes 
and update 'TOTAL_WORKERS' variable with the total number of participants in the federated proces, i.g., 10 is equal
to 9 worker and 1 chief

Modify the [shell.py](shell.py) file to match the number of participants for the federated process.  

In the file [server.py](server.py) change the line 31 
(fl.server.start_server("[::]:8080", config={"num_rounds": 3}, strategy=strategy)) and write the IP address of the server
VM

In the file [client.py](client.py) change the line 88 
(fl.client.start_numpy_client("0.0.0.0:8080", client=client)) and write the IP address of the server
VM

On a shell run:
```commandline
python setup.py
```

## Run the experiment
On a shell run:
```commandline
python shell.py
```