#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boofuzz import *

def main():
    # Target IP and port
    target_ip = '127.0.0.1'
    target_port = 21
    start_cmd = ["/home/kali/Documents/LightFTP/Source/Release/fftpd", "/home/kali/Documents/LightFTP/Source/Release/fftpd.conf"]
    procmon = ProcessMonitor(target_ip, 26002)
    procmon.set_options(start_commands=[start_cmd])

    # Initialize session
    session = Session(
        target=Target(
            connection=SocketConnection(target_ip, target_port, proto='tcp'),
            monitors=[procmon],
        )
    )
    define_proto(session=session)
    session.fuzz()

def define_proto(session):
    # disable Black formatting to keep custom indentation
    # fmt: off
    user = Request("user", children=(
        String(name="key", default_value="USER", fuzzable=False),
        Delim(name="space", default_value=" "),
        String(name="val", default_value="anonymous", fuzzable=False),
        Static(name="end", default_value="\r\n"),
    ))
    passw = Request("pass", children=(
        String(name="key", default_value="PASS", fuzzable=False),
        Delim(name="space", default_value=" "),
        String(name="val", default_value="anonymous", fuzzable=False),
        Static(name="end", default_value="\r\n"),
    ))
    stor = Request("stor", children=(
        String(name="key", default_value="STOR", fuzzable=False),
        Delim(name="space", default_value=" "),
        String(name="val", size=2500, padding="A", fuzzable=True),
        Static(name="end", default_value="\r\n"),
    ))
    # fmt: on

    session.connect(user)
    session.connect(user, passw)
    session.connect(passw, stor)

if __name__ == "__main__":
    main()

