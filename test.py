import sense_all
import common
from utime import sleep


# Configuration Load
config_file = open("config.json", "r")
configuration = ujson.load(config_file)
sense_all.test()


# DHT22 - Temperature + Humidity

# DHT22_reading = sense_all.get_dht(configuration["dht22"])
# print(DHT22_reading)


# AM312 - PIR Human Sensor

# AM312 = sense_all.setup_am312(configuration["am312"])
# x = 0
# while x <= 5:
#     AM312_reading = sense_all.get_am312(AM312)    
#     print(AM312_reading)
#     x = x + 1
#     sleep(1)


# SW520D - Tilt Sensor

# if isinstance(configuration["sw520d"]["pin"], list):
#     sw520d_sensors = []
#     for config in configuration["sw520d"]["pin"]:
#         config_value = {"pin": config}
#         configured_sensor = sense_all.setup_sw520d(config_value)
#         sw520d_sensors.append(configured_sensor)
#     x = 0
#     while x <= 10:
#         for sw520d_sensor in sw520d_sensors:
#             sw520d_reading = sense_all.get_sw520d(sw520d_sensor)
#             print(sw520d_reading)
#             x = x + 1
#             sleep(1)
    

# for sensor in sense_all.setup_sw520d(configuration["sw520d"]):
#     while x <= 10:
#         SW520D_reading = sense_all.get(sensor)
#         print(SW520D_reading)
#         x = x + 1
#         sleep(0.5)

# SW520D = sense_all.setup_sw520d(configuration["sw520d"])
# x = 0
# while x <= 5:
#     for sensor in SW520D:
#         SW520D_reading = sense_all.get_sw520d(SW520D)    
#         print(SW520D_reading)
#         x = x + 1
#         sleep(1)


# BMP180 - Temperature, Pressure, Altitude

# BMP180 = sense_all.setup_bmp180(configuration["bmp180"])
# bmp180_reading = sense_all.get_bmp180(BMP180)
# print(bmp180_reading)


#MFRC522 - NFC Reader

# MFRC522 = sense_all.setup_mfrc522(configuration["mfrc522"])
# MFRC522_reading = sense_all.get_mfrc522(MFRC522)
# print(MFRC522_reading)


#BH1750 - Ambient Light

# BH1750 = sense_all.setup_bh1750(configuration["bh1750"])
# BH1750_reading = sense_all.get_bh1750(BH1750)
# print(BH1750_reading)


# RELAY = NC/NO Relay Signal

# Turn Off
sense_all.set_relay(configuration["relay"], configuration["relay"]["alarmstate"])
# Wait a few seconds
sleep(1)
sleep(1)
sleep(1)
# Turn On
sense_all.set_relay(configuration["relay"], configuration["relay"]["safestate"])

# Next Thing                                                                                                                                                                                                                                                     ZS