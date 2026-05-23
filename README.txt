Assignment 3 - DSU Journal with Online Publishing
ICS 32 - Programming with Software Libraries in Python

This program extends the Assignment 2 journal application to support
publishing journal entries to a remote DSP server over network sockets.
The program stores journal data locally in .dsu files using the Profile
module, and optionally sends posts and bio updates to a DSP server using
the ds_client and ds_protocol modules. It supports both a friendly
numbered menu interface for regular users and an admin mode for direct
command input.

The ds_protocol module handles JSON encoding and decoding of all DSP
protocol messages including join, post, and bio commands. The ds_client
module manages the socket connection to the DSP server and implements
the send() function which joins the server, sends a post and/or bio,
and returns True on success or False on any failure. The ui module
handles all command parsing and dispatching for C, O, E, P, D, R, and T
commands. The a3.py module is the entry point and provides both a
friendly UI mode with guided menus and an admin mode that accepts raw
commands without interactive prompts.
