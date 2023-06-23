import os
import csv
import sys


def add_column_to_csvs(folder_path, column_name, value):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        temp_file_path = os.path.join(folder_path, 'temp_' + file_name)

        with open(file_path, 'r') as csv_file, open(temp_file_path, 'w', newline='') as temp_csv_file:
            reader = csv.reader(csv_file)
            writer = csv.writer(temp_csv_file)
            header = next(reader) 

            if column_name in header:
                print(f"Column '{column_name}' already exists in '{file_name}'. Skipping...")
                continue

            header.append(column_name)
            writer.writerow(header)

            for row in reader:
                row.append(value)
                writer.writerow(row)

        os.remove(file_path)
        os.rename(temp_file_path, file_path)

        print(f"Column '{column_name}' added to '{file_name}'.")


if len(sys.argv) != 4:
    print("Usage: python add_column_to_csv.py folder_path column_name value")
    sys.exit(1)

folder_path = sys.argv[1]
column_name = sys.argv[2]
value = sys.argv[3]

add_column_to_csv(folder_path, column_name, value)
