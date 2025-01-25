import re
import os

def rgb_to_hex(color):
    r, g, b = color
    r = min(int(r * 1.2), 255)
    g = min(int(g * 1.2), 255)
    b = min(int(b * 1.2), 255)
    return f"#{r:02x}{g:02x}{b:02x}"

class WofiController:
    def __init__(self, wofi_path, dominant_color):
        self.wofi_path = wofi_path
        self.dominant_color = rgb_to_hex(dominant_color)

    def apply_wofi_config(self):
        with open(self.wofi_path, 'r', encoding='utf-8') as file:
            config_data = file.read()



        pattern_selected = r'(#entry:selected\s*\{\s*background-color:\s*)#[0-9A-Fa-f]{6}'
        config_data = re.sub(pattern_selected, r'\1' + self.dominant_color, config_data)

        with open(self.wofi_path, 'w', encoding='utf-8') as file:
            file.write(config_data)
