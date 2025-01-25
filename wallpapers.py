import random
import subprocess
import os
import re

def count_wallpapers(wallpapers_path):
    last_walpaper_index = 0
    for filename in os.listdir(wallpapers_path):
        if re.search(r'\d', filename):
            last_walpaper_index += 1
    return last_walpaper_index

def chose_random_wallpaper(last_walp):
    random_number = random.randint(1, last_walp)
    return f"walp{random_number}"

class WallpaperController:
    def __init__(self, hyprpaper_path, wallpapers_path, wallpaper):
        self.hyprpaper_path = hyprpaper_path

        if (wallpaper != '-1'):
            self.current_wallpaper_name = f'{wallpaper}'
        else:
            last_walp = count_wallpapers(wallpapers_path)
            self.current_wallpaper_name = chose_random_wallpaper(last_walp)

        self.current_wallpaper_path = wallpapers_path + '/' + self.current_wallpaper_name

        if os.path.isfile(self.current_wallpaper_path + '.png'):
            self.current_wallpaper_path += '.png'
        if os.path.isfile(self.current_wallpaper_path + '.jpg'):
            self.current_wallpaper_path += '.jpg'

    def apply_wallpaper(self):
        with open(self.hyprpaper_path, 'r') as file:
            config_data = file.read()

        config_data = re.sub(r'preload = .+', f'preload = {self.current_wallpaper_path}', config_data)
        config_data = re.sub(r'wallpaper = .+', f'wallpaper = eDP-1,{self.current_wallpaper_path}', config_data)

        with open(self.hyprpaper_path, 'w') as file:
            file.write(config_data)

        subprocess.run('pkill hyprpaper', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run('hyprpaper &', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

if __name__ == "__main__":
    cntrl = WallpaperController('/home/wzqrxzd/Wallpapers', '-1') 
    cntrl.apply_wallpaper()
