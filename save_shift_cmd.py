#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
import os
import sys
import re
import json

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SaveShiftCmd(Gtk.Window):
  def __init__(self):
    Gtk.Window.__init__(self, title="save Shift cmd", default_width=500, default_height=350)
    self.border_width = 10

    self.connect("key-press-event", self.on_window_key_press)

    hb = Gtk.HeaderBar()
    hb.set_show_close_button(True)
    hb.props.title = "Save Shift cmd"
    self.set_titlebar(hb)

    self.grid = Gtk.Grid()
    self.add(self.grid)

    # params:
    #   1 => obj
    #   2 => left
    #   3 => top
    #   4 => width

    self.label = Gtk.Label(label="Atalho")
    self.combo = Gtk.ComboBoxText()
    self.combo.insert(0,  "0",  "s1")
    self.combo.insert(1,  "1",  "s2")
    self.combo.insert(2,  "2",  "s3")
    # self.combo.insert(3,  "3",  "s4")
    # self.combo.insert(4,  "4",  "s5")
    # self.combo.insert(5,  "5",  "s6")
    self.combo.insert(6,  "6",  "s7")
    self.combo.insert(7,  "7",  "s8")
    self.combo.insert(8,  "8",  "s9")

    self.combo.connect("changed", self.on_combo_changed)

    self.grid.add(self.label)
    self.grid.insert_column(1)
    self.grid.set_row_spacing(10)
    self.grid.set_column_spacing(10)
    self.grid.attach(self.combo, 1, 0, 100, 1)
    # self.grid.attach_next_to(self.combo, self.label, Gtk.PositionType.RIGHT, 1, 10)

    # a scrollbar for the child widget (that is going to be the textview)
    self.scrolled_window = Gtk.ScrolledWindow()
    self.scrolled_window.set_border_width(5)
    # we scroll only if needed
    self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

    # a text buffer (stores text)
    self.buffer1 = Gtk.TextBuffer()

    # a textview (displays the buffer)
    self.textview = Gtk.TextView(buffer=self.buffer1)
    # wrap the text, if needed, breaking lines in between words
    self.textview.set_wrap_mode(Gtk.WrapMode.WORD)

    # textview is scrolled
    self.scrolled_window.add(self.textview)
    self.grid.attach_next_to(self.scrolled_window, self.label, Gtk.PositionType.BOTTOM, 100, 20)

    self.label2 = Gtk.Label(label="Time")
    self.entry = Gtk.Entry()
    self.grid.attach_next_to(self.label2, self.scrolled_window, Gtk.PositionType.BOTTOM, 1, 1)
    self.grid.attach_next_to(self.entry, self.label2, Gtk.PositionType.RIGHT, 3, 1)

    self.button = Gtk.Button(label="Save")
    self.grid.attach(self.button, 30, 30, 15, 1)

    self.button.connect("clicked", self.on_button_clicked)


  def on_window_key_press(self, widget, event):
    keycode = event.get_keycode()[1]

    if(keycode == 9):
      sys.exit()

  def on_combo_changed(self, combo):
    if self.combo.get_active_text() == None:
      return

    str_json = open("/home/danilo/scripts/scmds.json", "r").read()
    jjson = json.loads(str_json)

    key_json = self.combo.get_active_text()
    tree_iter = combo.get_active_iter()

    if not key_json in jjson:
      self.buffer1.set_text('')
      self.entry.set_text('360')
      return

    cmd  = jjson[key_json]['cmd']
    time = jjson[key_json]['time']

    self.buffer1.set_text(cmd)
    self.entry.set_text(time)

  def on_button_clicked(self, widget):
    cmd = self.buffer1.get_text(self.buffer1.get_start_iter(), self.buffer1.get_end_iter(), False)
    time = self.entry.get_text()

    if self.combo.get_active_text() == None or not cmd or not time:
      return

    str_json = open("/home/danilo/scripts/scmds.json", "r").read()
    jjson = json.loads(str_json)

    key_json = self.combo.get_active_text()
    jjson[key_json] = { "cmd": cmd, "time": time }

    wids = open("/home/danilo/scripts/scmds.json", "w")
    wids.write(json.dumps(jjson))
    wids.close()

    sys.exit()

win = SaveShiftCmd()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
