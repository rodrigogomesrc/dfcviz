import os
import sys
import pandas as pd

def csvs_from_folder(folder_path):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    dataframes = []

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        dataframes.append(df)

    concatenated_df = pd.concat(dataframes, ignore_index=True)

    return concatenated_df

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide the folder path as an argument.')
        sys.exit(1)

    folder_path = sys.argv[1]
    concatenated_dataframe = csvs_from_folder(folder_path)
    print(concatenated_dataframe)
