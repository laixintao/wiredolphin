# -*- coding: utf-8 -*-

"""
Load pcapng using pyshark
"""
import asyncio
from ipaddress import ip_address
import logging
from functools import partial

from pyshark.capture.file_capture import FileCapture

logger = logging.getLogger("shark")


async def write_test_log():
    logger.info("test log...")


def add_packet_to_table(table, packet):
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


def make_packet_callback(table):
    add_packet_to_table_partial = partial(add_packet_to_table, table)
    return add_packet_to_table_partial

async def read_packet_lists(callback):
    logger.info("capture run...")
    capture = FileCapture("test.pcapng", only_summaries=True, eventloop=asyncio.get_event_loop())
    # https://docs.python.org/3/library/ipaddress.html
    logger.info("capture created..")
    await capture.packets_from_tshark(callback)
