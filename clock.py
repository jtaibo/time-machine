#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#	Clock implementation over nixie
#

import threading
import time
import nixie
import datetime


class Clock(threading.Thread):

    def __init__(self, nixies):
      threading.Thread.__init__(self)
      self.done = False
      self.nixies = nixies

    def run(self):
      while not self.done:
        self.setTime()
        time.sleep(1)

    def setTime(self):
      now = datetime.datetime.now()
      self.nixies.set_numbers(now.hour, now.minute, now.second)        

    def stop(self):
      self.done = True
      