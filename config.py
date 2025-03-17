import asyncio
from libqtile import bar, layout, widget
from libqtile.config import Drag, Group, Key, Match, Screen, Click
from libqtile.lazy import lazy

mod = "mod4"
terminal = "alacritty"

# Async command runner
async def run_command(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return stdout.decode().strip()

# Key bindings with proper window resizing
keys = [
    # Navigation
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),
    
    # Window manipulation with proper grow commands
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
    Key([mod], "p", lazy.spawn("rofi -show drun")),
    
    # Layout control
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),
    Key([mod], "c", lazy.window.kill()),
]

# Improved Group System
groups = [
    Group("1", label="DEV", matches=[Match(wm_class="code"), Match(wm_class="jetbrains-.*")]),
    Group("2", label="WEB", matches=[Match(wm_class="firefox"), Match(wm_class="chromium")]),
    Group("3", label="COM", matches=[Match(wm_class="thunderbird"), Match(wm_class="discord")]),
    Group("4", label="MED", matches=[Match(wm_class="vlc"), Match(wm_class="gimp")]),
    Group("5", label="SYS", matches=[Match(wm_class="alacritty"), Match(wm_class="htop")]),
    Group("6", label="DOC", matches=[Match(wm_class="libreoffice"), Match(wm_class="evince")]),
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

# Layouts with proper grow settings
layouts = [
    layout.Columns(
        border_focus="#ff79c6",
        border_normal="#bd93f9",
        border_width=2,
        margin=4,
        insert_position=1,
        grow_amount=10  # Added grow amount for better resizing
    ),
    layout.Max(),
    layout.MonadTall(
        border_focus="#ff79c6",
        border_normal="#bd93f9",
        border_width=2,
        margin=4,
        ratio=0.65,
        change_ratio=0.05,
        min_ratio=0.25,
        max_ratio=0.75,
        grow_amount=10
    ),
]

# Bottom Bar Setup
def create_bar(primary=True):
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
                urgent_alert_method="block",
                this_current_screen_border="#ff79c6",
                spacing=10,
            ),
            widget.Sep(linewidth=2, padding=10),
            widget.WindowName(max_chars=40, empty_group_string="Desktop"),
            widget.Spacer(),
            widget.Clock(
                format="%Y-%m-%d %a %I:%M %p",
                update_interval=10,
                foreground="#8be9fd"
            ),
            widget.Systray() if primary else widget.CurrentLayoutIcon(),
        ],
        48,
        margin=[6, 8, 2, 8],
        background="#282a36dd",
        opacity=0.95,
    )

screens = [
    Screen(bottom=create_bar(primary=True)),
    Screen(bottom=create_bar(primary=False)),
]

# Fixed Mouse Configuration
mouse = [
    Drag([mod], "Button1", 
        lazy.window.set_position_floating(),
        start=lazy.window.get_position()
    ),
    Drag([mod], "Button3", 
        lazy.window.set_size_floating(),
        start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# Widget defaults
widget_defaults = dict(
    font="JetBrains Mono Medium",
    fontsize=18,
    padding=4,
    background="#282a36",
    foreground="#f8f8f2",
)
extension_defaults = widget_defaults.copy()

# Floating layout
floating_layout = layout.Floating(
    border_focus="#ff79c6",
    border_normal="#bd93f9",
    border_width=2,
    fullscreen_border_width=0,
    max_border_width=0,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ]
)

# General configuration with fixed focus settings
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True  # Enable mouse focus following
bring_front_click = True   # Bring window to front on click
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None

wmname = "LG3D"
