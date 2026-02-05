import numpy as np

def compute_mse(b, w, data):
    arr = np.array(data, dtype=float)
    x = arr[:, 0]
    y = arr[:, 1]
    y_pred = w * x + b
    return float(np.mean((y_pred - y) ** 2))


def step_gradient(b, w, data, alpha):
    arr = np.array(data, dtype=float)
    N = arr.shape[0]

    x = arr[:, 0]
    y = arr[:, 1]

    y_pred = w * x + b
    error = y - y_pred

    db = (2.0 / N) * np.sum(error)
    dw = (2.0 / N) * np.sum(error * x)

    b_new = float(b - alpha * db)
    w_new = float(w - alpha * dw)
    return b_new, w_new


def fit(data, b, w, alpha, num_iterations):
    b_list = []
    w_list = []
    for _ in range(num_iterations):
        b, w = step_gradient(b, w, data, alpha)
        b_list.append(b)
        w_list.append(w)
    return b_list, w_list