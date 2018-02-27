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
    time_start = None

    @classmethod
    def get_time_delta(cls, sniff_timestamp):
        # TODO possiable to use tshark's time_relative?
        # https://www.wireshark.org/lists/wireshark-users/201110/msg00143.html
        sniff_timestamp = float(sniff_timestamp)
        if cls.time_start is None:
            cls.time_start = sniff_timestamp
            return 0
        else:
            return sniff_timestamp - cls.time_start

    def __init__(self, packet):
        self._packet = packet
        super().__init__()

        self.update({
            "highest_layer": packet.highest_layer,
            'number': packet.number,
            'length': packet.length,
            'time_delta': "%.6f" % self.get_time_delta(packet.sniff_timestamp),
            'src': packet.ip.src,
            'dst': packet.ip.dst,
        })

        if 'tcp' in packet:
            self.update(tcp_port=packet['tcp'].port)

    @property
    def transport_layer_and_heighest_layer(self):
        return '%s/%s' % (self._packe.transport_protocol, self._packet.highest_layer)


def packet_lists():
    packets = FileCapture("test.pcapng")
    return [DolphinPacket(packet) for packet in packets]
