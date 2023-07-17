from machine import Pin, SoftI2C, SoftSPI
from time import sleep
import os
import common
import ujson
import gc
import dht
from bmp180 import BMP180
import mfrc522
import bh1750


def test():
    print("This is inside the test function.")
    return("This is outside the test function")


def get_dht(dht_config): 
    dht22_object = dht.DHT22(Pin(dht_config["pin"]))    
    dht22_object.measure()
    temperature = dht22_object.temperature()
    humidity = dht22_object.humidity()    
    dht22_reading = {
        'temperature': temperature,
        'humidity': humidity
        }    
    return dht22_reading


def setup_am312(am312_config):
    am312_pinobject = Pin(am312_config["pin"], Pin.IN)
    return am312_pinobject


def get_am312(am312_pinobject):    
    return_object = {
        'motion': am312_pinobject.value()
    }
    return(return_object)


def setup_sw520d(sw520d_config):
    sw520d_pinobject = Pin(sw520d_config["pin"], Pin.IN)
    return sw520d_pinobject


def get_sw520d(sw520d_pinobject):    
    return_object = {
        'motion': sw520d_pinobject.value()
    }
    return(return_object)


def setup_bmp180(bmp180_config):
    bus = SoftI2C(
        scl=Pin(bmp180_config["scl"]),
        sda=Pin(bmp180_config["sda"]),
        freq=bmp180_config["frequency"],
        timeout=bmp180_config["timeout"]
        )
    bmp180 = BMP180(bus)
    bmp180.oversample_sett = bmp180_config["oversample"]
    bmp180.baseline = bmp180_config["baseline"]
    return(bmp180)

    
def get_bmp180(bmp180_bus):
    temperature = bmp180_bus.temperature
    pressure = bmp180_bus.pressure
    altitude = bmp180_bus.altitude
    bmp180_reading = {
        "temperature": temperature,
        "presssure": pressure,
        "altitude" : altitude
        }
    return bmp180_reading


def setup_mfrc522(mfrc522_config):
    config_sck = Pin(mfrc522_config["sck"])
    config_mosi = Pin(mfrc522_config["mosi"])
    config_miso = Pin(mfrc522_config["miso"])
    config_reset = Pin(mfrc522_config["reset"], Pin.OUT)
    config_baudrate = mfrc522_config["baudrate"]
    config_polarity = mfrc522_config["polarity"]
    config_phase = mfrc522_config["phase"]
    
    spi = SoftSPI(
        baudrate = config_baudrate,
        polarity = config_polarity,
        phase = config_phase,
        sck = config_sck,
        mosi = config_mosi,
        miso = config_miso
        )
    sda = config_reset
    reader = mfrc522.MFRC522(spi, sda)
    return(reader)
    
    
def get_mfrc522(reader):
    uid = ""
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, raw_uid) = reader.anticoll()
        if stat == reader.OK:
            uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            return(uid)
        
        
def write_mfrc522(reader):    
    while True:
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, raw_uid) = reader.anticoll()
            if stat == reader.OK:
                print("New card detected")
                print("  - tag type: 0x%02x" % tag_type)
                print("  - uid   : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print("")

                if reader.select_tag(raw_uid) == reader.OK:
                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                    if reader.auth(reader.AUTHENT1A, 8, key, raw_uid) == reader.OK:
                        stat = reader.write(8, b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f")
                        reader.stop_crypto1()
                        if stat == reader.OK:
                            print("Data written to card")
                        else:
                            print("Failed to write data to card")
                    else:
                        print("Authentication error")
                else:
                    print("Failed to select tag")


def setup_bh1750(bh1750_configuration):
    config_sda = Pin(bh1750_configuration["sda"])
    config_scl = Pin(bh1750_configuration["scl"])
    i2c = SoftI2C(sda=config_sda, scl=config_scl)
    bh1750_object = bh1750.BH1750(0x23, i2c)
    return(bh1750_object)


def get_bh1750(bh1750_object):
    measurement = bh1750_object.measurement
    return(measurement)


def save_relay_state(state):
    config_file = open("config.json")    
    config = ujson.load(config_file)
    config_file.close()
    config["relay"]["relaystate"] = int(state)
    new_config = ujson.dumps(config)
    os.remove("config.json")
    config_file = open("config.json", "w")
    config_file.write(ujson.dumps(config))
    config_file.close()
    print("Relay State Saved")
    return()

def set_relay(relay_config, state):
    relay = Pin(relay_config["pin"], Pin.OUT)
    save_relay_state(state)
    sleep(0.3)
    relay.value(state)
    return()


