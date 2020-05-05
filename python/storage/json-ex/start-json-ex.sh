#!/bin/sh

CLASSES_EX=`realpath ../../basic/classes-ex/classes-ex.py`
CAPTAIN_EX=`realpath ../../basic/classes-ex/captain.py`

ln -s "$CLASSES_EX" `pwd`/starships.py
ln -s "$CAPTAIN_EX" `pwd`/captain.py

python3 json-ex.py

unlink starships.py
unlink captain.py

exit 0
