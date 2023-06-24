import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def csvs_from_folder(folder_path):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    dataframes = []

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=False)


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
        title = []
        plots = []
        plot_data = []

        for line in file:
            line = line.strip()

            if line:
                if line.startswith('|'):
                    plot_info = line.split('|')
                    plot_info.pop(0) 
                    plot = [p.split(',') for p in plot_info]
                    plots.append(plot)
                    
                else:
                    title.append(line)

        for title, plot_info in zip(title, plots):
            plot_data.append((title, plot_info))

    return tuple(plot_data)

def create_subplots(data, dataframes_dict):
    num_rows = len(data)
    num_cols = len(data[0][1])

    if num_rows == 1 and num_cols == 1:
        fig, axes = plt.subplots()
    else:
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 10))

    for i, (title, plots) in enumerate(data):
        if num_rows == 1:
            ax = axes[j]
            for j, plot_info in enumerate(plots):
                dataframe_key, coluna_plot, coluna_variavel, titulo = plot_info

                df = dataframes_dict[dataframe_key]
                unique_values = df[coluna_variavel].unique()

                for value in unique_values:
                    subset_df = df[df[coluna_variavel] == value]
                    ax.plot(subset_df[coluna_plot], label=str(value))

            ax.set_title(titulo)
            ax.legend()
        else:
            for j, plot_info in enumerate(plots):
                ax = axes[i, j]
                dataframe_key, coluna_plot, coluna_variavel, titulo = plot_info

                df = dataframes_dict[dataframe_key]
                unique_values = df[coluna_variavel].unique()

                for value in unique_values:
                    subset_df = df[df[coluna_variavel] == value]
                    ax.plot(subset_df[coluna_plot], label=str(value))

                ax.set_title(titulo)
                ax.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    dataframes_dict = {} 
    exit_program = False

    while not exit_program:
        command = input("Enter a command (or 'exit' or to quit): ")

        if command == 'exit' or command == 'quit':
            exit_program = True

        elif command.startswith('concatenate'):
            command_parts = command.split()
            if len(command_parts) != 3:
                print("Invalid command format. Please provide 'concatenate <path> <name>'.")
                continue

            path = command_parts[1]
            name = command_parts[2]

            try:
                df = csvs_from_folder(path)
                dataframes_dict[name] = df
                print(f"DataFrame '{name}' concatenated and saved successfully.")

            except FileNotFoundError:
                print("File not found. Please provide a valid file path.")

        elif command == 'plot':
            plot_file = 'plot.txt'
            plot_data = read_plot_data_from_file(plot_file)
            create_subplots(plot_data, dataframes_dict)

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