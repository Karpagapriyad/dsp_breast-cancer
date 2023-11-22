import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

target = 'tumor type'
feature_list = ['mean radius', 'mean texture', 'mean perimeter', 'mean area']


# This function checks if the data is train or test and sieves it into required data out of the chunk
def sieve_data(df):
    if target in df.columns:
        sieved_data = df[feature_list].join(df[target])

    else:
        sieved_data = df[feature_list]

    return sieved_data


def drop_missing_rows(df):
    complete_rows = df.dropna()
    return complete_rows


def scale_numeric(df):

  scaler = joblib.load("scaler_lri.joblib")
  scaled_data = scaler.transform(df[feature_list])
  scaled_df = pd.DataFrame(data=scaled_data, columns=feature_list)

  return scaled_df


def preprocessing(df):
    output_sieve = sieve_data(df)
    output_drop = drop_missing_rows(output_sieve)
    return output_drop
