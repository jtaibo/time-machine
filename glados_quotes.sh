#!/bin/bash
#

#THE_PLAYER=mplayer
#THE_PLAYER=omxplayer
#THE_PLAYER=cvlc
THE_PLAYER="omxplayer -o alsa"

GLADOS_DIR=~/.GLaDOS_quotes

if [ ! -d $GLADOS_DIR ]; then
  mkdir $GLADOS_DIR
fi
pushd $GLADOS_DIR

GLADOS_QUOTES_PAGE_URL=http://theportalwiki.com/wiki/GLaDOS_voice_lines
GLADOS_FILE=`basename $GLADOS_QUOTES_PAGE_URL`
AUDIO_LIST_FILE=audio_list_file
CACHE_DIR=cache

if [ ! -r $AUDIO_LIST_FILE ]; then

  if [ ! -r $GLADOS_FILE ]; then
    wget $GLADOS_QUOTES_PAGE_URL
  fi

  cat $GLADOS_FILE | tr '<' '\n' | grep "^a href" | cut -f2 -d\" | grep \.wav$ > $AUDIO_LIST_FILE  
fi

LIST_SIZE=`wc -l < $AUDIO_LIST_FILE`
AUDIO_FILE=`head -$((${RANDOM} % $LIST_SIZE + 1)) $AUDIO_LIST_FILE | tail -1`

if [ ! -d $CACHE_DIR ]; then
  mkdir $CACHE_DIR
fi
cd $CACHE_DIR

LOCAL_FILE=`basename $AUDIO_FILE`
if [ ! -r $LOCAL_FILE ]; then
  echo "Calling \"wget $AUDIO_FILE\" in directory `pwd`"
  wget $AUDIO_FILE
fi

$THE_PLAYER $LOCAL_FILE

popd
