from PIL import Image, ImageFile
from os import path


class PictureEncoding:
    def __init__(self):
        self.picture_1_path: str = "pictures/wallpaper_1.jpeg"
        self.picture_2_path: str = "pictures/wallpaper_2.jpeg"
        self.picture_3_path: str = "pictures/wallpaper_3.jpeg"
        self.pictures_list: list = [self.picture_1_path, self.picture_2_path, self.picture_3_path]

    @staticmethod
    def import_picture(picture_path: str):
        if path.exists(picture_path):
            return Image.open(picture_path, "r")

        print("Impossible de sauvegarder le token")
        return None

    @staticmethod
    def mod_pix(picture_data: list, data: list) -> tuple[int]:

        for three_num, pixel in zip(data, picture_data):
            pix: list = [p for p in pixel]
            for i in range(len(pix)):
                if three_num[i] == "0" and pix[i] % 2 != 0:
                    pix[i] -= 1
                elif three_num[i] == "1" and pix[i] % 2 == 0:
                    if pix[i] != 0:
                        pix[i] -= 1
                    else:
                        pix[i] += 1

            yield tuple(pix)

    @staticmethod
    def shift(digit: int) -> str:
        return str(digit << 7)

    @staticmethod
    def to_binary(str_digit: str) -> str:
        return str(format(ord(str_digit), '6b'))

    def compute_data_info(self, data: list) -> list:
        shift_data_len = self.shift(len(data))
        binary_data_len = self.to_binary(shift_data_len)

        into_list: list = [[binary_data_len[i], binary_data_len[i + 1], binary_data_len[i + 2]] for i in
                           range(0, len(binary_data_len), 3)]

        temp = self.shift(len(into_list))
        temp = self.to_binary(temp)
        temp_list: list = [[temp[i], temp[i + 1], temp[i + 2]] for i in
                           range(0, len(temp), 3)]
        # à tester
        temp_list.extend(into_list)

        return temp_list

    def encoded_img(self, picture: ImageFile, data: list) -> None:
        width = picture.size[0]
        x, y = 0, 0

        data_info: list = self.compute_data_info(data)

        for pix in self.mod_pix(picture.getdata(), data):
            picture.putpixel((x, y), pix)
            if x == width - 1:
                x = 0
                y += 1
            else:
                x += 1

    def rework_picture(self, picture_path: str, data: list) -> None:
        picture: ImageFile = self.import_picture(picture_path)

        if picture is not None:
            encoded_picture = picture.copy()
            print(f"before {encoded_picture.getdata()[0] =}")
            print(data[0])
            self.encoded_img(encoded_picture, data)
            print(f"before {encoded_picture.getdata()[0] =}")
            print()

            file_name, ext = picture_path.split(".")
            new_image_name = f"{file_name}_.{ext}"
            encoded_picture.save(new_image_name)

    def picture_token_link(self, binary_token: list) -> None:
        [self.rework_picture(picture, token) for picture, token in zip(self.pictures_list, binary_token)]

    @staticmethod
    def list_of_binary(shifted_token: list[str]) -> list[list[str]]:
        binary_token = []

        for element in shifted_token:
            for digit in element:
                byte_str = str(format(ord(digit), '6b'))
                into_list: list = [[byte_str[i], byte_str[i + 1], byte_str[i + 2]] for i in
                                   range(0, len(byte_str), 3)]

                for d in into_list:
                    binary_token.append(d)

        return binary_token

    def convert_token_part(self, token_part: list) -> list[list[str]]:
        ascii_token: list[int] = [ord(letter) for letter in token_part]
        shifted_token: list[str] = [self.shift(digit) for digit in ascii_token]
        return self.list_of_binary(shifted_token)

    def crypt_token(self, token: str) -> None:
        if not token:
            return None

        split_token: list = token.split(".")
        binary_token: list = []

        for token_part in split_token:
            binary_token.append(self.convert_token_part(token_part))

        self.picture_token_link(binary_token)
