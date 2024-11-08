from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, DropDown, ScratchPad
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
import os, subprocess, json, re

mod = "mod4"
terminal = guess_terminal()

# pywal Colors
colors = os.path.expanduser('~/.cache/wal/colors.json')
colordict = json.load(open(colors))
ColorZ=(colordict['colors']['color0'])
ColorA=(colordict['colors']['color1'])
ColorB=(colordict['colors']['color2'])
ColorC=(colordict['colors']['color3'])
ColorD=(colordict['colors']['color4'])
ColorE=(colordict['colors']['color5'])
ColorF=(colordict['colors']['color6'])
ColorG=(colordict['colors']['color7'])
ColorH=(colordict['colors']['color8'])
ColorI=(colordict['colors']['color9'])




##############################
######## KEY BINDINGS ########
##############################
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.group.focus_back(), desc="Alternate between two most recent windows"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "Tab", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between different layouts
    Key([mod], "grave", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "x", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "w", lazy.window.toggle_maximize(), desc="Maximize window"),
    Key([mod], "s", lazy.window.toggle_minimize(), desc="Minimize window"),
    # Spawn hotkeys
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "r", lazy.spawn("rofi -show drun -show-icons"), desc="Spawn application launcher"),
    Key([mod], "b", lazy.spawn("firefox"), desc="Launch browser"),
    Key([mod, "shift"], "b", lazy.spawn("firefox --private-window"), desc="Launch private browser"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Take screenshot"),
    Key([mod, "shift"], "c", lazy.spawn(os.path.expanduser("~/.config/qtile/wallpaper_change.sh")), desc="Change wallpaper"),
    # Key([mod], "l", lazy.spawn("dm-tool switch-to-greeter"), desc="Lock screen (switch to greeter)"),
]
# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )




##############################
#### LAYOUT AND GROUP BOX ####
##############################
groups =[
    # Start Discord and Steam after PC boot up
    # Group("1", label = "", layout = "max", spawn = ["vesktop", "steam"], matches=[Match(wm_class=re.compile(r"^(vesktop|steam)$"))]),
    Group("1", label = "", layout = "max"),
    Group("2", label = "", layout = "max"),
    Group("3", label = "", layout = "columns"),
    Group("4", label = "", layout = "monadtall"),
    Group("5", label = "", layout = "columns"),
]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                'khal', 
                terminal +
                " --config-file " + os.path.expanduser("~/.config/alacritty/calendar.toml") +
                " -t ikhal -e ikhal ", 
                x=0.665, 
                width=0.33, 
                height=0.397, 
                opacity=1
            )
        ]
    )
)

layout_theme = {
    "border_width": 2,
    "margin": 5,
    "border_focus": ColorB,
    "border_normal": ColorD,
    "grow_amount": 1,
}

# layout modes when you press mod + ` (there is columns, max, monadtall and floating so far
layouts = [
    layout.Columns(
        **layout_theme,
        fair=False,
        border_on_single=True
        ),
    layout.Max(),
    # layout.Spiral(),
    layout.MonadTall(
        **layout_theme,
        fair=False,
        border_on_single=True
        ),
    layout.MonadWide(
        **layout_theme,
        fair=False,
        border_on_single=True
        ),
    layout.TreeTab(),
    layout.floating.Floating(
        **layout_theme,
        ),
]

widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()





##############################
###########  BAR  ############
##############################
text_foreground=ColorZ

def parse_window_name(text):
    '''Simplifies the names of a few windows, to be displayed in the bar'''
    target_names = [
        'Firefox',
        'Brave',
        'Chrome',
        'Edge',
        'VSCodium',
        'Discord',
        'Steam',
    ]
    try:
        return next(filter(lambda name: name in text, target_names), text)
    except TypeError:
        return text

forward_slash = {
    "decorations":
    [
        PowerLineDecoration(path="forward_slash")
    ],
}

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename="~/.config/qtile/arch.svg",
                    padding=6,
                    adjust_x=4,
                    #colour=ColorZ,
                    mask=True,
                    background=ColorA,
                    **forward_slash,
                ),
                widget.Spacer(
                    length=5,
                ),
                widget.GroupBox(
                    use_mouse_wheel=True,
                    highlight_method='text',
                    active=ColorG,
                    #inactive=ColorC,
                    this_current_screen_border=ColorC,
                    padding=3,
                    disable_drag=True,
                ),
                widget.Spacer(
                    length=15,
                ),
                widget.CurrentLayoutIcon(
                    scale = 0.67,
                    padding=6,
                    # foreground=text_foreground,
                ),
                widget.CurrentLayout(
                    scale = 0.78,
                    padding=3,
                    # foreground=text_foreground,
                ),
                widget.Sep(
                    linewidth=2,
                    padding=20,
                    size_percent=50,
                    # foreground=text_foreground,
                ),
                widget.WindowName(
                    fontsize=14,
                    padding=3,
                    parse_text=parse_window_name,
                    empty_group_string='Desktop',
                    # foreground=text_foreground,
                ),
                widget.Systray(
                    **forward_slash,
                ),
                widget.Spacer(
                    length=1,
                    background=ColorE,
                ),
                widget.TextBox(
                    text='',
                    fontsize=15,
                    padding=6,
                    background=ColorE,
                    # foreground=text_foreground,
                ),
                widget.Memory(
                    measure_mem='G',
                    format="{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
                    padding=6,
                    background=ColorE,
                    # foreground=text_foreground,
                ),
                widget.Spacer(
                    length=1,
                    background=ColorE,
                    **forward_slash,
                ),
                widget.TextBox(
                    text='',
                    fontsize=18,
                    padding=6,
                    background=ColorB,
                    # foreground=text_foreground,
                ),
                widget.ThermalSensor(
                    tag_sensor='Tctl',
                    format="CPU {temp:.0f}{unit}",
                    threshold=80,
                    foreground_alert='ff6000',
                    background=ColorB,
                    # foreground=text_foreground,
                    padding=3
                ),
                widget.NvidiaSensors(
                    format="GPU {temp}°C",
                    threshold=80,
                    foreground_alert='ff6000',
                    padding=6,
                    background=ColorB,
                    # foreground=text_foreground,
                ),
                widget.Spacer(
                    length=1,
                    background=ColorB,
                    **forward_slash,
                ),
                widget.CheckUpdates(
                    distro="Arch_checkupdates",
                    no_update_string="No updates",
                    display_format="Pacman: {updates}",
                    colour_have_updates="ffffff",
                    colour_no_updates="ffffff",
                    background=ColorC,
                    padding=6,
                ),
                widget.Spacer(
                    length=1,
                    background=ColorC,
                    **forward_slash,
                ),
                widget.Volume(
                    emoji=True,
                    emoji_list = [' ', ' ', ' ', ' '],
                    fontsize=14,
                    # mouse_callbacks = {"Button1": lazy.spawn("pavucontrol")},
                    volume_app = "pavucontrol", # uses Button2 by default
                    background=ColorH,
                    # foreground=text_foreground,
                    padding=6,
                ),
                widget.Volume(
                    # mouse_callbacks = {"Button1": lazy.spawn("pavucontrol")},
                    volume_app = "pavucontrol", # uses Button2 by default
                    background=ColorH,
                    # foreground=text_foreground,
                    padding=3,
                ),
                widget.Spacer(
                    length=1,
                    background=ColorH,
                    **forward_slash,
                ),
                widget.Clock(
                    format="%a %d/%m/%y %H:%M",
                    background=ColorA,
                    # foreground=text_foreground,
                    padding=6,
                    mouse_callbacks={"Button1": lazy.group['scratchpad'].dropdown_toggle('khal')},
                ),
            ],
            24,
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# auto-start apps on startup
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/wallpaper_change.sh')
    subprocess.Popen([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
