#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boofuzz import *

def main():    
    target_ip = '127.0.0.1'
    target_port = 21
    session = Session(
        target=Target(
            connection=SocketConnection(target_ip, target_port, proto='tcp'),
        )
    )
    define_proto(session=session)
    session.fuzz()

def define_proto(session):
    user = Request("user", children=(
        String(name="key", default_value="USER", fuzzable=False),
        Delim(name="space", default_value=" ", fuzzable=False),
        String(name="val", default_value="anonymous", fuzzable=False),
        Static(name="end", default_value="\r\n"),
    ))
    cmd_2 = Request("ftp-cmds", children=(
        Block("cmds", children=(
            Group("key", values= ["PASS", "STOR", "NLST", "MKD", "DEL", ""], fuzzable=True),
            Delim(name="space", default_value=" ", fuzzable=False),
            String(name="val", fuzzable=True),
            Static(name="end", default_value="\r\n")
        ))
    ))

    session.connect(user)
    session.connect(user, cmd_2)

if __name__ == "__main__":
    main()

