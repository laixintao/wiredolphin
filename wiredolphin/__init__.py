# -*- coding: utf-8 -*-

import urwid
from pyshark.capture.file_capture import FileCapture


def packet_lists():
    packets = FileCapture("test.pcapng")
    body = []
    for packet in packets:
        body.append(urwid.Text(packet.number))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))
