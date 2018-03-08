# -*- coding: utf-8 -*-

"""
Load pcapng using pyshark
"""
import asyncio
import logging

from pyshark.capture.inmem_capture import InMemCapture
from scapy.all import rdpcap, raw

from wiredolphin.packet_table import table

logger = logging.getLogger(__name__)
packets = []


def load_packets(filename):
    global packets
    logger.debug("scapy.rdpcap start to read file...")
    parsed_packets = rdpcap(filename)
    logger.debug("scapy.rdpcap read file done! len: {}".format(len(packets)))
    packets = [raw(packet) for packet in parsed_packets]


async def capture_memeory_packets(*args, **kwargs):
    """ coroutine to read packets to table """
    global packets

    capture = InMemCapture(*args, **kwargs)
    logger.info("Capture Feed packets")
    logger.debug("Start to feed_packets...")
    logger.info("Packets: {}".format(len(packets)))
    await capture.feed_packets(packets)
    logger.debug("Start to add_table...")

    for packet in capture:
        table.add_packet(packet)


if __name__ == "__main__":
    load_packets("test.pcapng")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(capture_memeory_packets(only_summaries=True))
