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

    return pd.concat(dataframes, ignore_index=True)

def filter_dataframe_by_tuples(df, filters):
    filtered_df = df.copy()
    
    for column, value in filters:
        filtered_df = filtered_df[filtered_df[column] == value]
    
    return filtered_df


def read_filters_from_file(file_path):
    filters = []
    
    with open(file_path, 'a') as file:
        pass
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                column, value = line.split('=')
                filters.append((column.strip(), value.strip()))
    
    return filters

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide the folder path as an argument.')
        sys.exit(1)

    folder_path = sys.argv[1]
    concatenated_dataframe = csvs_from_folder(folder_path)

    dataframes_dict = {}  # Dictionary to store DataFrames
    exit_program = False

    while not exit_program:
        command = input("Enter a command (or 'exit' to quit): ")

        if command == 'exit':
            exit_program = True

        elif command.startswith('concatenate'):
            command_parts = command.split()
            if len(command_parts) != 3:
                print("Invalid command format. Please provide 'concatenate <path> <name>'.")
                continue

            path = command_parts[1]
            name = command_parts[2]

            try:
                df = pd.read_csv(path)
                dataframes_dict[name] = df
                print(f"DataFrame '{name}' concatenated and saved successfully.")

            except FileNotFoundError:
                print("File not found. Please provide a valid file path.")

        # Add more commands here...

        else:
            print("Unknown command. Please try again.")

    # Example usage of the filtered_dataframe_by_tuples function
    filters_file = 'filter.txt'
    filters = read_filters_from_file(filters_file)
    filtered_df = filter_dataframe_by_tuples(concatenated_dataframe, filters)
    print(filtered_df)