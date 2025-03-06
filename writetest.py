#!/usr/bin/env python3

# WriteTest.py | v0.1 | 6/11/2020 | by alimahouk
# ---------------------------------------------
# ABOUT THIS FILE
# ---------------------------------------------
# A test script that writes to an Internet
# pocket. To check that it works, Telnet to the
# address and port. The output should be what this
# script wrote out to the pocket.

import socket

MESSAGE = "Hello World!"
POCK_ADDR = ("127.0.0.1", 1024)

sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM)
sock.sendto(
        MESSAGE.encode(),
        POCK_ADDR)