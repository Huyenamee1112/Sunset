from functools import lru_cache
import pandas as pd

@lru_cache(maxsize=1)
def get_df():
    return pd.read_csv("data/data.csv")
