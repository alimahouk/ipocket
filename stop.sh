# stop.sh | v0.1 | 7/11/2020 | by alimahouk
# ---------------------------------------------
# ABOUT THIS FILE
# ---------------------------------------------
# This is a convenience script to kill Internet
# Pockets.

PIDFILE_IPOCK=/tmp/ipock.pid
if [ -f "$PIDFILE_IPOCK" ]; then
        kill -15 $(cat $PIDFILE_IPOCK)
        rm $PIDFILE_IPOCK
fi
