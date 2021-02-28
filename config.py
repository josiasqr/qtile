# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import socket

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [

    Key([mod], "h", lazy.layout.left(), desc = "Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc = "Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc = "Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc = "Move focus up"),
    Key([mod], "r", lazy.spawncmd(), desc = "Spawn a command using a prompt widget"),
    Key([mod], "w", lazy.window.kill(), desc = "Kill focused window"),
    Key([mod], "m", lazy.layout.maximize(), desc = 'toggle window between minimum and maximum sizes'),
    Key([mod], "n", lazy.layout.normalize(), desc = "Reset all window sizes"),
    Key([mod], "Tab", lazy.next_layout(), desc = "Toggle between layouts"),
    Key([mod], "space", lazy.layout.next(), desc = "Move window focus to other window"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc = "Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc = "Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc = "Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc = "Move window up"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc = 'toggle floating'),
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show drun -show-icons"), desc="Move window up"),
    Key([mod, "shift"], "space",lazy.layout.rotate(), lazy.layout.flip(), desc = 'Switch which side main pane occupies (XmonadTall)'),

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc = "Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc = "Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc = "Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc = "Grow window up"),
    Key([mod, "control"], "Return", lazy.layout.toggle_split(), desc = "Toggle between split and unsplit sides of stack"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    

]


group_names = [("WWW", {'layout': 'monadtall'}),
               ("DEV", {'layout': 'monadtall'}),
               ("SYS", {'layout': 'monadtall'}),
               ("DOC", {'layout': 'monadtall'}),
               ("VBOX", {'layout': 'floating'}),
               ("CHAT", {'layout': 'tile'}),
               ("MUS", {'layout': 'tile'}),
               ("VID", {'layout': 'monadtall'}),
               ("GFX", {'layout': 'floating'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group


layout_theme = {"border_width": 2,
                "margin": 1,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

prompt = "{0}@{1}".format(os.environ["USER"], socket.gethostname())

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Stack(**layout_theme, num_stacks=2),
    layout.TreeTab(
         font = "Ubuntu",
         fontsize = 10,
         sections = ["FIRST", "SECOND"],
         section_fontsize = 11,
         bg_color = "141414",
         active_bg = "90C435",
         active_fg = "000000",
         inactive_bg = "384323",
         inactive_fg = "a0a0a0",
         padding_y = 5,
         section_top = 10,
         panel_width = 320
         ),
    layout.Floating(**layout_theme)
]


colors = [["#282c34", "#282c34"], # panel background
          ["#434758", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#8d62a9", "#8d62a9"], # border line color for other tab and odd widgets
          ["#668bd7", "#668bd7"], # color for the even widgets
          ["#e1acff", "#e1acff"]] # window name

#ff5555
##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)

extension_defaults = widget_defaults.copy()

def open_pacman(qtile):
    qtile.cmd_spawn('alacritty -e sudo pacman -Syu')

screens = [
    Screen(
        top=bar.Bar([
            widget.Sep(
                linewidth = 0,
                padding = 5,
                foreground = colors[2],
                background = colors[0]
                ),
            widget.GroupBox(
                font = "Ubuntu Bold",
                fontsize = 9,
                margin_y = 3,
                margin_x = 0,
                padding_y = 5,
                padding_x = 3,
                borderwidth = 3,
                active = colors[2],
                inactive = colors[2],
                rounded = False,
                highlight_color = colors[1],
                highlight_method = "line",

                this_current_screen_border = colors[3],
                this_screen_border = colors [4],
                other_current_screen_border = colors[3],
                other_screen_border = colors[0],
                
                foreground = colors[2],
                background = colors[0]
                ),
            widget.Prompt(
                prompt = prompt + ': ',
                font = "Ubuntu Mono",
                padding = 10,
                foreground = colors[3],
                background = colors[1]
                ),
            widget.Sep(
                linewidth = 0,
                padding = 10,
                foreground = colors[2],
                background = colors[0]
                ),
            widget.CurrentLayoutIcon(
                #custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                foreground = colors[2],
                background = colors[0],
                padding = 0,
                scale = 0.7
                ),
            widget.CurrentLayout(
                foreground = colors[2],
                background = colors[0],
                padding = 5
                ),
            widget.Sep(
                linewidth = 1,
                padding = 10,
                foreground = colors[2],
                background = colors[0]
                ),
            widget.WindowName(
                foreground = colors[6],
                background = colors[0],
                padding = 5
                ),
            widget.TextBox(
                text = '',
                background = colors[0],
                foreground = colors[1],
                padding = 0,
                fontsize = 37
            ),
            widget.TextBox(
                text = '',
                background = colors[1],
                foreground = colors[5],
                padding = 0,
                fontsize = 37
                ),
            widget.Net(
                interface = "enp4s0",
                format = '{down} ↓↑ {up}',
                foreground = colors[2],
                background = colors[5],
                padding = 5
                ),
            # widget.TextBox(
            #     text = " Vol:",
            #     foreground = colors[2],
            #     background = colors[5],
            #     padding = 0
            #     ),
            # widget.Volume(
            #     foreground = colors[2],
            #     background = colors[5],
            #     padding = 5
            #     ),
            widget.TextBox(
                text = '',
                background = colors[5],
                foreground = colors[4],
                padding = 0,
                fontsize = 37
                ),
            widget.TextBox(
                text = '勒',
                background = colors[4],
                foreground = colors[2],
                padding = 3,
                fontsize = 17
                ),
            widget.CheckUpdates(
                no_update_string ='0',
                #update_interval = 1800,
                mouse_callbacks = {'Button1': open_pacman},
                foreground = colors[2],
                background = colors[4]
                ),
            widget.TextBox(
                text = "Updates",
                mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('alacritty -e sudo pacaman -Syu')},
                padding = 5,
                foreground = colors[2],
                background = colors[4]
                ),
            widget.TextBox(
                text = '',
                background = colors[4],
                foreground = colors[5],
                padding = 0,
                fontsize = 37
                ),
            widget.TextBox(
                text = '',
                background = colors[5],
                foreground = colors[2],
                padding = 3,
                fontsize = 17
                ),
            widget.Clock(
                foreground = colors[2],
                background = colors[5],
                format='%A, %B %d - [ %H:%M ]'
                ),
            widget.TextBox(
                text = '',
                background = colors[5],
                foreground = colors[4],
                padding = 0,
                fontsize = 37
                ),
            widget.Systray(
                background = colors[4],
                padding = 5
               ),
            widget.Sep(
                linewidth = 0,
                padding = 10,
                foreground = colors[0],
                background = colors[4]
                ),
        ],
        24,
    ),
    wallpaper='~/Images/wallpers/espacio.jpg',
    wallpaper_mode='fill',
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# ejecuatar algunos comandos cuanod inicia qtile
autostarts = [
    "picom -b",
    "volumeicon &"
]
for autostart in autostarts:
    os.system(autostart)
    
