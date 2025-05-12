import pandas as pd
from category_encoders import TargetEncoder
import pickle
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.decomposition import PCA
from .models import TrainTestData, MLModel
from django.core.files.base import ContentFile
from io import StringIO
from upload.models import Dataset
from .import load_models
from io import BytesIO
from sklearn import metrics


ctr_columns = ['site_id', 'site_domain', 'site_category', 'app_id', 'app_domain', 'app_category',
               'device_id', 'device_ip', 'device_model', 'C1', 'banner_pos', 'device_type',
               'device_conn_type', 'C14', 'C15', 'C16', 'C17','C18', 'C19', 'C20', 'C21',
               'hour_of_day', 'day_of_week', 'device_id_counts', 'device_ip_counts']

count_columns = ['device_id_counts', 'device_ip_counts', 'hourly_user_counts',
                 'weekly_user_counts', 'hourly_impression_counts', 'frequent_of_app_id',
                 'frequent_of_site_id']

target_columns = ctr_columns


# define columns
d1 = ['device_ip_ctr', 'device_id_ctr', 'site_id_target', 'C14_ctr','device_id_target']

d2 = ['device_ip_target', 'site_id_ctr', 'app_id_target', 'app_id_ctr',
'site_domain_ctr', 'device_id_counts_scaler', 'C14_target', 'C15_ctr',
'device_model_ctr', 'site_category_target', 'site_category_ctr',
'device_id_counts_ctr', 'app_domain_target', 'app_domain_ctr',
'frequent_of_app_id_scaler', 'site_domain_target',
'device_conn_type_target', 'C20_ctr', 'banner_pos_ctr', 'C17_ctr', 'C21_ctr',
'C21_target', 'banner_pos_target', 'device_ip_counts_scaler', 'C1_target',
'app_category_target', 'C20_target', 'C17_target', 'device_conn_type_ctr',
'frequent_of_site_id_scaler', 'C18_target', 'C18_ctr',
'hourly_user_counts_scaler', 'C16_target', 'C19_target',
'device_model_target', 'device_id_counts_target', 'device_ip_counts_target',
'C19_ctr', 'weekly_user_counts_scaler', 'hourly_impression_counts_scaler',
'app_category_ctr', 'C1_ctr', 'hour_of_day_target', 'C15_target',
'day_of_week_ctr', 'day_of_week_target', 'C16_ctr', 'hour_of_day_ctr',
'device_ip_counts_ctr', 'device_type_target', 'device_type_ctr']


# Train
def fit_ctr_encoding(df_train, columns, strategy='mean'):
    ctr_maps = {}
    for column in columns:
        group_data = df_train.groupby([column, 'click']).size().reset_index(name='count')
        pivot = group_data.pivot(index=column, columns='click', values='count').fillna(0)
        if 0 not in pivot.columns: pivot[0] = 0
        if 1 not in pivot.columns: pivot[1] = 0
        ctr = pivot[1] / (pivot[0] + pivot[1])
        if strategy == 'mean':
            ctr = ctr.fillna(ctr.mean())
        else:
            ctr = ctr.fillna(ctr.median())
        ctr_maps[column] = ctr
    return ctr_maps

# Apply to train/test
def transform_ctr_encoding(df, ctr_maps):
    data = pd.DataFrame(index=df.index)
    for column, ctr in ctr_maps.items():
        data[column + '_ctr'] = df[column].map(ctr).fillna(ctr.mean())
    return data



# Train
def fit_target_encoder(df_train, columns, smoothing=1):
    encoder = TargetEncoder(cols=columns, smoothing=smoothing)
    encoder.fit(df_train[columns], df_train['click'])
    return encoder

# Apply to train/test
def transform_target_encoding(df, encoder, columns):
    data = encoder.transform(df[columns])
    data.rename(columns={column: column + '_target' for column in columns}, inplace=True)
    data.fillna(-1, inplace=True)
    return data


# Train
def fit_min_max_scaler(df_train, columns):
    scaler = {}
    for column in columns:
        min_val = df_train[column].min()
        max_val = df_train[column].max()
        scaler[column] = (min_val, max_val)
    return scaler

# Apply to train/test
def transform_min_max_scaler(df, scaler):
    data = pd.DataFrame(index=df.index)
    for column, (min_val, max_val) in scaler.items():
        if min_val == max_val:
            data[column + '_scaler'] = 0
        else:
            data[column + '_scaler'] = (df[column] - min_val) / (max_val - min_val)
    return data


def pca(X_train, X_test):
    # get columns pca
    X_train_pca = X_train[d2]
    X_test_pca = X_test[d2]
    
    # pca
    pca = PCA(copy=True, iterated_power=100, n_components=25)
    X_train_pca_tf = pca.fit_transform(X_train_pca)
    X_test_pca_tf = pca.transform(X_test_pca)
    
    return X_train_pca_tf, X_test_pca_tf


def get_csv_content(data):
    csv_buffer = StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()
    return ContentFile(csv_content)


def create_train_test_data(instance, file):
    df = pd.read_csv(file)
    # train test
    group_data = df[['hour_of_day', 'device_id']].groupby('hour_of_day').count()
    df['hourly_user_counts'] = df['hour_of_day'].map(group_data['device_id'])

    group_data = df[['day_of_week', 'device_id']].groupby('day_of_week').count()
    df['weekly_user_counts'] = df['day_of_week'].map(group_data['device_id'])
    
    df['user'] = df['device_id'] + ',' + df['device_model']
    
    group_data = df[['hour_of_day', 'id']].groupby('hour_of_day').count()
    df['hourly_impression_counts'] = df['hour_of_day'].map(group_data['id'])
    
    df['frequent_of_app_id'] = df['user'].map(
        df.groupby('user')['app_id'].count() / df['app_id'].nunique()
    )
    
    df['frequent_of_site_id'] = df['user'].map(
        df.groupby('user')['site_id'].count() / df['site_id'].nunique()
    )
    
    # tran test split
    train, test = train_test_split(df, test_size=0.2, random_state=42)
    X_train, y_train = train.drop(['click'], axis=1), train['click']
    X_test, y_test = test.drop(['click'], axis=1), test['click']
    
    # scale
    scaler = fit_min_max_scaler(train, count_columns)
    encoder = fit_target_encoder(train, target_columns)
    ctr_maps = fit_ctr_encoding(train, ctr_columns)
    
    # X train
    try:
        X_train_fn = pd.concat([
            transform_min_max_scaler(X_train, scaler),
            transform_target_encoding(X_train, encoder, target_columns),
            transform_ctr_encoding(X_train, ctr_maps)], axis=1)
    except Exception as e:
        print(e)
        raise ValueError(str(e))
    # X test
    X_test_fn = pd.concat([
        transform_min_max_scaler(X_test, scaler),
        transform_target_encoding(X_test, encoder, target_columns),
        transform_ctr_encoding(X_test, ctr_maps)], axis=1)
    
    
    X_train_pca_tf, X_test_pca_tf = pca(X_train_fn[d2], X_test_fn[d2])
    
    pca_train_df = pd.DataFrame(X_train_pca_tf, index=X_train_fn.index)
    pca_test_df = pd.DataFrame(X_test_pca_tf, index=X_test_fn.index)
    X_train_fn = pd.concat([X_train_fn[d1], pca_train_df], axis=1)
    X_test_fn = pd.concat([X_test_fn[d1], pca_test_df], axis=1)
    
    train_test_data = TrainTestData(dataset=instance)
    train_test_data.X_train.save('X_train.csv', get_csv_content(X_train_fn))
    train_test_data.X_test.save('X_test.csv', get_csv_content(X_test_fn))
    train_test_data.y_train.save('y_train.csv', get_csv_content(y_train))
    train_test_data.y_test.save('y_test.csv', get_csv_content(y_test))
    
    train_test_data.save()
    

    
def training(user, dataset_name, selected_model, model_name):
    try:
        dataset = Dataset.objects.get(name=dataset_name)
        instance = TrainTestData.objects.get(dataset=dataset)
    except Dataset.DoesNotExist as e:
        raise ValueError(str(e))
    except TrainTestData.DoesNotExist as e:
        raise ValueError(str(e))
    
    X_train_file = instance.X_train.path
    y_train_file = instance.y_train.path
    
    try:
        X_train = pd.read_csv(X_train_file).values.astype(np.float32)
        y_train = pd.read_csv(y_train_file).values.ravel()
    except:
        raise ValueError('An error while reading csv file.')
    
    # train model
    if selected_model == 'logistic_regression':
        model = load_models.load_logistic_regression()
    elif selected_model == 'catboost':
        model = load_models.load_catboost_classifier()
    elif selected_model == 'random_forest':
        model = load_models.load_random_forest_classifier()
    elif selected_model == 'decision_tree':
        model = load_models.load_decision_tree_classifier()
    else:
        model = load_models.load_xgboost_classifier()
        
    model.fit(X_train, y_train)
    
    # save model
    try:
        model_name_path = f'{model_name}.pkl'
        model_buffer = BytesIO()
        pickle.dump(model, model_buffer)
        model_buffer.seek(0)
            
        model_file = ContentFile(model_buffer.read(), name=model_name_path)
            
        ml_model = MLModel.objects.create(
            user=user,
            name=model_name,
            model_type=selected_model,
            file=model_file,
        )
        ml_model.save()
    except:
        raise ValueError('An exception while saving model.')
    
    
def testing(dataset_name, model_name):
    try:
        dataset = Dataset.objects.get(name=dataset_name)
        instance = TrainTestData.objects.get(dataset=dataset)
    except Dataset.DoesNotExist as e:
        raise ValueError(str(e))
    except TrainTestData.DoesNotExist as e:
        raise ValueError(str(e))
    
    X_test_file = instance.X_test.path
    y_test_file = instance.y_test.path
    
    try:
        X_test = pd.read_csv(X_test_file).values.astype(np.float32)
        y_test = pd.read_csv(y_test_file).values.ravel()
    except:
        raise ValueError('An error while reading csv file.')
    
    try:
        model_instance = MLModel.objects.get(name=model_name)
        with model_instance.file.open('rb') as f:
            model = pickle.load(f)
    except MLModel.DoesNotExist as e:
        raise ValueError(str(e))
    
    # testing
    y_pred = model.predict(X_test)
    y_scores = model.predict_proba(X_test)[:, 1]
    
    accuracy = metrics.accuracy_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred)
    f1_macro = metrics.f1_score(y_test, y_pred, average="macro")
    f1_weighted = metrics.f1_score(y_test, y_pred, average="weighted")
    confusion_matrix = metrics.confusion_matrix(y_test, y_pred, labels=[1, 0])
    roc_auc = metrics.roc_auc_score(y_test, y_scores)
    
    
    result = {
        "Accuracy": round(accuracy, 2),
        "Precision": round(precision, 2),
        "Recall": round(recall, 2),
        "F1-Score": {
            "macro": round(f1_macro, 2),
            "weighted": round(f1_weighted, 2)
        },
        "ROC-AUC": round(roc_auc, 2),
        "confusion_matrix": confusion_matrix.tolist()
    }
    
    return result