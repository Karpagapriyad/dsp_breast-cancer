from sklearn.datasets import load_breast_cancer
import pandas as pd
import os

def save_breast_cancer_data(num_data_points_per_file, output_directory):
    data = load_breast_cancer()
    X, y = data.data, data.target
    num_csv_files = len(X) // num_data_points_per_file
    for i in range(num_csv_files):
        start_idx = i * num_data_points_per_file
        end_idx = (i + 1) * num_data_points_per_file
        subset_X = X[start_idx:end_idx]
        subset_y = y[start_idx:end_idx]
        df = pd.DataFrame(data=subset_X, columns=data.feature_names)
        df['target'] = subset_y
        file_name = os.path.join(output_directory, f'breast_cancer_data_{i + 1}.csv')
        df.to_csv(file_name, index=False)


output_directory = '/Users/karpagapriyadhanraj/Desktop/EPITA/DSP/dsp_breast-cancer/Folder-A/'
num_data_points_per_file = 100
save_breast_cancer_data(num_data_points_per_file, output_directory)
