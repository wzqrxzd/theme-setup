from wallpapers import WallpaperController
from hyprland import HyprlandController
from waybar import WaybarController
from cava import CavaController
from wofi import WofiController
from colorthief import ColorThief

import os
import subprocess

def get_color_palette(image_path, color_count=5):
    color_thief = ColorThief(image_path)
    color_palette = color_thief.get_palette(color_count=color_count, quality=1)
    return color_palette

def launch_wofi(prompt="Select an option", options=None):
    if options is None:
        options = []

    # options = sorted(options, key=lambda x: int(x))
    
    # Prepare the Wofi command
    wofi_command = [
        "wofi", "--show", "dmenu", "--prompt", prompt
    ]


    # Run Wofi as a subprocess
    try:
        result = subprocess.run(
            wofi_command,
            input="\n".join(options).encode('utf-8'),  # Pass options as input
            stdout=subprocess.PIPE,                   # Capture output
            stderr=subprocess.PIPE,                   # Capture errors
            check=True                                # Raise exception on error
        )
        # Process the result
        selected_option = result.stdout.decode('utf-8').strip()
        return selected_option if selected_option else None
    except subprocess.CalledProcessError as e:
        print(f"Wofi failed: {e.stderr.decode('utf-8')}")
        return None
    except FileNotFoundError:
        print("Wofi is not installed or not in PATH.")
        return None

def choose_wallpaper_and_color(hyprpaper_path, wallpapers_path):
    file_count = len([f for f in os.listdir(wallpapers_path) if os.path.isfile(os.path.join(wallpapers_path, f))])
    options = [f"{i}" for i in range(1,file_count+1)]   

    wallpaper_index = launch_wofi("Chose a wallpaper:", options)
    if not wallpaper_index:
        return None, None

    wallpaper_name = f"walp{wallpaper_index}"
    wallpaper_path = os.path.join(wallpapers_path, wallpaper_name)

    wallpaper_cntrl = WallpaperController(hyprpaper_path, wallpapers_path, wallpaper_name)
    wallpaper_cntrl.apply_wallpaper()

    color_palette = get_color_palette(wallpaper_cntrl.current_wallpaper_path)

    color_options = [f"{index + 1}: {color}" for index, color in enumerate(color_palette)]
    selected_color_option = launch_wofi("Choose a color from the palette:", color_options)

    if selected_color_option:
        selected_color_index = int(selected_color_option.split(":")[0]) - 1
        selected_color = color_palette[selected_color_index]
        return selected_color
    else:
        return color_palette[0]

if __name__ == "__main__":
    wallpapers_path = "/home/wzqrxzd/Wallpapers"
    hyprland_path =  "/home/wzqrxzd/.config/hypr/hyprland.conf"
    hyprpaper_path = "/home/wzqrxzd/.config/hypr/hyprpaper.conf"
    waybar_path = "/home/wzqrxzd/.config/waybar/style.css"
    cava_path = "/home/wzqrxzd/.config/cava/config"
    wofi_path = "/home/wzqrxzd/.config/wofi/style.css"

    selected_color = choose_wallpaper_and_color(hyprpaper_path, wallpapers_path)
    hyprland_cntrl = HyprlandController(hyprland_path, selected_color)
    hyprland_cntrl.apply_hyprland_config()

    waybar_cntrl = WaybarController(waybar_path, selected_color)
    waybar_cntrl.apply_waybar_config()

    cava_cntrl = CavaController(cava_path, selected_color)
    cava_cntrl.apply_cava_config()

    wofi_cntrl = WofiController(wofi_path, selected_color)
    wofi_cntrl.apply_wofi_config()
