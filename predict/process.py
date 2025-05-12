import pandas as pd
from models.utils import add_feature, transform_ctr_encoding, transform_min_max_scaler, transform_target_encoding, target_columns, pca, d1, d2
import numpy as np
import pickle
from sklearn.decomposition import PCA

def load_toolkits():
    with open(r'predict\toolkits\ctr_maps.pkl', 'rb') as f:
        ctr_maps = pickle.load(f)
    with open(r'predict\toolkits\encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)
    with open(r'predict\toolkits\scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
        
    return ctr_maps, encoder, scaler


def get_processed_data(df):
    ctr_maps, encoder, scaler = load_toolkits()
    df = add_feature(df)
    
    try:
        X = pd.concat([
            transform_min_max_scaler(df, scaler),
            transform_target_encoding(df, encoder, target_columns),
            transform_ctr_encoding(df, ctr_maps)], axis=1)
    except Exception as e:
        print(e)
        raise ValueError(str(e))
    
    pca = PCA(copy=True, iterated_power=100, n_components=25)
    X_pca_tf = pca.fit_transform(X[d2])
    
    return np.concatenate([X[d1], X_pca_tf], axis=1).astype(np.float32)