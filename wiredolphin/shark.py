# -*- coding: utf-8 -*-

"""
Load pcapng using pyshark
"""
from ipaddress import ip_address
import logging
from functools import partial

from pyshark.capture.inmem_capture import InMemCapture
from scapy.all import rdpcap, raw

logger = logging.getLogger("shark")


def add_packet_to_table(table, packet):
    """
    Actually callback, use global ``table`` will cause a problem.
    Don't know why...
    """
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

async def read_file(filename):
    logger.debug("scapy.rdpcap start to read file...")
    packets = rdpcap(filename)
    logger.debug("scapy.rdpcap read file done! len: {}".format(len(packets))) 
    return [raw(packet) for packet in packets]


async def read_packet_lists(callback):
    """ coroutine to read packets to table """
    logger.info("capture run...")
    capture = InMemCapture(only_summaries=True)
    # https://docs.python.org/3/library/ipaddress.html
    logger.info("capture created..")
    raw_packets = await read_file("test.pcapng")
    logger.info("Capture Feed packets")
    capture.feed_packets(raw_packets)
    await capture.packets_from_tshark(callback)


if __name__ == '__main__':
    def print_callback(packet):
        print(packet)
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_packet_lists(print_callback))
