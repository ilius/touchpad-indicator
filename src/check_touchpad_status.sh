#!/bin/sh
#copy to /etc/pm/sleep.d
LOGFILE="/var/log/sleep.log"

case "$1" in
        resume)
                echo "Resumed from suspend at `date`" >> "$LOGFILE"
                ;;
        thaw)
                echo "Resumed from hibernation at `date`" >> "$LOGFILE"
                ;;
        suspend)
                echo "Suspended to ram at `date`" >> "$LOGFILE"
                ;;
        hibernate)
                echo "Hibernated to disk at `date`" >> "$LOGFILE"
                ;;
esac
