import pandas as pd

def processed_dataset(df):
    # convert to datetime
    df['hour'] = pd.to_datetime(df['hour'])
    df['hour_of_day'] = df['hour'].dt.hour
    df['day_of_week'] = df['hour'].dt.dayofweek
    
    # device_id_counts
    device_id_counts = df['device_id'].value_counts()
    df['device_id_counts'] = df['device_id'].map(device_id_counts)
    
    # device_id_counts
    device_ip_counts = df['device_ip'].value_counts()
    df['device_ip_counts'] = df['device_ip'].map(device_ip_counts)
    
    # hourly_user_ip_count
    hourly_counts = df.groupby('hour_of_day')['device_ip'].count()
    df['hourly_user_ip_count'] = df['hour_of_day'].map(hourly_counts)
    
    # hourly_user_ip_count
    weekly_counts = df.groupby('day_of_week')['device_ip'].count()
    df['hourly_user_ip_count'] = df['day_of_week'].map(weekly_counts)
    
    return df