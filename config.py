from libqtile import bar, layout, widget, hook
from libqtile.config import Drag, Group, Screen
from libqtile.lazy import lazy
import subprocess

# Function to get connected screen identifiers
def get_screen_identifiers():
    xrandr_output = subprocess.check_output(["xrandr"]).decode("utf-8")
    screens = []
    for line in xrandr_output.splitlines():
        if " connected" in line:
            parts = line.split()
            screen_name = parts[0]
            screens.append(screen_name)
    return screens

# Function to assign groups to screens
def assign_groups_to_screens(qtile):
    screen_identifiers = get_screen_identifiers()
    for group in qtile.groups:
        if group.name == "1" or group.name == "5":  # DEV or SYS
            group.toscreen(1 if "HDMI-0" in screen_identifiers else 0)
        else:  # WEB, COM, MED, DOC
            group.toscreen(0 if "DP-0" in screen_identifiers else 1)

# Groups
groups = [
    Group("1", label="DEV", matches=[Match(wm_class="code"), Match(wm_class="jetbrains-.*")], screen_affinity=1),  # HDMI-0
    Group("2", label="SYS", matches=[Match(wm_class="alacritty"), Match(wm_class="htop")], screen_affinity=1),  # HDMI-0
    Group("3", label="WEB", matches=[Match(wm_class="firefox"), Match(wm_class="chromium")], screen_affinity=0),  # DP-0
    Group("4", label="COM", matches=[Match(wm_class="thunderbird"), Match(wm_class="discord")], screen_affinity=0),  # DP-0
    Group("5", label="MED", matches=[Match(wm_class="vlc"), Match(wm_class="gimp")], screen_affinity=0),  # DP-0
    Group("6", label="DOC", matches=[Match(wm_class="libreoffice"), Match(wm_class="evince")], screen_affinity=0),  # DP-0
]

# Layouts
layouts = [
    layout.Columns(
        border_focus="#ff79c6",
        border_normal="#bd93f9",
        border_width=2,
        margin=4,
    ),
    layout.Max(),
]

# Bar setup
def create_bar(visible_groups):
    # Default to primary screen for Systray
    return bar.Bar(
        [
            widget.TextBox(" § ", fontsize=21, padding=10, foreground="#ff79c6"),
            widget.Sep(linewidth=2, padding=10),
            widget.GroupBox(
                active="#50fa7b",
                inactive="#6272a4",
                borderwidth=2,
                highlight_method="block",
                block_highlight_text_color="#ff79c6",
                disable_drag=True,
                visible_groups=visible_groups,  # Set which groups to show on each screen
            ),
            widget.WindowName(max_chars=40, empty_group_string="Desktop"),
            widget.Spacer(),
            widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
            # Only add Systray on the primary screen (DP-0)
            widget.Systray() if "3" in visible_groups or "4" in visible_groups else widget.CurrentLayoutIcon(),
        ],
        48,
        background="#282a36dd",
        opacity=0.95,
    )

# Screens setup
screens = [
    Screen(
        bottom=create_bar(visible_groups=["3", "4", "5", "6"]),  # Groups on DP-0
    ),
    Screen(
        bottom=create_bar(visible_groups=["1", "2"]),  # Groups on HDMI-0
    ),
]

# Mouse config
mouse = [
    Drag(["mod4"], "Button1", lazy.window.set_position_floating()),
    Drag(["mod4"], "Button3", lazy.window.set_size_floating()),
]

# Hooks
@hook.subscribe.startup_once
def startup():
    assign_groups_to_screens(qtile)

@hook.subscribe.screen_change
def screen_change(qtile):
    assign_groups_to_screens(qtile)
