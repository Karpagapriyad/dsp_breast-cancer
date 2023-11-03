from sklearn.datasets import load_breast_cancer
from sklearn.impute import SimpleImputer
from db_connection import connect_to_database()
from Test_Connection import insert_not_quality_data(file_name, negative_value_count, missing_value_count)
import pandas as pd
import os
import psycopg2


def save_breast_cancer_data(num_data_points, directory_a):
    data = load_breast_cancer()
    X, y = data.data, data.target
    num_csv_files = len(X) // num_data_points
    for i in range(num_csv_files):
        start_idx = i * num_data_points
        end_idx = (i + 1) * num_data_points
        subset_X = X[start_idx:end_idx]
        subset_y = y[start_idx:end_idx]
        df = pd.DataFrame(data=subset_X, columns=data.feature_names)
        df['target'] = subset_y
        file_name = os.path.join(directory_a, f'breast_cancer_data_{i + 1}.csv')
        df.to_csv(file_name, index=False)


def validate_and_store_files(input_folder, output_folder_good, output_folder_bad, database):
    # List all CSV files in the input folder
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    # Initialize SimpleImpute to check for missing values
    impute = SimpleImputer(strategy='constant', fill_value=None)

    conn = psycopg2.connect(**database)
    cursor = conn.cursor()

    for file in csv_files:
        file_path = os.path.join(input_folder, file)
        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(file_path)

        # Check for missing values in the DataFrame
        if (data < 0).any().any() or data.isnull().values.any():
            # If negative or missing values are found, move the file to the bad data folder
            output_path = os.path.join(output_folder_bad, file)
            data.to_csv(output_path, index=False)

            # Store statistics about negative and missing values in the database
            negative_value_count = (data < 0).sum().sum()
            missing_value_count = data.isnull().sum().sum()
            cursor.execute(insert_not_quality_data(file, negative_value_count, missing_value_count))
            conn.commit()
        else:
            # If no negative or missing values are found, move the file to the good data folder
            output_path = os.path.join(output_folder_good, file)
            data.to_csv(output_path, index=False)

            # Close database connection
        cursor.close()
        conn.close()


connection = connect_to_database

folder_a = '/Users/karpagapriyadhanraj/Desktop/EPITA/DSP/dsp_breast-cancer/Folder-A/'
folder_b = '/Users/karpagapriyadhanraj/Desktop/EPITA/DSP/dsp_breast-cancer/Folder-C'
folder_c = '/Users/karpagapriyadhanraj/Desktop/EPITA/DSP/dsp_breast-cancer/Folder-B'

num_data_points_per_file = 100
save_breast_cancer_data(num_data_points_per_file, folder_a)
validate_and_store_files(folder_a, folder_c, folder_b, connection)
