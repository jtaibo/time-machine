#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#	Global configuration (static)
#
#	This configuration reflects all hardware connections, so no GPIO conflicts occur
#	It is also the only point to update when these connections change
#

import RPi.GPIO as GPIO

class GlobalConfig:

  # Pin configuration (BCM)
  GPIO_mode = GPIO.BCM

  pir_pin = 18

  relay_pins = [27, 22, 23, 24, 25, 12, 5, 6]

  relay_devices = [
                    ("plasma_ball", 0),
                    ("audio_amp", 1),
                    ("nixie_control", 2),
                    ("nixie_inverter", 4),
                    ("vumeter_board", 5)
                  ]

  # Presence configuration
  timeout_to_sleep = 60

  # Nixie lamps LEDs
  leds_r = 13
  leds_g = 19
  leds_b = 26

  nixie_data = 16
  nixie_sck = 20
  nixie_rck = 21

  seconds_sound = 0

  # Known BT MACs
  bt_macs = [
              {"Javi", "A8:96:75:8B:A3:9A"}
            ]

