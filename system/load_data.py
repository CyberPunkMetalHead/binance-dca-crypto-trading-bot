import yaml

def load_data(file):
    with open(file) as file:
        return yaml.load(file, Loader=yaml.FullLoader)
