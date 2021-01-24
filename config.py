#l3ox qtile config

import os
import subprocess

from typing import List
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"

keys = [
    Key([mod], "h", lazy.layout.left()),  # focus left
    Key([mod], "l", lazy.layout.right()), # focus right
    Key([mod], "j", lazy.layout.down()),  # focus down
    Key([mod], "k", lazy.layout.up()),    # focus up
    Key([mod], "space", lazy.layout.next()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),  # move window left
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()), # move window right
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),  # move window down
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),    # move window up
    
    Key([mod, "control"], "h", lazy.layout.grow_left()),  # grow window left
    Key([mod, "control"], "l", lazy.layout.grow_right()), # grow window right
    Key([mod, "control"], "j", lazy.layout.grow_down()),  # grow window down
    Key([mod, "control"], "k", lazy.layout.grow_up()),    # grow window up
    
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn("gnome-terminal")),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd())
]

layout_theme = {"border_width": 3,
                "margin": 3,
                "border_focus": "50fa7b",
                "border_normal": "282a36"
                }

layouts = [
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Floating(**layout_theme),
    layout.MonadTall(**layout_theme)
]

widget_defaults = dict(
    font='mononoki bold',
    fontsize=13,
    padding=4,
    background=("#282a36"),
    foreground=("#bd93f9")
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(linewidth = 2, padding = 6),
                widget.Image(filename = "~/.config/qtile/icons/python.png"),
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Sep(linewidth = 2, padding = 6),
                widget.Prompt(),    
                widget.WindowName(),
                widget.Sep(linewidth = 2, padding = 6),
                widget.Chord(
                    chords_colors={
                        'launch': ("#bd93f9", "#282a36"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.BitcoinTicker(format="BTC: {avg}", **widget_defaults),
                widget.Sep(linewidth = 2, padding = 6),
                # widget.CPUGraph(
                #     core='all',
                #     width=30,
                #     frequency=5,
                #     samples=100
                # ),
                # widget.Memory(
                #      mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn("gnome-terminal" + ' -e htop')},
                #      width=30,
                #      padding=5
                #      ),

                widget.Clock(format='%m-%d %a %I:%M %p'),
                widget.Sep(linewidth = 2, padding = 6),
                widget.QuickExit(),
                widget.Sep(linewidth = 2, padding = 6),
            ],
            30,
        ),
    ),
]

groups = [Group(i) for i in "123"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])
    
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='Steam'),
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
    
auto_fullscreen = True
focus_on_window_activation = "smart"	
wmname = "LG3D"
