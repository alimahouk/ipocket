# XP001: Internet Pockets

What new possibilities would exist if we were to open unused ports on computers around the world and turn them into transient data repositories?

Internet Pockets are protocol-less, ephemeral, microdata stores. A pocket is represented by an IP port. The port is open over both TCP and UDP.

Any data written to a pocket over UDP is considered as 'storing' the data there (and will overwrite any existing data). Any client connecting to the pocket over TCP is considered as 'fetching' the data there.

Restarting the daemon wipes out the contents of all pockets.
