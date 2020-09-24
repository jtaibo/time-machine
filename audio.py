#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#	Audio management
#

import alsaaudio

#mixer = alsaaudio.Mixer('PCM', cardindex=1)
mixer = alsaaudio.Mixer('Speaker')


def getVolume():
  return mixer.getvolume()[0]

def setVolume(vol):
  mixer.setvolume(vol)


if __name__ == "__main__":

  scanCards = alsaaudio.cards()
  print("cards:", scanCards)
  for card in scanCards:
    scanMixers = alsaaudio.mixers(scanCards.index(card))
    print("mixers:", scanMixers)
