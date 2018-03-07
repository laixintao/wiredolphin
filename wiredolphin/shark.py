# -*- coding: utf-8 -*-

"""
Load pcapng using pyshark
"""
import asyncio
from ipaddress import ip_address
import logging

from pyshark.capture.file_capture import FileCapture

from wiredolphin.packet_table import table

logger = logging.getLogger("shark")

def read_packet_lists():
    logger.info("capture run...")
    capture = FileCapture("test.pcapng", only_summaries=True, eventloop=asyncio.get_event_loop())
    # https://docs.python.org/3/library/ipaddress.html
    logger.info("capture created..")
    capture.packets_from_tshark(add_packet_to_table)


async def write_test_log():
    logger.info("test log...")


def add_packet_to_table(packet):
    #  logger.info(table)
    table.add_row({
        'Destination': ip_address(packet._fields['Destination']),
        'Source': ip_address(packet._fields['Source']),
        'Length': int(packet._fields['Length']),
        'No.': int(packet._fields['No.']),
        'Protocol': packet._fields['Protocol'],
        'Time': float(packet._fields['Time']),
        # to decode a literal escape in str
        # see https://stackoverflow.com/questions/26311277/evaluate-utf-8-literal-escape-sequences-in-a-string-in-python3
        'Info': packet._fields['Info'].encode().decode('unicode-escape').encode('latin1').decode('utf-8'),
    })
    table.last_rec += 1

def add_row():
    logger.info("add row run ...")
    logger.info("tshark table...{}".format(id(table)))

table.add_row(
        {
            'Destination': "2.1.1.1",
            'Source': "2.1.1.1",
            'Length': 200,
            'No.': 100,
            'Protocol': "TCP",
            'Time': 0.2020,
            # to decode a literal escape in str
            # see https://stackoverflow.com/questions/26311277/evaluate-utf-8-literal-escape-sequences-in-a-string-in-python3
            'Info': "test package",
        }
)
