"""
This code is a modification of:
https://github.com/adap/flower/blob/main/examples/advanced_tensorflow/server.py
"""

from typing import Optional, Tuple
import os
import sys
import tensorflow as tf
import flwr as fl
import pandas as pd
import utils.iroha_config as iroha_config
import utils.iroha_functions as iroha_functions
from iroha import Iroha

# Get the name of the chief. This function will take the first argument after 'python3 server.py', i.e., chief
# when you run the program
name = sys.argv[1]


def main() -> None:
    # Create strategy
    strategy = fl.server.strategy.FedAvg(
        # Uncomment for overriding the evaluation and the fitting and evaluation parameters
        # eval_fn=get_eval_fn(),
        # on_fit_config_fn=fit_config,
        # on_evaluate_config_fn=evaluate_config,
    )
    # Start Flower server for three rounds of federated learning
    # Change [::] for the ip address of the server
    fl.server.start_server("[::]:8080", config={"num_rounds": 3}, strategy=strategy)


# You can override the evaluation function
def get_eval_fn():
    """
    Return an evaluation function for server-side evaluation.
    """
    # Load data and model here to avoid the overhead of doing it in `evaluate` itself
    (x_train, y_train), _ = tf.keras.datasets.cifar10.load_data()
    # Load and compile model
    # print('model compilation start')
    model = tf.keras.applications.MobileNetV2((32, 32, 3), classes=10, weights=None)
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
    # print('model compilation end')

    # The `evaluate` function will be called after every round
    def evaluate(weights: fl.common.Weights):
        model.set_weights(weights)  # Update model with the latest parameters
        # print('model evaluation')
        loss, accuracy = model.evaluate(x_train, y_train)
        print('Send request to blockchain')
        return loss, accuracy
    return evaluate


# You can override the fitting parameters
def fit_config(rnd: int):
    """
    Return training configuration dict for each round.
    Keep batch size fixed at 32, perform two rounds of training with one
    local epoch, increase to two local epochs afterwards.
    """
    config = {
        "batch_size": 32,
        "local_epochs": 1 if rnd < 2 else 2,
    }
    # set_detail_to_node(iroha, account_id, private_key, detail_key, detail_value):
    key_pairs = pd.read_csv("../iroha_keys/keypairs.csv")
    # 0 is the ketpair of the chief
    p_key = key_pairs['private_key'][0]
    domain = iroha_config.domain_id
    net = name + "@" + domain
    # this function will send a transaction to the blockchain
    iroha_functions.set_detail_to_node(Iroha(net), net, p_key, 'model_round_n', 'file_model_round_n')
    return config


# You can override the evaluation parameters
def evaluate_config(rnd: int):
    """
    Return evaluation configuration dict for each round.
    Perform five local evaluation steps on each client (i.e., use five
    batches) during rounds one to three, then increase to ten local
    evaluation steps.
    """
    val_steps = 5 if rnd < 4 else 10
    return {"val_steps": val_steps}


if __name__ == "__main__":
    main()