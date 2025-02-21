from PIL import ImageFile, Image
from models.picture_manipulation import PictureManipulation


class PictureEncoding(PictureManipulation):
    def __init__(self):
        super().__init__()
        self.pictures_list: list = [self.picture_1_path, self.picture_2_path, self.picture_3_path]

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
    def compute_data_info(data: list) -> list:
        binary_len: str = '{0:012b}'.format(len(data))

        return [[binary_len[i], binary_len[i + 1], binary_len[i + 2]] for i in
                range(0, len(binary_len), 3)]

    def encoded_img(self, picture: ImageFile, data: list):
        width = picture.size[0]
        x, y = 0, 0

        data_info: list = self.compute_data_info(data)
        data_info.extend(data)

        for pix in self.mod_pix(picture.getdata(), data_info):
            picture.putpixel((x, y), pix)
            if x == width - 1:
                x = 0
                y += 1
            else:
                x += 1

        return picture

    def rework_picture(self, picture_path: str, data: list) -> None:
        picture: Image = self.import_picture(picture_path)

        if picture is not None:
            encoded_picture = picture.copy()
            encoded_picture = self.encoded_img(encoded_picture, data)

            file_name, ext = picture_path.split(".")
            new_image_name = f"{file_name}_.{ext}"
            encoded_picture.save(new_image_name, quality=100, subsampling=0, optimize=False)

    def picture_token_link(self, binary_token: list) -> None:
        [self.rework_picture(picture, token_part) for picture, token_part in zip(self.pictures_list, binary_token)]

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

    @staticmethod
    def shift(digit: int) -> str:
        return str(digit << 7)

    def convert_token_part(self, token_part: list) -> list[list[str]]:
        ascii_token: list[int] = [ord(letter) for letter in token_part]
        shifted_token: list[str] = [self.shift(digit) for digit in ascii_token]
        print(shifted_token[0])
        # todo il faut sans doute ajouter la longueur pour décoder shifted token !!!
        return self.list_of_binary(shifted_token)

    def crypt_token(self, token: str) -> None:
        if not token:
            return None

        split_token: list = token.split(".")
        binary_token: list = []

        for token_part in split_token:
            binary_token.append(self.convert_token_part(token_part))

        self.picture_token_link(binary_token)
