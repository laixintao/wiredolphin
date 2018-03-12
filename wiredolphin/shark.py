# -*- coding: utf-8 -*-

"""
Load pcapng using pyshark
"""
import asyncio
import logging

from pyshark.capture.inmem_capture import InMemCapture
from scapy.all import rdpcap, raw


logger = logging.getLogger(__name__)
packets = []


def load_packets(filename):
    global packets
    logger.debug("scapy.rdpcap start to read file...")
    parsed_packets = rdpcap(filename)
    logger.debug("scapy.rdpcap read file done! len: {}".format(len(packets)))
    packets = [raw(packet) for packet in parsed_packets]


async def capture_memeory_packets(table, *args, **kwargs):
    """ coroutine to read packets to table """
    global packets
    logger.info("packets: {}".format(len(packets)))
    capture = InMemCapture(*args, **kwargs)
    packets = await capture.feed_packets(packets)
    for packet in packets:
        table.add_packet(packet)


if __name__ == "__main__":
    load_packets("test.pcapng")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(capture_memeory_packets(only_summaries=True))
