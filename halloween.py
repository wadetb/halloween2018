import os
import importlib
import subprocess
from time import sleep

from flask import Flask
from flask import render_template, request
app = Flask(__name__)

import smbus

bus = smbus.SMBus(1)

STRIP_ADDR = 7
STRIP_CMD_ADD_FX = 1

STRIP_BOLT = 0
STRIP_FLASH = 1

def pack_short(v):
    return [v >> 8, v & 0xff]

def pack_fixed(v):
    return pack_short(int(v * 16))

def pack_fx_fields(f):
    return (pack_fixed(f['position']) +
        pack_fixed(f['length']) +
        pack_fixed(f['spread']) + 
        pack_fixed(f['r']) +
        pack_fixed(f['g']) +
        pack_fixed(f['b']))

def strip_add_fx(strip, fx):
    bus.write_i2c_block_data(STRIP_ADDR, STRIP_CMD_ADD_FX,
        pack_short(strip) + 
        pack_short(fx['delay']) +
        pack_short(fx['lifetime']) +
        pack_fx_fields(fx['start']) +
        pack_fx_fields(fx['velocity']))

VOLDY_ADDR = 8
VOLDY_CMD_SET_LED = 1
VOLDY_CMD_CALIBRATE_ARM = 2
VOLDY_CMD_CALIBRATE_HEAD = 3
VOLDY_CMD_SET_ARM = 4
VOLDY_CMD_SET_HEAD = 5
VOLDY_CMD_CLEAR_LED = 6
VOLDY_CMD_CLEAR_ARM = 7
VOLDY_CMD_CLEAR_HEAD = 8

def voldy_do(cmd, arg0, arg1, arg2):
    bus.write_i2c_block_data(VOLDY_ADDR, cmd, [
        arg0 >> 8, arg0 & 0xff,
        arg1 >> 8, arg1 & 0xff,
        arg2 >> 8, arg2 & 0xff])

def set_led(on, duration):
    voldy_do(VOLDY_CMD_SET_LED, on, duration, 0)

def cab_arm(delta):
    voldy_do(VOLDY_CMD_CALIBRATE_ARM, delta, 0, 0)

def cab_head(delta):
    voldy_do(VOLDY_CMD_CALIBRATE_HEAD, delta, 0, 0)

def clear_led():
    voldy_do(VOLDY_CMD_CLEAR_LED, 0, 0, 0)

def clear_arm():
    voldy_do(VOLDY_CMD_CLEAR_ARM, 0, 0, 0)

def clear_head():
    voldy_do(VOLDY_CMD_CLEAR_HEAD, 0, 0, 0)

def set_arm(target, duration, slowness):
    voldy_do(VOLDY_CMD_SET_ARM, target, duration, slowness)

def set_head(target, duration, slowness):
    voldy_do(VOLDY_CMD_SET_HEAD, target, duration, slowness)

# SPEAKER_DEV = "bluealsa:HCI=hci0,DEV=90:C6:82:02:78:19,PROFILE=a2dp" # Stormtrooper
SPEAKER_DEV = "sysdefault"

def play_sound(audio_file):
    cmd = "aplay -D {} {}".format(SPEAKER_DEV, audio_file)
    subprocess.Popen(cmd, shell=True)

@app.route('/reboot')
def reboot():
    subprocess.check_output('sudo shutdown -r now', shell=True)
    return "OK"

@app.route('/wifi')
def wifi():
    iwconfig_out = subprocess.check_output(['iwconfig'])
    return render_template('wifi.html', iwconfig_out=iwconfig_out)

def get_fx():
    #importlib.invalidate_caches()
    fx_module = importlib.import_module('fx')
    reload(fx_module)
    return getattr(fx_module, 'EFFECTS')

@app.route('/')
def index():
    local_ip = subprocess.check_output("ip addr show wlan0 | grep -Po 'inet \K[\d.]+'", shell=True)
    #effects = [name.split('.')[0] for name in os.listdir('.') if name.endswith('.wav')] 
    fx = get_fx()
    return render_template('halloween.html', local_ip=local_ip, effects=sorted(fx.keys()))

@app.route('/play')
def play():
    fx = get_fx()
    f = fx[request.args.get('effect')]
    f()
    return "OK"
