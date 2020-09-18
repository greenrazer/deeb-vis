import numpy as np

inputs = np.array([
    [21, 13],
    [14, 12],
    [18.5, 16],
    [14, 14],
    [17.5, 15.5],
    [13, 11.5],
    [17.5, 12.5],
    [17.5, 11],
    [12, 9],
    [16, 13],
    [12, 10],
    [16, 12],
    [12, 10],
    [12.5, 16],
    [12, 14.5],
    [12.5, 13],
    [9.5, 11],
    [12.5,10],
    [9.5, 8.5],

    [5, 8.5],
    [6, 8],
    [10, 9],
    [4, 7.5],
    [16, 10.5],
    [70, 24],
    [54, 14],
    [20,14],
    [35,19],
    [21,12],
    [17,14.75],
    [27,11],
    [60,20],
    [25, 15],
])

labels = np.array([
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
    [0, 1],
])


def sigmoid(x):
    return 1/(1 + np.exp(-x))

def sigmoid_prime(x):
    sig = sigmoid(x)
    return sig*(1-sig)

def generate_layers(layers):
    out = []
    for l in range(len(layers)-1):
        step = {
            'weights': np.random.rand(layers[l], layers[l+1]),
            'bias': np.random.rand(1, layers[l+1]),
            'activation_function': sigmoid,
            'activation_function_prime': sigmoid_prime
        }
        out.append(step)
    return out

def forward_prop(layers, inp):
    history = []
    temp = inp
    history.append(temp)
    for l in layers:
        temp = temp @ l['weights'] + l['bias']
        history.append(temp)
        temp = l['activation_function'](temp)
        history.append(temp)
    return history

def back_prop(layers, hist, labels):
    dJd = []
    # derr/dw = derr/dsig * dsig/dz * dz/dW = x^T * -(sig(Wx + b) - label) * sig_prime(Wx + b)
    # derr/db = derr/dsig * dsig/dz * dz/db = -(sig(Wx + b) - label) * sig_prime(Wx + b) * 1
    layers_reversed = layers[::-1]
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


def update(layers, changes, sigma):
    for l in range(len(layers)):
        layers[l]['weights'] -= changes[l][0]*sigma
        layers[l]['bias'] -= changes[l][1]*sigma


change = 0.1
layers = generate_layers((2, 3,3,3,3,3,3, 2))
print(layers[0]['weights'])
for a in range(100000):
    hist = forward_prop(layers, np.array(inputs))
    changes = back_prop(layers, hist, np.array(labels))
    update(layers, changes, change)
print(layers[0]['weights'])

print(inputs[0], inputs[-1])

print(forward_prop(layers, np.array(inputs[-1]))[-1] )
print(forward_prop(layers, np.array(inputs[0]))[-1] )



    