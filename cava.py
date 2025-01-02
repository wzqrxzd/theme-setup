import re
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


class CavaController:
    def __init__(self, cava_path, color):
        self.cava_path = cava_path
        self.color = rgb_to_hex(color)

    def apply_cava_config(self):
        with open(self.cava_path, 'r') as file:
            config_data = file.read()

        pattern_foreground = r'(\s*foreground\s*=\s*)\'#[0-9A-Fa-f]{6}\''
        config_data = re.sub(pattern_foreground, r'\1' + '\'' + self.color + '\'', config_data)

        with open(self.cava_path, 'w', encoding='utf-8') as file:
            file.write(config_data)
        
if __name__ == "__main__":
    cntrl = CavaController("/home/wzqrxzd/.config/cava/config", get_dominant_color("/home/wzqrxzd/Wallpapers/walp2.jpg"))
    cntrl.apply_cava_config()

