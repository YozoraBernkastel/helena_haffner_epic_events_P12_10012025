from os import path
from PIL import Image
from settings.settings import MAX_ASCII_NUM, SHIFTER


class PictureManipulation:
    """
    Virtual class given as parent to the encoding and decoding classes.
    """

    def __init__(self):
        self.picture_1_path: str = "pictures/wallpaper_1.png"
        self.picture_2_path: str = "pictures/wallpaper_2.png"
        self.picture_3_path: str = "pictures/wallpaper_3.png"
        self.shift_num: int = SHIFTER
        self.ascii_length = len(str(MAX_ASCII_NUM << self.shift_num))

    @staticmethod
    def import_picture(picture_path: str):
        """
        Inport an existing picture.
        :param picture_path: picture's path.
        :return: the picture
        """
        if path.exists(picture_path):
            return Image.open(picture_path, "r")

        print("Impossible de sauvegarder le token")
        return None

    def are_all_pictures_exists(self) -> bool:
        """
        Check if all the needed pictures exist.
        :return:
        """

        def exists(pic_path):
            return path.exists(pic_path)

        return exists(self.picture_1_path) and exists(self.picture_2_path) and exists(self.picture_3_path)
