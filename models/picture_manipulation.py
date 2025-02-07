from PIL import Image, ImageFile
from os import path


class PictureManipulation:
    def __init__(self):
        self.picture = None
        self.picture_1_path: str = ".pictures/wallpaper.jpeg"
        self.picture_2_path: str = ".pictures/wallpaper_2.jpeg"
        self.picture_3_path: str = ".pictures/wallpaper_3.jpeg"
        self.pictures_list: list = [self.picture_1_path, self.picture_2_path, self.picture_3_path]

    def import_picture(self, picture_path: str) -> None:
        if path.exists(picture_path):
            picture = Image.open(picture_path, "r")
            self.picture = iter(picture.getdata())

    @staticmethod
    def mod_pix(picture_data, data):
        pass

    def encoded_img(self, picture: ImageFile, data):
        img_width = picture.size[0]
        (x, y) = (0, 0)

        # for pix in self.mod_pix(picture.getdata(), data):
        #     pass

        # todo au dessus du centre, tu descend d'un cran si besoin, au dessous, tu montes -> permet de ne pas aller sous 0 et au dessus de 255 !!

    def picture_in_bytes(self, data: str) -> bytes | None:
        if self.picture is not None:
            encoded_picture = self.picture.copy()
            self.encoded_img(encoded_picture, data)

    @staticmethod
    def str_to_binary(shifted_token: list[str]) -> str:
        binary_token = []

        for element in shifted_token:
            for digit in element:
                binary_token.append(format(ord(digit), '6b'))

        return "".join(number for number in binary_token)

    def convert_token_part(self, token_part) -> str:
        ascii_token: list[int] = [ord(letter) for letter in token_part]
        shifted_token: list[str] = [str(digit << 7) for digit in ascii_token]
        return self.str_to_binary(shifted_token)

    def crypt_token(self, token: str) -> None:
        if not token:
            return None

        split_token: list = token.split(".")
        binary_token: list = []

        for token_part in split_token:
            binary_token.append(self.convert_token_part(token_part))



        for part in binary_token:
            print(len(part))
            print(part)
            print()




