from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression

LOGISTIC_REGRESSION_PARAMS = {
    'solver': 'lbfgs',
    'penalty': 'l2',
    'C': 2.667777777777778,
    'class_weight': None,
    'fit_intercept': True,
    'max_iter': 5000
}
RANDOM_FOREST_CLASSIFIER_PARAMS = {
    'n_estimators': 200,
    'criterion': 'gini',
    'bootstrap': False,
    'max_depth': 20,
    'max_features': 'sqrt'
}
XGBOOST_CLASSIFIER_PARAMS = {
    'objective': 'binary:logistic',
    'tree_method': 'hist',
    'device': 'cuda',
    'use_label_encoder': False,
    'eval_metric': 'logloss',
    'subsample': 1.0,
    'reg_lambda': 2.5,
    'reg_alpha': 10,
    'n_estimators': 500,
    'min_child_weight': 3,
    'max_depth': 6,
    'learning_rate': 0.2,
    'colsample_bytree': 0.6,
    'gamma': 0.3
}
CATBOOST_CLASSIFIER_PARAMS = {
    'iterations': 1000,
    'learning_rate': 0.05,
    'depth': 8,
    'task_type': 'GPU',
    'devices': '0',
    'random_seed': 42,
    'verbose': 100
}
DECISION_TREE_CLASSIFIER_PARAMS = {
    'criterion': 'entropy',
    'splitter': 'best',
    'max_depth': 10,
    'min_samples_split': 4,
    'min_samples_leaf': 2,
    'max_features': 'sqrt',
    'random_state': 42
}

def load_logistic_regression():
    return LogisticRegression(**LOGISTIC_REGRESSION_PARAMS)

def load_random_forest_classifier():
    return RandomForestClassifier(**RANDOM_FOREST_CLASSIFIER_PARAMS)

def load_decision_tree_classifier():
    return DecisionTreeClassifier(**DECISION_TREE_CLASSIFIER_PARAMS)

def load_catboost_classifier():
    return CatBoostClassifier(**CATBOOST_CLASSIFIER_PARAMS)

def load_xgboost_classifier():
    return XGBClassifier(**XGBOOST_CLASSIFIER_PARAMS)