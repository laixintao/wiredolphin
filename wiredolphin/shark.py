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
    summary_capture = FileCapture(filename, only_summaries=True, *args, **kwargs)
    detail_capture = FileCapture(filename, only_summaries=False, *args, **kwargs)
    await summary_capture.packets_from_tshark(table.add_packet)

    table.packets_loaded = True
    table.summary_capture = summary_capture
    table.detail_capture = detail_capture
    table.detail_capture.load_packets()

    logger.info("packets loaded!")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(capture_memeory_packets(only_summaries=True))
