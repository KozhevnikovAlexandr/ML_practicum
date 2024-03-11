import pickle

class MLModel():

    __instance = None

    def predict(self, data, *args, **kwargs):
        raise NotImplementedError

    def preprocess(self, data, *args, **kwargs):
        raise NotImplementedError

    def load(self, path):
        if self.__instance is None:
            with open(path, 'rb') as f:
                self.__instance = pickle.load(f)

        return self.__instance
    
    def load_preprocessing(self, paths):
        result = []
        for path in paths:
             with open(path, 'rb') as f:
                result.append(pickle.load(f))
        return result