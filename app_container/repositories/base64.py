import base64
import csv
import io
import os


def to_csv(file):
    base64_data = file
    decoded_data = base64.b64decode(base64_data)
    csv_file = io.StringIO(decoded_data.decode('utf-8'))
    output_file_path = f"{os.getcwd()}\\app_container\\scripts\\csv_file.csv"

    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        reader = csv.reader(csv_file)

        # Iterate over the rows and write to the output file
        for row in reader:
            writer.writerow(row)
