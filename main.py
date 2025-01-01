from wallpapers import WallpaperController
from hyprland import HyprlandController
from colorthief import ColorThief

def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

if __name__ == "__main__":
    wallpapers_path = "/home/wzqrxzd/Wallpapers"
    hyprland_path =  "/home/wzqrxzd/.config/hypr/hyprland.conf"
    hyprpaper_path = "/home/wzqrxzd/.config/hypr/hyprpaper.conf"

    wallpaper_cntrl = WallpaperController(hyprpaper_path, wallpapers_path, '-1')
    wallpaper_cntrl.apply_wallpaper()

    dominant_color = get_dominant_color(wallpaper_cntrl.current_wallpaper_path)

    hyprland_cntrl = HyprlandController(hyprland_path, dominant_color)
    hyprland_cntrl.apply_hyprland_config()
