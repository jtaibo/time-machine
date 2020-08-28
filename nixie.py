#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#	Relay management module
#

import RPi.GPIO as GPIO
from globalconfig import GlobalConfig
import time

PULSE_DURATION = 0.01

class NixieDisplay:

  def __init__(self):
    GPIO.setmode(GlobalConfig.GPIO_mode)
    # Serial registers for nixie digits ()
    GPIO.setup(GlobalConfig.nixie_data, GPIO.OUT)
    GPIO.setup(GlobalConfig.nixie_sck, GPIO.OUT)
    GPIO.setup(GlobalConfig.nixie_rck, GPIO.OUT)
    GPIO.output(GlobalConfig.nixie_data, 0)
    GPIO.output(GlobalConfig.nixie_sck, 0)
    GPIO.output(GlobalConfig.nixie_rck, 0)
    # RGB LEDs
    GPIO.setup(GlobalConfig.leds_r, GPIO.OUT)
    GPIO.setup(GlobalConfig.leds_g, GPIO.OUT)
    GPIO.setup(GlobalConfig.leds_b, GPIO.OUT)
    GPIO.output(GlobalConfig.leds_r, 0)
    GPIO.output(GlobalConfig.leds_g, 0)
    GPIO.output(GlobalConfig.leds_b, 0)

  def pulse(self, pin):
  #  GPIO.output(pin, 0)
  #  time.sleep(PULSE_DURATION)
    GPIO.output(pin, 1)
    time.sleep(PULSE_DURATION)
    GPIO.output(pin, 0)

  def push_bit(self, bit):
  #  print("push_bit", bit)
    GPIO.output(GlobalConfig.nixie_data, bit)
    self.pulse(GlobalConfig.nixie_sck)

  def push_digit(self, digit):
  #  print("push_digit", digit)
    for x in range(3, -1, -1):
      bit = ( digit >> x ) & 0x1
      self.push_bit(bit)

  def set_number(self, number):
  #  print( "set_number", number)
    digit1 = number // 10
    digit2 = number % 10
  #  print("digit1", digit1)
  #  print("digit2", digit2)
    self.push_digit(digit2)
    self.push_digit(digit1)
    self.pulse(GlobalConfig.nixie_rck)

  def turn_off(self):
    print( "turn_off" )
    self.push_digit(0xf)
    self.push_digit(0xf)
    self.pulse(GlobalConfig.nixie_rck)


  def testLEDs(self):
    # Test LEDs
    GPIO.output(GlobalConfig.leds_r, 1)
    time.sleep(.2)
    GPIO.output(GlobalConfig.leds_r, 0)
    GPIO.output(GlobalConfig.leds_g, 1)
    time.sleep(.2)
    GPIO.output(GlobalConfig.leds_g, 0)
    GPIO.output(GlobalConfig.leds_b, 1)
    time.sleep(.2)
    GPIO.output(GlobalConfig.leds_b, 0)
    
  def testDisplay(self, num_iters=100):
    number = 0
    for i in range(num_iters):
      # LEDs
      GPIO.output(GlobalConfig.leds_r, number & 0x1)
      GPIO.output(GlobalConfig.leds_g, number & 0x2)
      GPIO.output(GlobalConfig.leds_b, number & 0x4)
      # Nixie lamps
      self.set_number(number)
      time.sleep(.1)
      number = ( number + 1 ) % 100
