#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#	Clock implementation over nixie
#

from globalconfig import GlobalConfig
import threading
import time
import nixie
import relay
import datetime


class Clock(threading.Thread):

    def __init__(self, nixies, relays):
      threading.Thread.__init__(self)
      self.done = False
      self.nixies = nixies
      self.relays = relays

    def run(self):
      while not self.done:
        self.setTime()
        if GlobalConfig.seconds_sound == 0:
          pass
        elif GlobalConfig.seconds_sound == 1:
          self.ticToc()
        elif GlobalConfig.seconds_sound == 2:
          self.ticTic()
        # Pause til next second
        now = time.time()
        time.sleep( 1 - ( now - int(now) ))

    def setTime(self):
      now = datetime.datetime.now()
      self.nixies.set_numbers(now.hour, now.minute, now.second)        

    def ticToc(self):
        self.relays.toggle(7)

    def ticTic(self):
        self.relays.on(7)
        time.sleep(.025)
        self.relays.off(7)

    def stop(self):
      self.done = True
      