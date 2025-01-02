from wallpapers import WallpaperController
from hyprland import HyprlandController
from waybar import WaybarController
from colorthief import ColorThief

def get_color_palette(image_path, color_count=5):
    color_thief = ColorThief(image_path)
    # Get a palette of colors (up to 'color_count' colors)
    color_palette = color_thief.get_palette(color_count=color_count, quality=1)
    return color_palette

def print_color_preview(color):
    """Функция для отображения цвета в консоли."""
    r, g, b = color
    # Создаем строку с цветом, используя ANSI escape-коды
    print(f"\033[48;2;{r};{g};{b}m   {r},{g},{b} \033[0m")

def choose_color_from_palette(color_palette):
    print("Available Colors: ")
    for idx, color in enumerate(color_palette):
        print(f"{idx}: ", end="")
        print_color_preview(color)  # Показываем цвет в консоли
    
    try:
        choice = int(input(f"Choose a color by index (0-{len(color_palette) - 1}): "))
        if 0 <= choice < len(color_palette):
            return color_palette[choice]
        else:
            print("Invalid index. Defaulting to the first color.")
            return color_palette[0]
    except ValueError:
        print("Invalid input. Defaulting to the first color.")
        return color_palette[0]

if __name__ == "__main__":
    wallpapers_path = "/home/wzqrxzd/Wallpapers"
    hyprland_path =  "/home/wzqrxzd/.config/hypr/hyprland.conf"
    hyprpaper_path = "/home/wzqrxzd/.config/hypr/hyprpaper.conf"
    waybar_path = "/home/wzqrxzd/.config/waybar/style.css"

    wallpaper_cntrl = WallpaperController(hyprpaper_path, wallpapers_path, '-1')
    wallpaper_cntrl.apply_wallpaper()

    color_palette = get_color_palette(wallpaper_cntrl.current_wallpaper_path)
    selected_color = choose_color_from_palette(color_palette)

    hyprland_cntrl = HyprlandController(hyprland_path, selected_color)
    hyprland_cntrl.apply_hyprland_config()

    waybar_cntrl = WaybarController(waybar_path, selected_color)
    waybar_cntrl.apply_waybar_config()
