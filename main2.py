import re
from colorthief import ColorThief
import os

def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

def generate_colors(dominant_color):
    r, g, b = dominant_color

    r_active = min(int(r * 1.2), 255)
    g_active = min(int(g * 1.2), 255)
    b_active = min(int(b * 1.2), 255)

    active_border = f"rgba({r_active:02x}{g_active:02x}{b_active:02x}{255:02x}) rgba({r_active:02x}{g_active:02x}{b_active:02x}{255:02x}) 45deg"
    
    r_inactive = int(r * 0.8)
    g_inactive = int(g * 0.8)
    b_inactive = int(b * 0.8)

    inactive_border = f"rgba({r_inactive:02x}{g_inactive:02x}{b_inactive:02x}{170:02x})"  # 170 — полупрозрачный

    colors = [f"{active_border}", f"{inactive_border}"]
    return colors

def apply_hyprland_config(color_cheme, config_file_path):
    with open(config_file_path, 'r') as file:
        config_data = file.read()

    config_data = re.sub(r'col.active_border = .+', f'col.active_border = {color_scheme[0]}', config_data)
    config_data = re.sub(r'col.inactive_border = .+', f'col.inactive_border = {color_scheme[1]}', config_data)

    with open(config_file_path, 'w') as file:
        file.write(config_data)

def setup_paper(path_paper, config_file_path):
    with open(config_file_path, 'r') as file:
        config_data = file.read()

    config_data = re.sub(r'preload = .+', f'preload = {path_paper}', config_data)
    config_data = re.sub(r'wallpaper = .+', f'wallpaper = eDP-1,{path_paper}', config_data)

    with open(config_file_path, 'w') as file:
        file.write(config_data)

    os.system('pkill hyprpaper')
    os.system('hyprpaper &')

if __name__ == "__main__":
    image_path = '/home/wzqrxzd/Wallpapers/walp2.jpg'
    config_path = '/home/wzqrxzd/.config/hypr/hyprland.conf'
    paper_config_path = '/home/wzqrxzd/.config/hypr/hyprpaper.conf'

    setup_paper(image_path, paper_config_path)
    dominant_color = get_dominant_color(image_path)
    color_scheme = generate_colors(dominant_color)
    apply_hyprland_config(color_scheme, config_path)

    print(f"dominant color: {dominant_color}")
    print(f"color active: {color_scheme[0]}")
    print(f"color inactive: {color_scheme[1]}")
