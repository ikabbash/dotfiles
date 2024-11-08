#!/bin/bash

# for Rofi
PREV_COLOR=$(xrdb -query | grep '*color3' | awk '{print $2}')
ROFI_THEME="square-dark.rasi"

# Wallpapers path
feh --bg-max --randomize ~/Pictures/wallpapers/*
wal -i $(cat ~/.fehbg | cut -d"'" -f2 | awk 'NR==2')

NEW_COLOR=$(xrdb -query | grep '*color3' | awk '{print $2}')
# This might need to be modified
sed -i "s/${PREV_COLOR}/${NEW_COLOR}/g" ~/.local/share/rofi/themes/${ROFI_THEME}

qtile cmd-obj -o cmd -f reload_config