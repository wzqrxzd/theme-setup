import re
import os
import subprocess
from colorthief import ColorThief

def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

def rgb_to_hex(color):
    r, g, b = color
    r = min(int(r * 1.2), 255)
    g = min(int(g * 1.2), 255)
    b = min(int(b * 1.2), 255)
    return f"#{r:02x}{g:02x}{b:02x}"

class WaybarController:
    def __init__(self, waybar_path, dominant_color):
        self.waybar_path = waybar_path
        self.dominant_color = rgb_to_hex(dominant_color)

    def apply_waybar_config(self):
        with open(self.waybar_path, 'r', encoding='utf-8') as file:
            config_data = file.read()

        pattern_music = r'(#mpris\s*{[^}]*color:\s*)#[0-9A-Fa-f]{6}'
        config_data = re.sub(pattern_music, r'\1' + self.dominant_color, config_data)

        pattern_workspaces = r'(#workspaces\s*button\s*{[^}]*color:\s*)#[0-9A-Fa-f]{6}'
        config_data = re.sub(pattern_workspaces, r'\1' + self.dominant_color, config_data)

        pattern_workspaces_active = r'(#workspaces\s*button\.active\s*{[^}]*color:\s*)#[0-9A-Fa-f]{6}'
        config_data = re.sub(pattern_workspaces_active, r'\1' + self.dominant_color, config_data)       

        pattern_clock = r'(#clock\s*{[^}]*color:\s*)#[0-9A-Fa-f]{6}'
        config_data = re.sub(pattern_clock, r'\1' + self.dominant_color, config_data)

        pattern_current_window = r'(#window\s*{[^}]*color:\s*)#[0-9A-Fa-f]{6}'
        config_data = re.sub(pattern_current_window, r'\1' + self.dominant_color, config_data)

        pattern_network = r'(#network\s*{[^}]*color:\s*)#[0-9A-Fa-f]{6}'
        config_data = re.sub(pattern_network, r'\1' + self.dominant_color, config_data)

        with open(self.waybar_path, 'w', encoding='utf-8') as file:
            file.write(config_data)

        # subprocess.run('pkill waybar', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        # subprocess.run('hyprctl dispatch exec waybar', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)



if __name__ == "__main__":
    cntrl = WaybarController("/home/wzqrxzd/.config/waybar/style.css", get_dominant_color("/home/wzqrxzd/Wallpapers/walp2.jpg"))
    cntrl.apply_waybar_config()

