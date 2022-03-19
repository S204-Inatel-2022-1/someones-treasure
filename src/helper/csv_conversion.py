import csv


def csv_to_matrix(csv_file_name):
    matrix = []
    with open(csv_file_name) as csv_file:
        reader = csv.reader(csv_file)
        for row_list in reader:
            matrix.append(row_list)
    return matrix
