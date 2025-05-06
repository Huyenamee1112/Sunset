from functools import lru_cache
from upload.models import Dataset
import pandas as pd

@lru_cache(maxsize=1)
def get_df(user):
    instance = Dataset.objects.filter(user=user).first()
    if not instance:
        return None
    return pd.read_csv(instance.file.path)
