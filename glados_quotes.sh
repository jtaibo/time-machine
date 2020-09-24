#!/bin/bash
#

#THE_PLAYER=mplayer
#THE_PLAYER=omxplayer
#THE_PLAYER=cvlc
THE_PLAYER="omxplayer -o alsa"

#GLADOS_DIR=/tmp/GlaDOS_quotes
GLADOS_DIR=~/.GlaDOS_quotes

if [ ! -d $GLADOS_DIR ]; then
  mkdir $GLADOS_DIR
fi
cd $GLADOS_DIR

GLADOS_QUOTES_PAGE_URL=http://theportalwiki.com/wiki/GLaDOS_voice_lines
GLADOS_FILE=`basename $GLADOS_QUOTES_PAGE_URL`
AUDIO_LIST_FILE=audio_list_file

if [ ! -r $AUDIO_LIST_FILE ]; then

  if [ ! -r $GLADOS_FILE ]; then
    wget $GLADOS_QUOTES_PAGE_URL
  fi

  cat $GLADOS_FILE | tr '<' '\n' | grep "^a href" | cut -f2 -d\" | grep \.wav$ > $AUDIO_LIST_FILE  
fi

LIST_SIZE=`wc -l < $AUDIO_LIST_FILE`
AUDIO_FILE=`head -$((${RANDOM} % $LIST_SIZE + 1)) $AUDIO_LIST_FILE | tail -1`

$THE_PLAYER $AUDIO_FILE

