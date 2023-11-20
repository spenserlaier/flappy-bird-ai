import random
import bird_logic
import numpy as np

# Define constants
POPULATION_SIZE = 50
MUTATION_RATE = 0.1
GENERATIONS = 100

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
def should_flap(self, inputs):
    # Neural network decision
    output = self.neural_network.forward(inputs)
    return output > 0  # Adjust threshold as needed
