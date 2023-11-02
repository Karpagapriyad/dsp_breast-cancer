from sklearn.datasets import load_breast_cancer
import pandas as pd
import tensorflow_data_validation as tfdv
import os


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



# Function to validate data quality using TFDV for files in folder A
def validate_and_store_files(input_folder, output_folder_c, output_folder_b, database):
    # Get a list of CSV files in the input folder
    file_list = [file for file in os.listdir(input_folder) if file.endswith('.csv')]

    # Iterate through each CSV file in the input folder
    for file_name in file_list:
        input_file_path = os.path.join(input_folder, file_name)

        # Load data from CSV file
        data = pd.read_csv(input_file_path)

        # Perform data validation using TFDV
        stats = tfdv.generate_statistics_from_dataframe(dataframe=data)
        schema = tfdv.infer_schema(statistics=stats)
        anomalies = tfdv.validate_statistics(statistics=stats, schema=schema)

        # Check if data quality issues are found
        if not anomalies.total_anomalies:
            # No data quality issues found, store the file in folder C
            output_file_path_c = os.path.join(output_folder_c, file_name)
            data.to_csv(output_file_path_c, index=False)
            print(f'File stored in folder C: {output_file_path_c}')
        else:
            # Data quality issues found, store the file in folder B
            output_file_path_b = os.path.join(output_folder_b, file_name)
            data_with_issues = data[anomalies.row_anomalies()]
            data_without_issues = data.drop(index=data_with_issues.index)

            # Save the files with and without issues in folder B
            data_with_issues.to_csv(output_file_path_b, index=False)
            print(f'File with data issues stored in folder B: {output_file_path_b}')

            # Save data problems statistics in the database
            data_problem_stats = {
                'file_path': output_file_path_b,
                'total_anomalies': anomalies.total_anomalies,
                'column_anomalies': len(anomalies.schema_anomalies),
                # Add more statistics as needed
            }
            database.save_data_problem_stats(data_problem_stats)

            # Save the file without issues in folder C
            output_file_path_c = os.path.join(output_folder_c, file_name)
            data_without_issues.to_csv(output_file_path_c, index=False)
            print(f'File without data issues stored in folder C: {output_file_path_c}')


# Example usage of the function
# validate_and_store_files('folder_A', 'folder_C', 'folder_B', database)


output_directory = '/Users/karpagapriyadhanraj/Desktop/EPITA/DSP/dsp_breast-cancer/Folder-A/'
num_data_points_per_file = 100
save_breast_cancer_data(num_data_points_per_file, output_directory)
