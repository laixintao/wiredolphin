# -*- coding: utf-8 -*-

import urwid
from pyshark.capture.file_capture import FileCapture


display_filter = urwid.Edit("Filter:")

def packet_lists():
    packets = FileCapture("test.pcapng")
    body = []
    for packet in packets:
        body.append(urwid.Text(packet.number))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


main_list = packet_lists()
main = urwid.Frame(main_list, header=display_filter, focus_part='header')


urwid.MainLoop(main, palette=[('reversed', 'standout', '')]).run()
