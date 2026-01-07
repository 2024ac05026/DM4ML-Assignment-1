import yaml

def load_paths(config_path="config/paths.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
