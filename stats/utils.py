from functools import lru_cache
from upload.models import Dataset
import pandas as pd

@lru_cache(maxsize=128)
def get_df_cached(dataset_id, updated_at_str):
    instance = Dataset.objects.filter(id=dataset_id).first()
    if not instance:
        return None
    return pd.read_csv(instance.processed_data.file.path)


def get_df(user_id):
    instance = Dataset.objects.filter(user__id=user_id).first()
    if not instance:
        return None
    if instance.profiles.exists():
        profile = instance.profiles.first()
        return get_df_cached(instance.id, str(profile.updated_at))
    return None
