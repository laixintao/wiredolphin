#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import logging
from ipaddress import ip_address

import urwid
import string

from panwid.datatable import DataTableColumn, DataTable

logger = logging.getLogger(__name__)

NORMAL_FG_MONO = "white"
NORMAL_FG_16 = "light gray"
NORMAL_BG_16 = "black"
NORMAL_FG_256 = "light gray"
NORMAL_BG_256 = "g0"


COLUMNS = [
    DataTableColumn("No.", label="No.", width=5, align="right",
                    attr="color", padding=0,
                    footer_fn=lambda column, values: sum(v for v in values if v is not None)),
    DataTableColumn("Time", label="Time", width=10, align="left",
                    sort_key=lambda v: (v is None, v),
                    attr="color", padding=0,
                    footer_fn=lambda column, values: sum(v for v in values if v is not None)),
    DataTableColumn("Source", label="Srouce", width=15, align="left",
                    attr="color", padding=0,
                    footer_fn=lambda column, values: sum(v for v in values if v is not None)),
    DataTableColumn("Destination", label="Destination", width=15, align="left",
                    attr="color", padding=0,
                    footer_fn=lambda column, values: sum(v for v in values if v is not None)),
    DataTableColumn("Protocol", label="Protocol", width=9, align="left",
                    attr="color", padding=0,
                    footer_fn=lambda column, values: sum(v for v in values if v is not None)),
    DataTableColumn("Length", label="Length", width=7, align="right",
                    attr="color", padding=0,
                    footer_fn=lambda column, values: sum(v for v in values if v is not None)),
    DataTableColumn("Info", label="Info", align="left",
                    attr="color", padding=0,
                    wrap='clip',
                    footer_fn=lambda column, values: sum(v for v in values if v is not None)),
]

class PacketTable(DataTable):

    columns = COLUMNS[:]

    index = "No."

    def __init__(self, packets, *args, **kwargs):
        self.packets = packets
        self.last_rec = len(self.packets)
        self.packets_loaded = False  # flag capture status
        super(PacketTable, self).__init__(*args, **kwargs)

    def query(self, sort=(None, None), offset=None, limit=None, load_all=False):
        return self.packets

    def query_result_count(self):
        return len(self.packets)

    def add_packet(self, packet):
        """
        Actually callback, use global ``table`` will cause a problem.
        Don't know why...
        """
        logger.info("{}.add_packet {}".format(self, packet))
        data = {
            'Destination': ip_address(packet._fields['Destination']),
            'Source': ip_address(packet._fields['Source']),
            'Length': int(packet._fields['Length']),
            'No.': int(packet._fields['No.']),
            'Protocol': packet._fields['Protocol'],
            'Time': float(packet._fields['Time']),
            # to decode a literal escape in str
            # see https://stackoverflow.com/questions/26311277/evaluate-utf-8-literal-escape-sequences-in-a-string-in-python3
            'Info': packet._fields['Info'].encode().decode('unicode-escape').encode('latin1').decode('utf-8'),
        }
        self.add_row(data)

    def toggle_details(self):
        logger.info("Toggle details: {}".format(self.selection))
        logger.info("TableRow values: {}".format(self.selection.values))
        packet_no = self.selection.values['No.']
        logger.info("--------------------Packet detail--------------")
        logger.info(self.detail_capture[packet_no])

    def keypress(self, size, key):
        if key == "meta r":
            self.randomize_query_data()
            self.reset(reset_sort=True)
        if key == "ctrl r":
            self.reset(reset_sort=True)
        if key == "ctrl d":
            self.log_dump(20)
        if key == "meta d":
            self.log_dump(20, columns=["foo", "baz"])
        if key == "ctrl f":
            self.focus_position = 0
        elif key == "ctrl t":
            # logger.info(self.get_row(0)[0])
            logger.info(self.selection.data["bar"])
        elif key == "meta i":
            logger.info("foo %s, baz: %s" %(self.selection.get("foo"),
                                                self.selection.get("baz")))
        elif self.ui_sort and key.isdigit() and int(key)-1 in range(len(self.columns)):
            col = int(key)-1
            self.sort_by_column(col, toggle=True)
        elif key == "ctrl l":
            self.load("test.json")
        elif key == "ctrl s":
            self.save("test.json")
        elif key == "0":
            # self.sort_by_column(self.index, toggle=True)
            self.sort_index()
        elif key == "a":
            self.add_row(self.random_row(self.last_rec))
            self.last_rec += 1
        elif key == "A":
            self.add_row(self.random_row(self.last_rec), sort=False)
            self.last_rec += 1
        elif key == "d":
            if len(self):
                self.delete_rows(self.df.index[self.focus_position])
        elif key == "meta a":
            name = "".join( random.choice(
                        string.ascii_uppercase
                        + string.lowercase
                        + string.digits
                    ) for _ in range(5) )
            data = [ "".join( random.choice(
                        string.ascii_uppercase
                        + string.lowercase
                        + string.digits
                    ) for _ in range(5)) for _ in range(len(self)) ]
            col = DataTableColumn(name, label=name, width=6, padding=0)
            self.add_columns(col, data=data)
        elif key == "r":
            self.set_columns(COLUMNS)
        elif key == "t":
            self.toggle_columns("qux")
        elif key == "T":
            self.toggle_columns(["foo", "baz"])
        elif key == "D":
            self.remove_columns(len(self.columns)-1)
        elif key == "f":
            self.apply_filters([lambda x: x["foo"] > 20, lambda x: x["bar"] < 800])
        elif key == "F":
            self.clear_filters()
        elif key == ".":
            self.toggle_details()
        elif key == "s":
            self.selection.set_attr("red")
        elif key == "S":
            self.selection.clear_attr("red")
        elif key == "k":
            self.selection[2].set_attr("red")
        elif key == "K":
            self.selection[2].clear_attr("red")
        elif key == "u":
            logger.info(self.footer.values)
        elif key == "shift left":
            self.cycle_sort_column(-1)
        elif key == "shift right":
            self.cycle_sort_column(1)
        elif self.ui_sort and key == "shift up":
            self.sort_by_column(reverse=True)
        elif self.ui_sort and key == "shift down":
            self.sort_by_column(reverse=False)
        elif key == "shift end":
            self.load_all()
            # self.listbox.focus_position = len(self) -1
        elif key == "ctrl up":
            if self.focus_position > 0:
                self.swap_rows(self.focus_position, self.focus_position-1, "foo")
                self.focus_position -= 1
        elif key == "ctrl down":
            if self.focus_position < len(self)-1:
                self.swap_rows(self.focus_position, self.focus_position+1, "foo")
                self.focus_position += 1
        else:
            return super(PacketTable, self).keypress(size, key)


def detail_fn(data):
    logger.info("detail_fn run...")
    return urwid.Padding(urwid.Columns([
        ("weight", 1, data.get("qux")),
        ("weight", 1, urwid.Text(str(data.get("baz_len")))),
        ("weight", 2, urwid.Text(str(data.get("xyzzy")))),
    ]))


table = PacketTable(
    [], # init as empty, `add_row` dynamic
    index="No.",
    detail_fn=detail_fn,
    detail_column="bar",
    with_scrollbar=True,
    sort_refocus = True
)
urwid.connect_signal(
    table, "select",
    lambda source, selection: logger.info("selection: %s" %(selection))
)
