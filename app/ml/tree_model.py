
from ml.ml_model_wrapper import MLModel
import numpy as np

class PredictModel(MLModel):

    def __init__(self):
        super().__init__()
        self.model = None
        self.ohe, self.scaler = self.load_preprocessing(['/home/akozhevnikov/dz/systemdisine/app/ml/models/preprocessing/data_ohe.pkl', 
                                                        '/home/akozhevnikov/dz/systemdisine/app/ml/models/preprocessing/data_scaler.pkl'])
        self.cat_features = ['Drug', 'Sex', 'Ascites', 'Hepatomegaly', 'Spiders', 'Edema']
    
    def preprosess(self, data):
        continius_data = self.scaler.transform(data.drop(self.cat_features, axis=1))
        cat_data = self.ohe.transform(data[self.cat_features].values).toarray()
        return np.concatenate((continius_data, cat_data), axis=1)
    
    def predict(self, data):
        return self.model.predict(self.preprosess(data))
    

class TreeModel(PredictModel):

    def __init__(self):
        super().__init__()
        self.model = self.load('/home/akozhevnikov/dz/systemdisine/app/ml/models/tree.pkl')


class KNNModel(PredictModel):

    def __init__(self):
        super().__init__()
        self.model = self.load('/home/akozhevnikov/dz/systemdisine/app/ml/models/knn.pkl')


class BoostingModel(PredictModel):

    def __init__(self):
        super().__init__()
        self.model = self.load('/home/akozhevnikov/dz/systemdisine/app/ml/models/boosting.pkl')