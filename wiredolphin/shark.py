# -*- coding: utf-8 -*-

"""
Load pcapng using pyshark
"""
import asyncio
import logging

from pyshark.capture.file_capture import FileCapture

from wiredolphin.pantable import table

logger = logging.getLogger(__name__)


async def capture_memeory_packets(filename, *args, **kwargs):
    """ coroutine to read packets to table """
    capture = FileCapture(filename, *args, **kwargs)
    await capture.packets_from_tshark(table.add_packet, close_tshark=False)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(capture_memeory_packets(only_summaries=True))
