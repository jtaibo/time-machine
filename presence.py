#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#	Presence detection
#

from globalconfig import GlobalConfig
import threading
import time
import RPi.GPIO as GPIO


class Presence(threading.Thread):

    #def __init__(self, nixies, relays):
    def __init__(self):
      GPIO.setmode(GlobalConfig.GPIO_mode)
      GPIO.setup(GlobalConfig.pir_pin, GPIO.IN)
      threading.Thread.__init__(self)
      self.presenceValue = False
      self.lastTimeUp = 0
      self.lastTimeDown = 0
      self.done = False

    def run(self):
      while not self.done:
        self.update()
        time.sleep(.1)

    def update(self):
      pir_state = GPIO.input(GlobalConfig.pir_pin)
      if pir_state:
        self.lastTimeUp = time.time()
      else:
        self.lastTimeDown = time.time()
      self.presenceValue = pir_state

    def stop(self):
      self.done = True

    def value(self):
      return self.presenceValue

    def lastUp(self):
      return self.lastTimeUp
    
    def lastDown(self):
      return self.lastTimeDown

if __name__ == "__main__":
  presence = Presence()
  presence.start()
  sleep_state = False
  while True:
    #print("PRESENCE: ", presence.value())
    if sleep_state and presence.value():
      sleep_state = False
      print("WAKE UP!")
      continue

    if not sleep_state:
      now = time.time()
      if now - presence.lastUp() > 5:
        print("TURN OFF")
        sleep_state = True
      time.sleep(.1)

