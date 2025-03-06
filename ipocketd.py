#!/usr/bin/env python3

# ipocketd.py | v0.1 | 5/11/2020 | by alimahouk
# ---------------------------------------------
# ABOUT THIS FILE
# ---------------------------------------------
# Internet Pockets are protocol-less, ephemeral,
# microdata stores. A pocket is represented by
# an IP port. The port is open over both TCP and
# UDP.
#
# Any data written to a pocket over UDP is
# considered as 'storing' the data there (and
# will overwrite any existing data). Any client
# connecting to the pocket over TCP is
# considered as 'fetching' the data there.
#
# Restarting the daemon wipes out the contents
# of all pockets.

import argparse
import socket
import threading


class IPockets:
        DEFAULT_PORT_COUNT = 20  # Open this many ports by default.
        DEFAULT_PORT_START = 1024
        POCK_HEAD = "#!ipock"

        def __init__(self, ports=DEFAULT_PORT_COUNT, start=DEFAULT_PORT_START):
                # For handling argparse.
                if ports is None:
                        ports = self.DEFAULT_PORT_COUNT
                if start is None:
                        start = self.DEFAULT_PORT_START
                self.pockets = dict()
                self.portCount = ports
                self.portStart = start
                self.readSockets = set()
                self.writeSockets = set()

                i = self.portStart
                portsOpened = 0
                while portsOpened < self.portCount:
                        pocketAddress = ("0.0.0.0", i)
                        sockRead = None
                        sockWrite = None
                        try:
                                # For "reading from" the client.
                                sockRead = socket.socket(
                                        socket.AF_INET,
                                        socket.SOCK_DGRAM)
                                sockRead.setsockopt(
                                        socket.SOL_SOCKET, 
                                        socket.SO_REUSEADDR, 
                                        1
                                        )
                                sockRead.bind(pocketAddress)
                                self.readSockets.add(sockRead)
                                # For "writing to" the client.
                                sockWrite = socket.socket(
                                        socket.AF_INET,
                                        socket.SOCK_STREAM)
                                sockWrite.setsockopt(
                                        socket.SOL_SOCKET, 
                                        socket.SO_REUSEADDR, 
                                        1
                                        )
                                sockWrite.setsockopt(
                                        socket.IPPROTO_TCP, 
                                        socket.TCP_NODELAY, 
                                        1
                                        )
                                sockWrite.bind(pocketAddress)
                                self.writeSockets.add(sockWrite)

                                portsOpened += 1
                                print(f"OPENED PORT {i}")
                        except:
                                if sockRead is not None:
                                        sockRead.close()
                                        self.readSockets.remove(sockRead)
                                elif sockWrite is not None:
                                        sockWrite.close()
                                        self.writeSockets.remove(sockWrite)
                        finally:
                                i += 1
        
        def listenForWrite(self):
                for sock in self.writeSockets:
                        # Spawn a different thread and do writing there.
                        sockThread = threading.Thread(
                                target=self.write,
                                args=(sock,))
                        sockThread.daemon = True
                        sockThread.start()
        
        def listenForRead(self):
                for sock in self.readSockets:
                        # Spawn a different thread and do reading there.
                        sockThread = threading.Thread(
                                target=self.read,
                                args=(sock,))
                        sockThread.daemon = True
                        sockThread.start()
        
        def read(self, sock):
                while 1:
                        # NOTE:
                        # -----
                        # This probably needs to be modified to recv messages of arbitrary sizes.
                        message, _ = sock.recvfrom(1024)
                        port = sock.getsockname()[1]
                        try:
                                self.pockets[port] = message.decode()
                        except:
                                pass
        
        def start(self):
                self.listenForRead()
                self.listenForWrite()
                print(f"--[OPENED {self.portCount} POCKET(S) STARTING FROM PORT {self.portStart}]--")
                forever = threading.Event()
                forever.wait()
        
        def write(self, sock):
                sock.listen(1)
                while 1:
                        connection, _ = sock.accept()
                        port = sock.getsockname()[1]
                        if port in self.pockets:
                                existingContents = self.pockets[port]
                        else:
                                existingContents = ""
                        try:
                                connection.sendall(f"{self.POCK_HEAD} {port}\r\n{existingContents}\r\n\r\n".encode())
                        except Exception as e:
                                print(e)
                        finally:
                                connection.close()

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Internet Pockets are protocol-less, ephemeral, microdata stores. A pocket is represented by an IP port. The port is open over both TCP and UDP.\n\nAny data written to a pocket over UDP is considered as 'storing' the data there (and will overwrite any existing data). Any client connecting to the pocket over TCP is considered as 'fetching' the data there.\n\nRestarting the daemon wipes out the contents of all pockets.")
        parser.add_argument("-s", "--start", type=int, help="The first port to open.", required=False)
        parser.add_argument("-p", "--ports", type=int, help="How many pockets to open beginning at the start port.", required=False)
        args = parser.parse_args()

        pocketDaemon = IPockets(
                ports=args.ports,
                start=args.start)
        pocketDaemon.start()
