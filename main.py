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


def read_plot_data_from_file(file_path):
    plot_data = []

    with open(file_path, 'r') as file:
        title = None
        plots = []

        for line in file:
            line = line.strip()

            if line:
                if line.startswith('['):
                    plot_info = eval(line)  
                    plots.append(plot_info)
                else:
                    if title and plots:
                        plot_data.append((title, plots))
                    title = line
                    plots = []

        if title and plots:
            plot_data.append((title, plots))

    return tuple(plot_data)


if __name__ == '__main__':

    dataframes_dict = {} 
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

        elif command == 'plot':
            plot_file = 'plot.txt'
            plot_data = read_plot_data_from_file(plot_file)

        # Add more commands here...

         elif command.startswith('filter'):

            command_parts = command.split()
            if len(command_parts) != 3:
                print("Invalid command format. Please provide 'filter <original-df-name> <filtered-df-name>'.")
                continue

            original_name = command_parts[1]
            filtered_name = command_parts[2]

            filter_file = 'filter.txt'
            original_df = dataframes_dict[original_name]
            filters = read_filters_from_file(filters_file)
            filtered_df = filter_dataframe_by_tuples(original_df, filters)
            dataframes_dict[filtered_name] = filtered_df

        else:
            print("Unknown command. Please try again.")

        command = ''