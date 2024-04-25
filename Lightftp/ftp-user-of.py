#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boofuzz import *

def main():
    target_ip = '127.0.0.1'
    target_port = 21
    session = Session(
        target=Target(
            connection=SocketConnection(target_ip, target_port, proto='tcp')
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
        String(name="val", size=3000, padding="A", fuzzable=True),
        Static(name="end", default_value="\r\n"),
    ))
    # fmt: on

    session.connect(user)

if __name__ == "__main__":
    main()

