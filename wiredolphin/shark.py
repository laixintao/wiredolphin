# -*- coding: utf-8 -*-

"""
Load pcapng using pyshark
"""
import asyncio
import logging

from pyshark.capture.inmem_capture import InMemCapture
from pyshark.capture.file_capture import FileCapture
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

    capture = FileCapture("test.pcapng", only_summaries=True)
    logger.info("Capture Feed packets")
    logger.debug("Start to feed_packets...")
    await capture.packets_from_tshark(table.add_packet)
    logger.debug("Start to add_table...")
    logger.info("table_id: {}".format(id(table)))


if __name__ == "__main__":
    load_packets("test.pcapng")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(capture_memeory_packets(only_summaries=True))
