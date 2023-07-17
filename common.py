import ujson
import binascii
import machine


def get_machine_id():
    machine_unique_hex = machine.unique_id()
    machine_unique_bytestring = binascii.hexlify(machine_unique_hex)
    machine_unique_string = machine_unique_bytestring.decode()
    return machine_unique_string


def get_config():
    config_file = open("config.json", "r")
    config = ujson.load(config_file)
    config_file.close()
    return(config[config_name])


def save_config(config):
    config_file = open("config.json", "w")
    config = ujson.dumps(config)
    config_file.write(config)
    config_file.close()
    print("Configuration Saved")
    return