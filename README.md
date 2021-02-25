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