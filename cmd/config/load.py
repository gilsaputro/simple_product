import os
import yaml

class Config:
    def __init__(self, yaml_data):
        self.Postgres = Postgres(yaml_data.get('postgres', {}))
        self.Redis = Redis(yaml_data.get('redis', {}))

class Postgres():
    def __init__(self, yaml_data):
        self.Config = yaml_data.get('config', None)

class Redis():
    def __init__(self, yaml_data):
        self.Password = yaml_data.get('redis_password', None)
        self.Host =  yaml_data.get('redis_password', None)
        self.MaxIdle =  yaml_data.get('max_idle_in_sec', None)
        self.IdleTimeoutInSec =  yaml_data.get('idle_timeout_in_sec', None)

def get_config(values):
    # Read the YAML file into a dictionary
    config_path = os.path.join("config", "config.yaml")
    with open(config_path, "r") as file:
        config_data = file.read()

    # Replace yaml value with secret
    for k, v in values.items():
        config_data = config_data.replace(f"<{k}>", v)

    # Load the YAML into the Config object
    config_dict = yaml.safe_load(config_data)
    cfg = Config(config_dict)
    
    return cfg