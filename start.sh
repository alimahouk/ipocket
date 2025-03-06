# start.sh | v0.1 | 7/11/2020 | by alimahouk
# ---------------------------------------------
# ABOUT THIS FILE
# ---------------------------------------------
# This is a convenience script to start Internet
# Pockets.
#
# Redirect program output as required; default is no output.
# The PID of the process is written to /tmp.

FILE_IPOCK=ipocketd.py
if [ -f "$FILE_IPOCK" ]; then
        nohup python3 ipocketd.py </dev/null >/dev/null 2>&1 & echo $! > /tmp/ipock.pid
fi
