from libqtile.config import Key
from libqtile.lazy import lazy

mod = "mod4"
terminal = "alacritty"

keys = [
    # Navigation
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),

    # Move window to a specific workspace
    Key([mod, "shift"], "1", lazy.window.togroup("1")),
    Key([mod, "shift"], "2", lazy.window.togroup("2")),
    Key([mod, "shift"], "3", lazy.window.togroup("3")),
    Key([mod, "shift"], "4", lazy.window.togroup("4")),
    Key([mod, "shift"], "5", lazy.window.togroup("5")),
    Key([mod, "shift"], "6", lazy.window.togroup("6")),

    # Window manipulation
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),

    # System
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),

    # Applications
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "s", lazy.spawn("launch_steam.sh")),
    Key([mod], "p", lazy.spawn("rofi -show drun")),

    # Layout control
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),
    Key([mod], "c", lazy.window.kill()),

    # Workspace switching for HDMI-0 (dev, sys groups) - **Only swap between DEV and SYS on HDMI-0**
    Key([mod], "1", lazy.group["1"].toscreen(1)),  # Switch to DEV on HDMI-0
    Key([mod], "2", lazy.group["2"].toscreen(1)),  # Switch to SYS on HDMI-0
    
    # Switch to DP-0 (web, com, med, doc groups) without affecting HDMI-0
    Key([mod], "3", lazy.group["3"].toscreen(0)),  # Switch to group 3 (WEB) on DP-0
    Key([mod], "4", lazy.group["4"].toscreen(0)),  # Switch to group 4 (COM) on DP-0
    Key([mod], "5", lazy.group["5"].toscreen(0)),  # Switch to group 5 (MED) on DP-0
    Key([mod], "6", lazy.group["6"].toscreen(0)),  # Switch to group 6 (DOC) on DP-0
]
