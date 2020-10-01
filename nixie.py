#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#	Nixie management module
#

import RPi.GPIO as GPIO
from globalconfig import GlobalConfig
import time
import threading

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
    freq = 50
    self.r_led = GPIO.PWM(GlobalConfig.leds_r, freq)
    self.g_led = GPIO.PWM(GlobalConfig.leds_g, freq)
    self.b_led = GPIO.PWM(GlobalConfig.leds_b, freq)
    self.r = 0.
    self.g = 0.
    self.b = 0.
    self.r_led.start(self.r)
    self.g_led.start(self.g)
    self.b_led.start(self.b)
    self.LEDAnim = False
    self.colorAnimStepPause = .1	# Pause time

  def __del__(self):
    self.stopColorAnimation()
    self.r_led.stop()
    self.g_led.stop()
    self.b_led.stop()

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

  def push_number(self, number):
  #  print( "set_number", number)
    digit1 = number // 10
    digit2 = number % 10
  #  print("digit1", digit1)
  #  print("digit2", digit2)
    self.push_digit(digit2)
    self.push_digit(digit1)

  def set_number(self, number):
    self.push_number(number)
    self.pulse(GlobalConfig.nixie_rck)

  def set_numbers(self, n1, n2, n3):
    self.push_number(n1)
    self.push_number(n2)
    self.push_number(n3)
    self.pulse(GlobalConfig.nixie_rck)

  def turn_off(self):
    print( "turn_off" )
    self.push_digit(0xf)
    self.push_digit(0xf)
    self.pulse(GlobalConfig.nixie_rck)

  def setLEDColor(self, r, g, b):
    # TO-DO: Control PWM
#    GPIO.output(GlobalConfig.leds_r, r)
#    GPIO.output(GlobalConfig.leds_g, g)
#    GPIO.output(GlobalConfig.leds_b, b)
    self.stopColorAnimation()
#    print("Called setLEDColor with ", r, g, b)
    self.r = r*100.
    self.g = g*100.
    self.b = b*100.
#    print("Setting RGB to ", self.r, self.g, self.b)
    self.r_led.ChangeDutyCycle(self.r)
    self.g_led.ChangeDutyCycle(self.g)
    self.b_led.ChangeDutyCycle(self.b)

  def getLEDColor(self):
#    return GPIO.input(GlobalConfig.leds_r), GPIO.input(GlobalConfig.leds_g), GPIO.input(GlobalConfig.leds_b)
    return self.r/100., self.g/100., self.b/100.

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
      time.sleep(.01)
      number = ( number + 1 ) % 100

  def LEDColorAnimation(self):
    self.r_led.ChangeDutyCycle(0)
    self.g_led.ChangeDutyCycle(0)
    self.b_led.ChangeDutyCycle(0)
    for r in range(0, 101, 1):
      self.r = r
      self.r_led.ChangeDutyCycle(r)
      time.sleep(self.colorAnimStepPause)
      if not self.LEDAnim:
        return
    while True:
      for b in range(0, 101, 1):
        self.b = b
        self.b_led.ChangeDutyCycle(b)
        time.sleep(self.colorAnimStepPause)
        if not self.LEDAnim:
          return
      for r in range(100, -1, -1):
        self.r = r
        self.r_led.ChangeDutyCycle(r)
        time.sleep(self.colorAnimStepPause)
        if not self.LEDAnim:
          return
      for g in range(0, 101, 1):
        self.g = g
        self.g_led.ChangeDutyCycle(g)
        time.sleep(self.colorAnimStepPause)
        if not self.LEDAnim:
          return
      for b in range(100, -1, -1):
        self.b = b
        self.b_led.ChangeDutyCycle(b)
        time.sleep(self.colorAnimStepPause)
        if not self.LEDAnim:
          return
      for r in range(0, 101, 1):
        self.r = r
        self.r_led.ChangeDutyCycle(r)
        time.sleep(self.colorAnimStepPause)
        if not self.LEDAnim:
          return
      for g in range(100, -1, -1):
        self.g = g
        self.g_led.ChangeDutyCycle(g)
        time.sleep(self.colorAnimStepPause)
        if not self.LEDAnim:
          return

  def startColorAnimation(self):
    if self.LEDAnim:
      return
    self.LEDAnimThread = threading.Thread(target=self.LEDColorAnimation)
    self.LEDAnim = True
    self.LEDAnimThread.start()

  def stopColorAnimation(self):
    if not self.LEDAnim:
      return
    self.LEDAnim = False
    self.LEDAnimThread.join()

  def toggleColorAnimation(self):
    if self.LEDAnim:
      self.stopColorAnimation()
    else:
      self.startColorAnimation()

