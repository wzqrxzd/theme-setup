from wallpapers import WallpaperController
from hyprland import HyprlandController
from waybar import WaybarController
from colorthief import ColorThief

import os
import re
import tomllib

def get_color_palette(image_path, color_count=5):
    color_thief = ColorThief(image_path)
    color_palette = color_thief.get_palette(color_count=color_count, quality=1)
    return color_palette

def print_color_preview(color):
    # Функция для отображения цвета в консоли.
    r, g, b = color
    print(f"\033[48;2;{r};{g};{b}m   {r},{g},{b} \033[0m")

def choose_color_from_palette(color_palette):
    print("Available Colors: ")
    for idx, color in enumerate(color_palette):
        print(f"{idx}: ", end="")
        print_color_preview(color)
    
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

def display_image_preview(image_path):
    # Использование команды kitty для предпросмотра изображения
    print("Displaying image preview...")
    os.system(f"kitty +kitten icat {image_path}")

def choose_image_from_directory(directory_path):
    while True:
        print("Available Images: ")
        # Сортировка изображений по числовой части имени файла
        images = sorted(
            [f for f in os.listdir(directory_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))],
            key=lambda x: int(re.search(r'(\d+)', x).group())  # Извлечение числовой части имени
        )

        # Выводим изображения с индексами
        for idx, image in enumerate(images):
            print(f"{idx}: {image}")
        print(f"{len(images)}: Cancel")        

        try:
            choice = int(input(f"Choose an image by index (0-{len(images) - 1}, {len(images)} to cancel): "))
            if 0 <= choice < len(images):
                selected_image = os.path.join(directory_path, images[choice])
                display_image_preview(selected_image)
                
                confirm = input("Do you want to use this image? (y/n): ").strip().lower()
                if confirm == 'y':
                    return images[choice].split('.')[0]
                elif confirm == 'n':
                    continue
                else:
                    print("Invalid input, try again.")
            elif choice == len(images):
                exit()
            else:
                print("Invalid index. Try again.")
        except ValueError:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
    wallpapers_path = data["paths"]["wallpapers_path"]
    hyprland_path = data["paths"]["hyprland_path"] 
    hyprpaper_path = data["paths"]["hyprpaper_path"] 
    waybar_path = data["paths"]["waybar_path"] 

    wallpaper = choose_image_from_directory(wallpapers_path)

    wallpaper_cntrl = WallpaperController(hyprpaper_path, wallpapers_path, wallpaper)
    wallpaper_cntrl.apply_wallpaper()

    color_palette = get_color_palette(wallpaper_cntrl.current_wallpaper_path)
    selected_color = choose_color_from_palette(color_palette)

    hyprland_cntrl = HyprlandController(hyprland_path, selected_color)
    hyprland_cntrl.apply_hyprland_config()

    waybar_cntrl = WaybarController(waybar_path, selected_color)
    waybar_cntrl.apply_waybar_config()
