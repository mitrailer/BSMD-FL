"""
This code is a modification of:
https://github.com/adap/flower/blob/main/examples/advanced_tensorflow/client.py
"""
import os

import flwr as fl
import tensorflow as tf

# Make TensorFlow log less verbose
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


# Define Flower client
class Client(fl.client.NumPyClient):
    def __init__(self, model, x_train, y_train, x_test, y_test):
        self.model = model
        self.x_train, self.y_train = x_train, y_train
        self.x_test, self.y_test = x_test, y_test

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
    # Load and compile Keras model
    model = tf.keras.applications.MobileNetV2((32, 32, 3), classes=10, weights=None)
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

    # Load CIFAR-10 dataset
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

    # Start Flower client
    client = Client(model, x_train, y_train, x_test, y_test)
    fl.client.start_numpy_client("0.0.0.0:8080", client=client)


if __name__ == "__main__":
    main()




