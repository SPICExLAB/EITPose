import numpy as np


def scale_window_reshape(X_train, y_train, X_test, y_test, X_scaler, window_size, stride, shape='1d'):
    if X_scaler:
        X_train = X_scaler.fit_transform(X_train)
        X_test = X_scaler.transform(X_test)
    X_train_temp = []
    X_test_temp = []
    for i in range(0, X_train.shape[0]-window_size+1, stride):
        windowed_data = X_train[i:i+window_size, :]
        if shape == '1d':
            X_train_temp.append(windowed_data.flatten())
        elif shape == '2d':
            X_train_temp.append(windowed_data)
        elif shape == '3d':
            X_train_temp.append(windowed_data.reshape((windowed_data.shape[0], windowed_data.shape[1], 1)))
    X_train = np.array(X_train_temp)
    for i in range(0, X_test.shape[0]-window_size+1, stride):
        windowed_data = X_test[i:i+window_size, :]
        if shape == '1d':
            X_test_temp.append(windowed_data.flatten())
        elif shape == '2d':
            X_test_temp.append(windowed_data)
        elif shape == '3d':
            X_test_temp.append(windowed_data.reshape((windowed_data.shape[0], windowed_data.shape[1], 1)))
    X_test = np.array(X_test_temp)

    y_train = y_train[window_size-1:]
    y_test = y_test[window_size-1:]
    return X_train, y_train, X_test, y_test, X_scaler

