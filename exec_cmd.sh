#!/bin/bash

# get the window_id for the current active window
win_id="$(xdotool getwindowfocus)"

# Get the x and y coords for the current window, top left-hand corner.
x=$(xwininfo -id $win_id | awk '/Abs.+X/ { sub(/^.+\s/,""); print }')
y=$(xwininfo -id $win_id | awk '/Abs.+Y/ { sub(/^.+\s/,""); print }')

# Shift the coords by 30 pixels, down and across.
(( x=6780 , y=2332 ))

# Move the current window to the new coords, $x $y.
xdotool getwindowfocus windowmove  $x $y
xdotool windowsize $(xdotool getactivewindow) 2400 1331

source /home/danilo/.bashrc

printf 0x%x "$(xdotool getwindowfocus)" > "/home/danilo/scripts/win_$1"

cmd="$(/home/danilo/scripts/get_value_json.py /home/danilo/scripts/scmds.json $1 cmd)"
time="$(/home/danilo/scripts/get_value_json.py /home/danilo/scripts/scmds.json $1 time)"

echo "
#
#  $cmd
#
"

gsettings set org.gtk.Settings.Debug enable-inspector-keybinding true
eval $cmd
gsettings set org.gtk.Settings.Debug enable-inspector-keybinding false

echo "
#
#
#
"

read "-t$time" -p "Press enter to continue"
exit
