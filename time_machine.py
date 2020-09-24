#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#	Relay management module
#

import time
import RPi.GPIO as GPIO

from globalconfig import GlobalConfig
import relay
import nixie
import clock

import webserver

print("Starting TimeMachine(TM)")

# Construction of global objects
relays = relay.RelayModule()
nixies = nixie.NixieDisplay()
the_clock = clock.Clock(nixies, relays)



def test_relays():
  # Test relays
  for ch in range(relays.size()):
    relays.on(ch)
    time.sleep(.5)
    relays.off(ch)

# Cleanup
def shutdown():
  print("TimeMachine(TM) shutdown!")
  the_clock.stop()
  the_clock.join()
  GPIO.cleanup()

try:
  #test_relays()
  relays.turnOnDevice("plasma_ball")
#  time.sleep(.5)
  relays.turnOnDevice("audio_amp")
#  time.sleep(.5)
  relays.turnOnDevice("nixie_control")
#  time.sleep(.5)
  relays.turnOnDevice("nixie_inverter")
#  time.sleep(.5)
  relays.turnOnDevice("vumeter_board")

#  nixies.testLEDs()
#  time.sleep(2)
#  nixies.testDisplay(100)

  nixies.setLEDColor(0, 1, 0)
  the_clock.start()

  # Start web service
  webserver.start(relays, nixies)

  while True:
    time.sleep(.2)
    pass
  shutdown()

except KeyboardInterrupt:
  pass

finally:
  shutdown()
  
