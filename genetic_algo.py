import random
import bird_logic
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights_input_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.weights_hidden_output = np.random.uniform(-1, 1, (hidden_size, output_size))

    def forward(self, inputs):
        hidden = np.dot(inputs, self.weights_input_hidden)
        hidden = 1 / (1 + np.exp(-hidden))  # Sigmoid activation function
        output = np.dot(hidden, self.weights_hidden_output)
        output = 1 / (1 + np.exp(-output))
        return output

def create_neural_network(input_size, hidden_size, output_size):
    model = Sequential()
    model.add(Dense(hidden_size, input_dim=input_size, activation='sigmoid'))
    model.add(Dense(output_size, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
