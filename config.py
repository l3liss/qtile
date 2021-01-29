#l3ox qtile config

import os
import psutil
import socket
import subprocess

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.widget import (Clock, CurrentLayout, CurrentLayoutIcon,
                             GroupBox, Notify, PulseVolume, Prompt, Sep,
                             Spacer, Systray, TaskList, TextBox)

mod = "mod4"

keys = [
	# movement controls
    Key([mod], "h", lazy.layout.left()),  # focus left
    Key([mod], "l", lazy.layout.right()), # focus right
    Key([mod], "j", lazy.layout.down()),  # focus down
    Key([mod], "k", lazy.layout.up()),    # focus up
    Key([mod], "space", lazy.layout.next()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),  # move window left
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()), # move window right
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),  # move window down
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),    # move window up
    Key([mod, "control"], "h", lazy.layout.grow_left()),   # grow window left
    Key([mod, "control"], "l", lazy.layout.grow_right()),  # grow window right
    Key([mod, "control"], "j", lazy.layout.grow_down()),   # grow window down
    Key([mod, "control"], "k", lazy.layout.grow_up()),     # grow window up   
    Key([mod], "n", lazy.layout.normalize()),		   # reset window sizes
    Key([mod], "Tab", lazy.next_layout()),		   # switch between layouts
    Key([mod], "w", lazy.window.kill()),		   # kill window
    Key([mod, "control"], "r", lazy.restart()),		   # restart qtile
    Key([mod, "control"], "q", lazy.shutdown()),	   # shutdown qtile
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "Return", lazy.spawn("alacritty")),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
	# applications
    Key([mod, "mod1"], "b", lazy.spawn("qutebrowser")),
    Key([mod, "mod1"], "s", lazy.spawn("steam")),
    Key([mod, "mod1"], "e", lazy.spawn("pcmanfm"))
]

def init_floating_layout():
    return layout.Floating(border_focus="ffb86c")
    
def init_layouts():
    margin = 0
    if len(qtile.conn.pseudoscreens) > 1:
        margin = 8
    l3liss = dict (margin=margin, border_width=3, border_normal="282a36",
                  border_focus="50fa7b", border_focus_stack="ffb86c")
    layouts = [
        layout.Max(),
        layout.Columns(border_on_single=True, num_columns=2, grow_amount=5, **l3liss)
    ]
    return layouts
  
widget_defaults = dict (
    font='mononoki bold',
    fontsize=13,
    padding=6,
    background=("#282a36"),
    foreground=("#bd93f9")
)

extension_defaults = widget_defaults.copy()

def init_widgets():
    widgets = [
	widget.Sep(linewidth = 2, padding = 6),
	widget.Image(filename="~/.config/qtile/icons/python.png"),
        CurrentLayoutIcon(scale=0.6, padding=8),
        GroupBox(fontsize=8, padding=4, borderwidth=1, urgent_border="6272a4",
                 disable_drag=True, highlight_method="block",
                 this_screen_border="6272a4", other_screen_border="ff5555",
                 this_current_screen_border="8be9fd",
                 other_current_screen_border="ffb86c"),
        widget.Prompt(),    
        widget.WindowName(),
        widget.Systray(),
        Notify(fmt=" 🔥 {} "),
        widget.Sep(linewidth = 2, padding = 6),
        widget.BitcoinTicker(format="BTC: {avg}", **widget_defaults),
        #PulseVolume(fmt=" {}", emoji=True, volume_app="pavucontrol"),
        #PulseVolume(volume_app="pavucontrol"),
        Clock(format=" ⏱ %H:%M  <span color='#666'>%A %d-%m-%Y</span>"),
        widget.Sep(linewidth = 2, padding = 6),
        ]
    return widgets

groups = [Group(i) for i in "123"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name))
    ])
 
def init_mouse():
    mouse = [Drag([mod], "Button1", lazy.window.set_position_floating(),
                  start=lazy.window.get_position()),
             Drag([mod], "Button3", lazy.window.set_size_floating(),
                  start=lazy.window.get_size()),
             Click([mod], "Button2", lazy.window.bring_to_front())]
    return mouse

@hook.subscribe.client_new
def set_floating(window):
    floating_layout = init_floating_layout()
    layouts = init_layouts()
    floating_classes = ("pcmanfm")
    try:
        if window.window.get_wm_class()[0] in floating_classes:
            window.floating = True
    except IndexError:
        pass

@hook.subscribe.client_new
def set_parent(window):
    client_by_pid = {}
    for client in qtile.windows_map.values():
        client_pid = client.window.get_net_wm_pid()
        client_by_pid[client_pid] = client

    pid = window.window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    while ppid:
        window.parent = client_by_pid.get(ppid)
        if window.parent:
            return
        ppid = psutil.Process(ppid).ppid()

@hook.subscribe.client_new
def swallow(window):
    if window.parent:
        window.parent.minimized = True

@hook.subscribe.client_killed
def unswallow(window):
    if window.parent:
        window.parent.minimized = False
    
auto_fullscreen = False
focus_on_window_activation = "never"	
dgroups_key_binder = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = init_floating_layout()
layouts = init_layouts()
mouse = init_mouse()
widgets = init_widgets()
bar = bar.Bar(widgets=widgets, size=30, opacity=1)
screens = [Screen(top=bar)]
wmname = "Qtile"
