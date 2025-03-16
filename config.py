from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Dracula color palette
dracula_bg        = "#282a36"
dracula_current   = "#44475a"
dracula_fg        = "#f8f8f2"
dracula_purple    = "#bd93f9"
dracula_pink      = "#ff79c6"
dracula_cyan      = "#8be9fd"
dracula_green     = "#50fa7b"
dracula_orange    = "#ffb86c"
dracula_comment   = "#6272a4"

mod = "mod4"
terminal = guess_terminal()

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle split/unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Bind mod+p to launch rofi (optional alternative)
    Key([mod], "p", lazy.spawn("rofi -show drun"), desc="Launch rofi menu"),
]

# Define 6 groups (workspaces).
groups = [Group(i) for i in "123456"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc=f"Switch to & move focused window to group {i.name}"),
    ])

layouts = [
    layout.Columns(border_focus_stack=[dracula_pink, dracula_purple], border_width=4, margin=3),
    layout.Max(margin=3),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
    background=dracula_bg,
    foreground=dracula_fg,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                # Decorative "Qtile" widget as an art piece.
                widget.TextBox(
                    "Qtile",
                    foreground=dracula_fg,
                    background=dracula_bg,
                    fontsize=16,
                    font="sans bold",
                    padding=10,
                    markup=True,
                ),
                # A separator for style.
                widget.Sep(linewidth=2, padding=10, foreground=dracula_comment, background=dracula_bg),
                # GroupBox with Dracula colors.
                widget.GroupBox(
                    active=dracula_green,
                    inactive=dracula_comment,
                    borderwidth=2,
                    highlight_method="line",
                    this_current_screen_border=dracula_pink,
                    this_screen_border=dracula_cyan,
                    other_screen_border=dracula_orange,
                    background=dracula_bg,
                ),
                widget.Sep(linewidth=2, padding=10, foreground=dracula_comment, background=dracula_bg),
                widget.Prompt(),
                widget.Sep(linewidth=2, padding=10, foreground=dracula_comment, background=dracula_bg),
                # Display the current window name.
                widget.WindowName(foreground=dracula_fg, background=dracula_bg),
                widget.Sep(linewidth=2, padding=10, foreground=dracula_comment, background=dracula_bg),
                # Chord widget with Dracula accent colors.
                widget.Chord(
                    chords_colors={"launch": (dracula_pink, dracula_fg)},
                    name_transform=lambda name: name.upper(),
                    background=dracula_bg,
                ),
                widget.Sep(linewidth=2, padding=10, foreground=dracula_comment, background=dracula_bg),
                # Clock widget
                widget.Clock(format="%Y-%m-%d %a %I:%M %p", foreground=dracula_fg, background=dracula_bg),
            ],
            24,
            background=dracula_bg,
        ),
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
    ],
    background=dracula_bg
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

wmname = "LG3D"
