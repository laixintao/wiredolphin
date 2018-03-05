# -*- coding: utf-8 -*-

import pyshark


cap = pyshark.FileCapture('test.pcapng', only_summaries=True)

for packet in cap:
    print(packet.no)
