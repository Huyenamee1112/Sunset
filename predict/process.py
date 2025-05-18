import pandas as pd
from models.utils import add_feature, transform_ctr_encoding, transform_min_max_scaler, transform_target_encoding, target_columns, d1, d2
import numpy as np
import pickle
from sklearn.decomposition import PCA
import os
import gdown

def download_large_file(url, file_path):
    print("Downloading large file...")
    if "file/d/" in url:
        file_id = url.split("file/d/")[1].split("/")[0]
        url = f"https://drive.google.com/uc?id={file_id}"
        print(url)
    gdown.download(url, file_path, quiet=False)


def load_toolkits():
    ctr_maps = r'predict\toolkits\ctr_maps.pkl'
    encoder = r'predict\toolkits\encoder.pkl'
    scaler = r'predict\toolkits\scaler.pkl'
    
    if not os.path.exists(ctr_maps):
        download_large_file('https://drive.google.com/file/d/1-929DjQVxJ3K3c-bGbORvx-hr9SB6PAk/view?usp=drive_link', ctr_maps)
        print('download ctr_maps.pkl successfully!')
    if not os.path.exists(encoder):
        download_large_file('https://drive.google.com/file/d/1-BYTPUt5r8Uxd9K5G1Y5sAJjONOpXpxj/view?usp=drive_link', encoder)
        print('download encoder.pkl successfully!')
    if not os.path.exists(scaler):
        download_large_file('https://drive.google.com/file/d/1-JkmNR4R8eg0PKJkJkopC5dytQESyCry/view?usp=drive_link', scaler)
        print('download scaler.pkl successfully!')
        
    with open(ctr_maps, 'rb') as f:
        ctr_maps = pickle.load(f)
    with open(encoder, 'rb') as f:
        encoder = pickle.load(f)
    with open(scaler, 'rb') as f:
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