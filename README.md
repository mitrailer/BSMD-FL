## Install 4 Iroha nodes in a Docker network

1. Follow the Docker official [guide](https://www.docker.com/products/container-runtime) to install Docker on your 
   system 
2. Pull the iroha docker image in your system
```commandline
docker pull hyperledger/iroha:latest
```
3. Create a docker network   
```commandline
docker network create iroha-network
```
4. Create a docker volume per node
```commandline
docker volume create blockstore_0 
```
```commandline
docker volume create blockstore_1 
```
```commandline
docker volume create blockstore_2 
```
```commandline
docker volume create blockstore_3 
```

We are going to run 4 iroha node on 4 containers. So we need to create 4 postrgres containers 
1. Run postgresql in a container (The double backslashes (\\) are meant to be single)
```commandline
docker run --name some-postgres_0 \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-p 5435:5432 \
--network=iroha-network \
-d postgres:9.5
```
```commandline
docker run --name some-postgres_1 \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-p 5436:5432 \
--network=iroha-network \
-d postgres:9.5
```
```commandline
docker run --name some-postgres_2 \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-p 5437:5432 \
--network=iroha-network \
-d postgres:9.5
```
```commandline
docker run --name some-postgres_3 \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-p 5438:5432 \
--network=iroha-network \
-d postgres:9.5
```

Now we are going to install 4 iroha node and attach each node to a postgres contained

1. Run the following commands to install the Iroha nodes on containers.
```commandline
docker run --name iroha_0 \
-p 50051:50051 \
-v /mnt/home/david/Documents/BSMD/BSMD-FL/config/config_0:/opt/iroha_data \
-v blockstore_0:/tmp/block_store \
-e IROHA_POSTGRES_HOST='some-postgres_0' \
-e IROHA_POSTGRES_PORT='5435' \
-e IROHA_POSTGRES_PASSWORD='postgres' \
-e IROHA_POSTGRES_USER='postgres' \
-e KEY='node0' \
--network=iroha-network \
hyperledger/iroha:latest
```

```commandline
docker run --name iroha_1 \
-p 50052:50051 \
-v /mnt/home/david/Documents/BSMD/BSMD-FL/config/config_1:/opt/iroha_data \
-v blockstore_1:/tmp/block_store \
-e IROHA_POSTGRES_HOST='some-postgres_1' \
-e IROHA_POSTGRES_PORT='5436' \
-e IROHA_POSTGRES_PASSWORD='postgres' \
-e IROHA_POSTGRES_USER='postgres' \
-e KEY='node1' \
--network=iroha-network \
hyperledger/iroha:latest
```

```commandline
docker run --name iroha_2 \
-p 50053:50051 \
-v /mnt/home/david/Documents/BSMD/BSMD-FL/config/config_2:/opt/iroha_data \
-v blockstore_2:/tmp/block_store \
-e IROHA_POSTGRES_HOST='some-postgres_2' \
-e IROHA_POSTGRES_PORT='5437' \
-e IROHA_POSTGRES_PASSWORD='postgres' \
-e IROHA_POSTGRES_USER='postgres' \
-e KEY='node2' \
--network=iroha-network \
hyperledger/iroha:latest
```

```commandline
docker run --name iroha_3 \
-p 50054:50051 \
-v /mnt/home/david/Documents/BSMD/BSMD-FL/config/config_3:/opt/iroha_data \
-v blockstore_3:/tmp/block_store \
-e IROHA_POSTGRES_HOST='some-postgres_3' \
-e IROHA_POSTGRES_PORT='5438' \
-e IROHA_POSTGRES_PASSWORD='postgres' \
-e IROHA_POSTGRES_USER='postgres' \
-e KEY='node3' \
--network=iroha-network \
hyperledger/iroha:latest
```







## Install dependencies
On a virtual environment run
```commandline
pip install flwr
pip install tensorflow
```

## Run the experiment
Open three or more shell

On one shell run:
```commandline
python server.py
```
Wait one or two seconds
On the other shell run:
```commandline
python client.py
```

You can run as many clients (terminals) as you like

If you want to run the exp on a single shell run:
```console
./run.sh
```