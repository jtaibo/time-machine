#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#	Web interface using Flask
#
#	See:
#		https://pythonprogramming.net/jquery-flask-tutorial/
#
#

from globalconfig import GlobalConfig
from flask import Flask, render_template, jsonify, request
import monitor
import audio
import datetime
import threading
import time
from subprocess import call

app = Flask(__name__)


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
    
def round_component(v):
    if v > 127:
      return 255
    else:
      return 0
    
def rgb_round_up(rgb):
    return ( round_component(rgb[0]), round_component(rgb[1]), round_component(rgb[2]) )


def flaskThread():
#    app.run(host='192.168.0.46', port=80, debug=True)
    app.run(host='192.168.0.46', port=8080, debug=False)

def start(rels, nix):
    global relays
    global nixies
    relays = rels
    nixies = nix
    threading.Thread(target=flaskThread).start()


@app.route("/")
def index():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   leds_color = rgb_to_hex( tuple([255*x for x in nixies.getLEDColor() ]) )
   volume = audio.getVolume()
   templateData = {
      'title' : 'Time Machine(TM)',
      'time': timeString,
      'cpu_temp': monitor.get_cpu_temp(),
      'gpu_temp': monitor.get_gpu_temp(),
      'other_temp': monitor.get_gputemp_from_gpiozero(),
      'uptime_line': monitor.get_uptime_line(),
      'cpu_load': monitor.get_cpuload(),
      'ram': monitor.get_ram(),
      'connections': monitor.get_connections(),
      'ip_address': monitor.get_ipaddress(),
      'uptime': monitor.get_uptime(),
      'relays': [ relays.getState(0), relays.getState(1), relays.getState(2), relays.getState(3), relays.getState(4), relays.getState(5), relays.getState(6), relays.getState(7) ],
      'lamp_leds_color': leds_color,
      'volume': volume,
      'seconds_sound': GlobalConfig.seconds_sound
      }
   return render_template('index.html', **templateData)

@app.route("/_relay")
def relay():
  print("Switching relay")
  try:
    ch = request.args.get('channel', 0, type=int)
    relays.toggle(ch-1)
#    time.sleep(.2)
    return(jsonify(result=relays.getState(ch-1)))
  except Exception as e:
    return str(e)

@app.route("/_setColor")
def setColor():
  print("Setting color")
  try:
    hex_col = request.args.get('color')
    col = hex_to_rgb(hex_col)
    rnd_col = rgb_round_up(col)

    # Set LEDs color
    print("Setting LEDs to ", rnd_col[0]/255, rnd_col[1]/255, rnd_col[2]/255)
    nixies.setLEDColor( int(rnd_col[0]/255), int(rnd_col[1]/255), int(rnd_col[2]/255) )

    result_col = rgb_to_hex(rnd_col)
    return(jsonify(result=result_col))
  except Exception as e:
    return str(e)

@app.route("/_setVolume")
def setVolume():
  try:
    volume = int( request.args.get('volume') )
    audio.setVolume( volume )
    return(jsonify(result=volume))
  except Exception as e:
    return str(e)

@app.route("/_gladosQuote")
def gladosQuote():
  print("GLaDOS quote")
  try:
    call("./glados_quotes.sh", shell=True)
    return(jsonify(result="OK"))
  except Exception as e:
    return str(e)

@app.route("/_setConfig")
def setConfig():
  print("Set config")
  try:
    seconds_sound=request.args.get('seconds_sound')
    GlobalConfig.seconds_sound= int(seconds_sound)
    return(jsonify(seconds_sound=GlobalConfig.seconds_sound))
  except Exception as e:
    return str(e)

@app.route("/_pwrdwn")
def pwrdwn():
  print("SHUTDOWN Requested!")
  call("sudo poweroff", shell=True)
  return(jsonify(result="Power down requested"))


if __name__ == "__main__":

#    app.run(host='192.168.0.46', port=80, debug=True)
    app.run(host='192.168.0.46', port=8080, debug=True)
