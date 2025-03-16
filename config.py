from libqtile import bar, layout, widget
from libqtile.config import Drag, Group, Key, Match, Screen, Click
from libqtile.lazy import lazy

mod = "mod4"
terminal = "alacritty"

keys = [
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "c", lazy.window.kill()),  # changed kill window to mod+c
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "p", lazy.spawn("rofi -show drun")),
]

groups = [Group(i) for i in "123456"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

layouts = [
    layout.Columns(border_focus_stack=["#ff79c6", "#bd93f9"], border_width=4, margin=3),
    layout.Max(margin=3),
]

widget_defaults = dict(
    font="sans",
    fontsize=15,
    padding=6,
    background="#282a36",
    foreground="#f8f8f2",
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.TextBox(" § ", foreground="#f8f8f2", background="#282a36", fontsize=21, font="sans bold", padding=10, markup=True),
                widget.Sep(linewidth=2, padding=10, foreground="#6272a4"),
                widget.GroupBox(
                    active="#50fa7b",
                    inactive="#6272a4",
                    borderwidth=3,
                    highlight_method="line",
                    this_current_screen_border="#ff79c6",
                    this_screen_border="#8be9fd",
                    other_screen_border="#ffb86c",
                ),
                widget.Sep(linewidth=2, padding=10, foreground="#6272a4"),
                widget.WindowName(),
                widget.Sep(linewidth=2, padding=10, foreground="#6272a4"),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p", update_interval=60),
            ],
            24,
            background="#282a36",
        ),
        x11_drag_polling_rate=60,
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

wmname = "LG3D"
