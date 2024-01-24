from sklearn.ensemble import ExtraTreesRegressor
import pickle


class ETR:
    MODELNAME = 'extratreesregressor'

    def __init__(self):
        self.random_state = 42
        self.n_est = 100
        self.reg = ExtraTreesRegressor(n_estimators=self.n_est, random_state=self.random_state)

    def train(self, X_train, y_train, X_val, y_val, sample_weights=None):
        print("Fitting the model...")
        self.reg.fit(X_train, y_train, sample_weight=sample_weights)
        print("Done fitting the model.")
        return self

    def train_warm_model(self, X_train, y_train, num_new_estimators):
        self.reg.set_params(n_estimators=self.reg.n_estimators+num_new_estimators, warm_start=True)
        print("Fitting the model...")
        self.reg.fit(X_train, y_train)
        print("Done fitting the model.")
        return self

    def set_params(self, params):
        for key, value in params.items():
            if hasattr(self, key):  # Check if attribute exists in the class
                setattr(self, key, value)
            else:
                print(f"Warning: {key} is not an attribute of this class. Ignoring...")
        self.reg = ExtraTreesRegressor(n_estimators=self.n_est, random_state=self.random_state)

    def set_warm_start(self, num_new_estimators, warm_start):
        self.reg.set_params(n_estimators=num_new_estimators, warm_start=warm_start)
        return self

    def save_model(self, file_name):
        pickle.dump(self.reg, open(str(file_name) + ".pkl", 'wb'))

    def load_model(self, file_name):
        with open(file_name, 'rb') as f:
            self.reg = pickle.load(f)

    def predict(self, y_test):
        return self.reg.predict(y_test)