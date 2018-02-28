# -*- coding: utf-8 -*-

import urwid
from urwid_utils.palette import PaletteEntry, Palette
from panwid.datatable import DataTable

from packet_table import table

screen = urwid.raw_display.Screen()
screen.set_terminal_properties(256)
attr_entries = {}
for attr in ["dark red", "dark green", "dark blue"]:
    attr_entries[attr.split()[1]] = PaletteEntry(
        mono = "white",
        foreground = attr,
        background = "black"
    )
entries = DataTable.get_palette_entries(user_entries=attr_entries)
palette = Palette("default", **entries)

label = "Filter:"
help_text = "Use <Ctrl p> to focus on Filter."
pile = urwid.Pile([
    ("pack", urwid.Edit(label)),
    ("pack", urwid.Divider("\N{HORIZONTAL BAR}")),
    ("weight", 1, table),
    ("pack", urwid.Divider("\N{HORIZONTAL BAR}")),
    ("pack", urwid.Text(help_text))
])

def global_input(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    else:
        return False

main_loop = urwid.MainLoop(
    urwid.Frame(pile),
    palette=palette,
    screen=screen,
    unhandled_input=global_input
)

main_loop.run()
