"""
This code is a modification of:
https://github.com/adap/flower/blob/main/examples/advanced_tensorflow/client.py
"""
import os
import sys
import flwr as fl
import tensorflow as tf
import utils.iroha_functions as iroha_functions
import utils.iroha_config as iroha_config
from iroha import Iroha
import pandas as pd

# Make TensorFlow log less verbose
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


# Define Flower client
class Client(fl.client.NumPyClient):

    def __init__(self, model, x_train, y_train, x_test, y_test, name):
        self.model = model
        self.x_train, self.y_train = x_train, y_train
        self.x_test, self.y_test = x_test, y_test
        # This is the name of the node we get from the file run_shell --worker_name
        self.name = name

    def get_parameters(self):
        """
        Get the model from the chief
        """
        return self.model.get_weights()

    def fit(self, parameters, config):
        """
        Locally train the model and send the model to chief for average. This function also send a transaction
        request to blockchain (not yet implemented)
        :param parameters:
        :param config:
        :return:
        """
        self.model.set_weights(parameters)
        self.model.fit(self.x_train, self.y_train, epochs=1, batch_size=32, steps_per_epoch=5)
        print("Send request to blockchain")
        # set_detail_to_node(iroha, account_id, private_key, detail_key, detail_value):
        key_pairs = pd.read_csv("../iroha_keys/keypairs.csv")
         # i is equal to the index for the worker. For instance if name=worker1 then i=1
        p_key = key_pairs['private_key'][i]
        name = self.name
        domain = iroha_config.domain_id
        net = self.name + "@" + domain
        # this function will send a transaction to the blockchain
        iroha_functions.set_detail_to_node(Iroha(net), net, p_key, 'model_round_n', 'file_model_round_n')
        return self.model.get_weights(), len(self.x_train), {}

    def evaluate(self, parameters, config):
        """
        Evaluate the model and send a transaction request to blockchain (not yet implemented)
        :param parameters:
        :param config:
        :return:
        """
        self.model.set_weights(parameters)
        loss, accuracy = self.model.evaluate(self.x_test, self.y_test)
        print("Send request to blockchain")
        return loss, len(self.x_test), {"accuracy": accuracy}


def main() -> None:
    # Get the name of the worker. This function will take the first argument after 'python3 server.py', e.g., worker1
    # when you run the program
    name = sys.argv[1]
    # Load and compile Keras model
    model = tf.keras.applications.MobileNetV2((32, 32, 3), classes=10, weights=None)
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

    # Get the train sets from a file
    x,y= get_trainset_from_name
    x_train = worker_1/trainset/file_1_x.npy
    y_train = worker_1 / trainset / file_1_x.npy
    ...
    ...
    # (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

    # Start Flower client
    client = Client(model, x_train, y_train, x_test, y_test, name)
    # Change 0.0.0.0 for the ip address of the server
    fl.client.start_numpy_client("0.0.0.0:8080", client=client)


if __name__ == "__main__":
    main()




