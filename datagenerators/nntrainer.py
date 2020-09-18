import numpy as np

class NNTrainer:
    def __init__(self, data, hidden_layers, labels):
        self.data = np.array(data)
        self.labels = np.array(labels)
        self.layers = self.generate_layers([len(data[0])] + hidden_layers + [len(labels[0])])
        self.layers_history = [self.copy_layers()]
        self.sigma = 0.01

    def generate_layers(self, layers):
        out = []
        for l in range(len(layers)-1):
            step = {
                'weights': np.random.rand(layers[l], layers[l+1]),
                'bias': np.random.rand(1, layers[l+1]),
                'activation_function': NNTrainer.sigmoid,
                'activation_function_prime': NNTrainer.sigmoid_prime
            }
            out.append(step)
        return out

    def copy_layers(self):
        out = []
        for l in self.layers:
            step = {
                'weights': l['weights'].copy(),
                'bias': l['bias'].copy()
            }
            out.append(step)
        return out

    def forward_prop(self, inp):
        history = []
        temp = inp
        history.append(temp)
        for l in self.layers:
            temp = temp @ l['weights'] + l['bias']
            history.append(temp)
            temp = l['activation_function'](temp)
            history.append(temp)
        return history

    def back_prop(self, hist, labels):
        dJd = []
        # derr/dw = derr/dsig * dsig/dz * dz/dW = x^T * -(sig(Wx + b) - label) * sig_prime(Wx + b)
        # derr/db = derr/dsig * dsig/dz * dz/db = -(sig(Wx + b) - label) * sig_prime(Wx + b) * 1
        layers_reversed = self.layers[::-1]
        delta = (hist.pop() - labels) * layers_reversed[0]['activation_function_prime'](hist.pop())
        dJd.append((hist.pop().T @ delta, np.ones((1, delta.shape[0])) @ delta))
        b4_weight = layers_reversed[0]['weights']
        for l in layers_reversed[1:]:
            # derr/dw-1 = delta * dz/da * da/dz * dz/dW = x^T delta * WT * sig_prime(Wx + b)
            # derr/db-1 = delta * dz/da * da/dz * dz/dB = delta * WT * sig_prime(Wx + b)
            delta = delta @ b4_weight.T * l['activation_function_prime'](hist.pop())
            dJd.append((hist.pop().T @ delta, np.ones((1, delta.shape[0])) @ delta))
            b4_weight = l['weights']
        return dJd[::-1]


    def update(self, changes, sigma):
        for l in range(len(self.layers)):
            self.layers[l]['weights'] -= changes[l][0]*sigma
            self.layers[l]['bias'] -= changes[l][1]*sigma

    def one_training_epoch(self):
        self.n_training_epochs(1)

    def n_training_epochs(self, num):
        for _ in range(num):
            hist = self.forward_prop(self.data)
            changes = self.back_prop(hist, self.labels)
            self.update(changes, self.sigma)
        self.layers_history.append(self.copy_layers())

    @staticmethod
    def sigmoid(x):
        return 1/(1 + np.exp(-x))

    @staticmethod
    def sigmoid_prime(x):
        sig = NNTrainer.sigmoid(x)
        return sig*(1-sig)

    