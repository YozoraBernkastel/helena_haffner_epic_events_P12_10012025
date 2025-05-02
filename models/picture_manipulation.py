from os import path
from PIL import Image


class PictureManipulation:
    def __init__(self):
        self.picture_1_path: str = "pictures/wallpaper_1.png"
        self.picture_2_path: str = "pictures/wallpaper_2.png"
        self.picture_3_path: str = "pictures/wallpaper_3.png"
        self.shift_num: int = 7

    @staticmethod
    def import_picture(picture_path: str):
        if path.exists(picture_path):
            return Image.open(picture_path, "r")

        print("Impossible de sauvegarder le token")
        return None

    def are_all_pictures_exists(self) -> bool:
        def exists(pic_path):
            return path.exists(pic_path)

        return exists(self.picture_1_path) and exists(self.picture_2_path) and exists(self.picture_3_path)