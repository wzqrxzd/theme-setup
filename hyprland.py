import re

def generate_color(dominant_color):
    r, g, b = dominant_color

    r_active = min(int(r * 1.2), 255)
    g_active = min(int(g * 1.2), 255)
    b_active = min(int(b * 1.2), 255)

    # r_active = r
    # g_active = g 
    # b_active = b

    active_border = f"rgba({r_active:02x}{g_active:02x}{b_active:02x}{255:02x}) rgba({r_active:02x}{g_active:02x}{b_active:02x}{255:02x}) 45deg"
    
    r_inactive = int(r * 0.8)
    g_inactive = int(g * 0.8)
    b_inactive = int(b * 0.8)

    inactive_border = f"rgba({r_inactive:02x}{g_inactive:02x}{b_inactive:02x}{170:02x})"  # 170 — полупрозрачный

    color = [f"{active_border}", f"{inactive_border}"]
    return color


class HyprlandController:
    def __init__(self, config_path, dominant_color):
        self.config_path = config_path
        self.dominant_color = dominant_color
        self.color_scheme = generate_color(self.dominant_color)

    def apply_hyprland_config(self):
        with open(self.config_path, 'r') as file:
            config_data = file.read()

        config_data = re.sub(r'col.active_border = .+', f'col.active_border = {self.color_scheme[0]}', config_data)
        config_data = re.sub(r'col.inactive_border = .+', f'col.inactive_border = {self.color_scheme[1]}', config_data)

        with open(self.config_path, 'w') as file:
            file.write(config_data)
