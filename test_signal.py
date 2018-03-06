import urwid
debug = urwid.Text('')
def handler(widget, newtext):
   debug.set_text("Edit widget changed to %s" % newtext)
edit = urwid.Edit('')
key = urwid.connect_signal(edit, 'change', handler)
