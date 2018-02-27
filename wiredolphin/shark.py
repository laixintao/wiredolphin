# -*- coding: utf-8 -*-

"""
Load pcapng using pyshark
"""

from pyshark.capture.file_capture import FileCapture


import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="datatable.log"
)
logger = logging.getLogger("shark")


class DolphinPacket(dict):
    """Wrap pyshark's packet, to display in datatable"""

    def __init__(self, packet):
        self._packet = packet
        super().__init__()
        self.update({
            "highest_layer": packet.highest_layer,
            'number': packet.number,
            'length': packet.length,
        })

        if 'tcp' in packet:
            self.update(tcp_port=packet['tcp'].port)

    @property
    def transport_layer_and_heighest_layer(self):
        return '%s/%s' % (self._packe.transport_protocol, self._packet.highest_layer)


def packet_lists():
    packets = FileCapture("test.pcapng")
    return [DolphinPacket(packet) for packet in packets]
