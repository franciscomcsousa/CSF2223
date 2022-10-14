#!/bin/bash

timestamp() {
    date +%s
}


TS=$(timestamp)
USER=carlseagal
HOST=backup
DIR=~
ZIPFILE=backup_$TS.zip
BACKUP_PASS=$(~/backups/pass_gen.sh $TS)

zip -r --password $BACKUP_PASS $ZIPFILE ~/Desktop/moon
rsync -a ./$ZIPFILE $USER@$HOST:$DIR
rm $ZIPFILE

