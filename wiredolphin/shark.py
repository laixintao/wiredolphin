# -*- coding: utf-8 -*-

"""
Load pcapng using pyshark
"""

from pyshark.capture.file_capture import FileCapture


from ipaddress import ip_address
import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="datatable.log"
)
logger = logging.getLogger("shark")


def packet_lists():
    packets = FileCapture("test.pcapng", only_summaries=True)
    # https://docs.python.org/3/library/ipaddress.html
    for packet in packets:
        yield {
            'Destination': ip_address(packet._fields['Destination']),
            'Source': ip_address(packet._fields['Source']),
            'Length': int(packet._fields['Length']),
            'No.': int(packet._fields['No.']),
            'Protocol': packet._fields['Protocol'],
            'Time': float(packet._fields['Time']),
            'Info': packet._fields['Info'],
        }
