import yaml

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_paths():
    return load_yaml("config/paths.yaml")

def load_db_config():
    return load_yaml("config/database.yaml")