import json


def get_config():
    with open('config.txt') as f:
        configurations = {}
        line = f.readlines()
        string_config = line[0]

        config = json.loads(string_config)

        return config


def save_config(config):
    s = json.dumps(config)
    print(s)
    with open('config.txt', 'w') as f:
        f.write(s)


