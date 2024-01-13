import pandas as pd

import great_expectations as gx
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.data_context.types.resource_identifiers import ExpectationSuiteIdentifier
from great_expectations.exceptions import DataContextError
from great_expectations.core.batch import BatchRequest
import os
import csv

def validate_data(file_path, df):
    context = gx.get_context()
    batch_request = {'datasource_name': 'great_expectation_datasource', 'data_connector_name': 'default_inferred_data_connector_name', 'data_asset_name': 'breast_cancer_data_1.csv', 'limit': 5000}
    expectation_suite_name = "breast_cancer_expectation_suite"
    try:
        suite = context.get_expectation_suite(expectation_suite_name=expectation_suite_name)
    except DataContextError:
        suite = context.add_expectation_suite(expectation_suite_name=expectation_suite_name)
        
    validator = context.get_validator(
    batch_request=BatchRequest(**batch_request),
    expectation_suite_name=expectation_suite_name
    )
    
    validator.expect_column_values_to_not_be_null(column=["mean radius", "mean texture", "mean perimeter", "mean area"])

    result_format: dict = {
    "result_format": "COMPLETE",
    "unexpected_index_column_names": ["mean radius", "mean texture", "mean perimeter", "mean area", "mean smoothness", "mean compactness", "mean concavity", "mean concave points", "mean symmetry", "mean fractal dimension", "radius error", "texture error", "perimeter error", "area error", "smoothness error", "compactness error", "concavity error", "concave points error", "symmetry error", "fractal dimension error", "worst radius", "worst texture", "worst perimeter", "worst area", "worst smoothness", "worst compactness", "worst concavity", "worst concave points", "worst symmetry", "worst fractal dimension", "target"],
    }
    
    validation_result = validator.validate(result_format = result_format)
    return validation_result

def save_validate_data(df):
    validation_result = validate_data(file_path, df)
    if validation_result['results'] is False:
        invalid_indexes = []
        for result in validation_result['results']:
            invalid_index_df = result['result']['unexpected_index_query']
            invalid_index = invalid_index_df.replace('df.filter(items=[', '')
            invalid_index = invalid_index.replace('], axis=0)', '')
            split = invalid_index.split(", ")
            invalid_list = list(map(int, split))
            in_first = set(invalid_indexes)
            in_second = set(invalid_list)
    
            in_second_but_not_in_first = in_second - in_first
            
            invalid_indexes = invalid_indexes + list(in_second_but_not_in_first)
            df.drop(invalid_indexes)
            with open(folder_c+"\\"+file_name, 'w', newline='') as csv_file:
                csv.writer(csv_file)
            df.to_csv(folder_c+"\\"+file_name, index=False)
    else:
        with open(folder_c+"\\"+file_name, 'w', newline='') as csv_file:
            csv.writer(csv_file)
        df.to_csv(folder_c+"\\"+file_name, index=False)
        
file_path = "Folder-A/breast_cancer_data_2.csv"
file_name = "breast_cancer_data_2.csv"
folder_c = "Folder-C"
df = pd.read_csv(file_path)         
save_validate_data(df)