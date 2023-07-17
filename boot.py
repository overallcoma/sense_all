import ujson
import senseall
import common


config_file = open("config.json")
configuration = ujson.load(config_file)

sensors.set_relay(configuration["relay"], configuration["relay"]["relaystate"])