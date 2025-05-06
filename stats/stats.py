import json
import numpy as np
import pandas as pd

def get_item_counts(df):
    stats = dict()
    for column in df.columns:
        stats[column] = df[column].value_counts().to_dict()
        
    return stats

# def versus_click(df, column, target='click'):
#     group_data = df.groupby([column, target]).size().unstack()
#     group_data['Frequency'] = df[column].value_counts(normalize=True)
#     ctr = group_data[1] / (group_data[0] + group_data[1])
#     group_data['CTR'] = ctr
#     group_data = group_data.fillna(0)
    
#     return group_data.to_dict()


def get_stats(df):
    stats = {
        'click_distribution': df['click'].value_counts().to_dict(),
        'count_unique_per_column': df.nunique().to_dict(),
        'item_counts': get_item_counts(df),
        'corr': df.select_dtypes('number').corr().fillna(0).round(4).to_dict()
    }
    return stats


