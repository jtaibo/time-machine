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

print("Starting TimeMachine(TM)")

relays = relay.RelayModule()
nixies = nixie.NixieDisplay()

def test_relays():
  # Test relays
  for ch in range(relays.size()):
    relays.on(ch)
    time.sleep(.5)
    relays.off(ch)

# Cleanup
def shutdown():
  print("TimeMachine(TM) shutdown!")
  GPIO.cleanup()

try:
  #test_relays()
  relays.turnOnDevice("plasma_ball")
  time.sleep(.5)
  relays.turnOnDevice("audio_amp")
  time.sleep(.5)
  relays.turnOnDevice("nixie_control")
  time.sleep(.5)
  relays.turnOnDevice("nixie_inverter")

  nixies.testLEDs()
  time.sleep(2)
  nixies.testDisplay(100)

  while True:
    time.sleep(.2)
    pass
  shutdown()

except KeyboardInterrupt:
  pass

finally:
  shutdown()
  
