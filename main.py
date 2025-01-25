from wallpapers import WallpaperController
from hyprland import HyprlandController
from waybar import WaybarController
from cava import CavaController
from wofi import WofiController
from colorthief import ColorThief

import os
import re

def get_color_palette(image_path, color_count=5):
    color_thief = ColorThief(image_path)
    color_palette = color_thief.get_palette(color_count=color_count, quality=1)
    return color_palette

def preview_color(color):
    r, g, b = color
    print(f'\033[48;2;{r};{g};{b}m {r} {g} {b} \033[0m')

def choose_color_from_palette(color_palette):
    try:
        for index, color in enumerate(color_palette, start=1):
            print(f"{index}: ", end = "")
            preview_color(color)
        index = int(input(f"Choose a color by index (1-{index}): "))
        return color_palette[index-1]
    except (ValueError, IndexError):
        print("Invalid input. Defaulting to the first color.")
        return color_palette[0]

def choose_wallpaper():
    wallpaper_index = input('input index of your image, or -1 if u want random: ')

    if wallpaper_index != '-1':
        wallpaper = f"walp{wallpaper_index}"
    else:
        wallpaper = '-1'
    return wallpaper


if __name__ == "__main__":
    wallpapers_path = "/home/wzqrxzd/Wallpapers"
    hyprland_path =  "/home/wzqrxzd/.config/hypr/hyprland.conf"
    hyprpaper_path = "/home/wzqrxzd/.config/hypr/hyprpaper.conf"
    waybar_path = "/home/wzqrxzd/.config/waybar/style.css"
    cava_path = "/home/wzqrxzd/.config/cava/config"
    wofi_path = "/home/wzqrxzd/.config/wofi/style.css"

    wallpaper = choose_wallpaper()

    wallpaper_cntrl = WallpaperController(hyprpaper_path, wallpapers_path, wallpaper)
    wallpaper_cntrl.apply_wallpaper()

    color_palette = get_color_palette(wallpaper_cntrl.current_wallpaper_path)
    selected_color = choose_color_from_palette(color_palette)

    hyprland_cntrl = HyprlandController(hyprland_path, selected_color)
    hyprland_cntrl.apply_hyprland_config()

    waybar_cntrl = WaybarController(waybar_path, selected_color)
    waybar_cntrl.apply_waybar_config()

    cava_cntrl = CavaController(cava_path, selected_color)
    cava_cntrl.apply_cava_config()

    wofi_cntrl = WofiController(wofi_path, selected_color)
    wofi_cntrl.apply_wofi_config()
