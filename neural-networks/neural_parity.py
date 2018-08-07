import numpy as np
from random import random, shuffle
from math import floor

class Network:
    def __init__(self, structure: list):
        self.structure = structure
        self.biases = [np.random.randn(1, y) for y in structure[1:]]
        self.weights = [np.random.randn(x, y) for x, y in zip(structure[1:], structure[:-1])]

    def feed_forward(self, data: list) -> list:
        for w, b in zip(self.weights, self.biases):
            data = sigmoid(np.dot(w, data) + b[0])
        return data

    def back_propagation(self, input_data: np.ndarray, expectations: np.ndarray) -> (np.ndarray, np.ndarray):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        activation = input_data
        activations = [activation]
        zs = []
        for w, b in zip(self.weights, self.biases):
            z = np.dot(w, activation) + b[0]
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        delta = 2 * Network.cost_derivative(activations[-1], expectations) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta[np.newaxis].T, activations[-2][np.newaxis])

        for l in range(2, len(self.structure)):
            z = zs[-l]
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sigmoid_prime(z)
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta[np.newaxis].T, activations[-l-1][np.newaxis])
        return nabla_b, nabla_w

    def train(self, training_data: list, learning_rate: int):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for data, expect in training_data:
            nabla_b_delta, nabla_w_delta = self.back_propagation(data, expect)
            nabla_b = [nb + nbd for nb, nbd in zip(nabla_b, nabla_b_delta)]
            nabla_w = [nw + nwd for nw, nwd in zip(nabla_w, nabla_w_delta)]
        self.weights = [w - nw * learning_rate/len(training_data) for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - nb * learning_rate/len(training_data) for b, nb in zip(self.biases, nabla_b)]

    def input(self, data: list, packet_size: int, learning_rate: int = 1):
        shuffle(data)
        for x in range(0, len(data), packet_size):
            self.train(data[x:x + packet_size], learning_rate)

    def check_network(self, data: list) -> float:
        """ Function that checks how good is your network """
        return sum(int(x == y) for (x, y) in [(np.argmax(self.feed_forward(i)), np.argmax(o)) for (i, o) in data])/len(data)

    def test(self, number: int) -> str:
        bin_number = bin(number)[2:]
        i = (BITS - len(bin_number)) * '0' + bin_number
        t = self.feed_forward(list(map(lambda y: int(y), list(i))))
        return str(number) + ' is even' if t[0] < t[1] else str(number) + ' is Odd'

    def save_network(self):
        data = []
        # [[data.append(y) for y in z] for z in [x[0] for x in self.biases]]
        print(self.weights)
        [[data.append(y) for y in z] for z in [x for x in self.weights]]
        print(data)
        # np.savetxt('network.txt', data)


    def load_network(self):
        with np.load('network.npz') as file:
            data = file
        for x in file['arr_0']:
            print(x)
        print(file)

    @staticmethod
    def cost_derivative( activation_value: np.ndarray, expected_value: np.ndarray) -> np.ndarray:
        return np.subtract(activation_value, expected_value)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))

BITS = 16


net = Network([BITS, 4, 4, 2])

dane = []
od = 0
do = 2**BITS - 1
test = [int(floor(random()*do) + od) for _ in range(15)]
for x in range(50000):
    number = int(floor(random()*do) + od)
    if not number % 2: o = np.array([0, 1])
    else: o = np.array([1, 0])
    bin_number = bin(number)[2:]
    i = (BITS - len(bin_number)) * '0' + bin_number
    dane.append((np.array(list(map(lambda x: int(x), list(i)))), o))

test_data = []
for y in range(1000):
    number = int(floor(random()*do) + od)
    if not number % 2: o = np.array([0, 1])
    else: o = np.array([1, 0])
    bin_number = bin(number)[2:]
    i = (BITS - len(bin_number)) * '0' + bin_number
    test_data.append((np.array(list(map(lambda y: int(y), list(i)))), o))

for num in test:
    print(net.test(num))

print(net.check_network(test_data))
eff = 0
while eff != 1:
    net.input(dane, 5000, 1)
    eff = net.check_network(test_data)
    print(eff)

for num in test:
    print(net.test(num))

# print(n.weights)
# print(n.biases)
