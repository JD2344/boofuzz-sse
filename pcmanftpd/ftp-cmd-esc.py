#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boofuzz import *

def main():
    # Target IP and port
    target_ip = '192.168.100.212'
    target_port = 21
    start_cmd = ["C:\\Users\\j\\Desktop\\pcman 2.0\\PCManFTPD2.exe"]
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
    cmds = Request("ftp-cmds", children=(
        Block("cmds", children=(
            Group("key", values= ["USER", "PASS", "STOR", "NLST", "MKD", "DEL", ""], fuzzable=True),
            Delim(name="space", default_value=" ", fuzzable=False),
            Group("val", values= ["\'", "\"", "\b", "\?", "\\", "\v", "\f"], fuzzable=True),
            Static(name="end", default_value="\r\n")
        ))
    ))
    # fmt: on

    session.connect(cmds)

if __name__ == "__main__":
    main()

