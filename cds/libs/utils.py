def read_storage(file_path):
    with open(file_path) as file:
        return [line.strip() for line in file]
