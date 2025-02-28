from PIL import Image
from models.picture_manipulation import PictureManipulation
from settings.settings import DATA_INFO_LEN, DOT

# todo COMMENTER LE CODE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class PictureDecoding(PictureManipulation):
    def __init__(self):
        super().__init__()
        self.picture_1_path: str = "pictures/wallpaper_1_.png"
        self.picture_2_path: str = "pictures/wallpaper_2_.png"
        self.picture_3_path: str = "pictures/wallpaper_3_.png"
        self.pictures_list: list = [self.picture_1_path, self.picture_2_path, self.picture_3_path]

    @staticmethod
    def convert_binary_to_int(binary_list: list) -> int:
        temp_list: list = []

        for element in binary_list:
            for n in element:
                temp_list.append(str(n % 2))
        temp: str = "".join(temp_list)

        return int(temp, 2)

    def get_binary_string(self, data) -> int:
        data_len: list = [data[pixel] for pixel in range(0, DATA_INFO_LEN)]

        return self.convert_binary_to_int(data_len)

    def decoded_data(self, data_len: int, data) -> str:
        token_part: str = ""

        for i in range(DATA_INFO_LEN, data_len + DATA_INFO_LEN, 10):
            temp_list = [data[j] for j in range(i, i + 10)]

            temp_str: str = ""
            for y in range(0, len(temp_list), 2):
                ascii_number: int = self.convert_binary_to_int([temp_list[y], temp_list[y + 1]])
                temp_str = f"{temp_str}{chr(ascii_number)}"

            token_part = f"{token_part}{chr(int(temp_str) >> self.shift_num)}"

        return token_part

    def get_decoded_token_parts(self, picture_path: str) -> str:
        picture: Image = self.import_picture(picture_path)
        data_len: int = self.get_binary_string(picture.getdata())

        return self.decoded_data(data_len, picture.getdata())

    def token_decoder(self) -> str:
        token_parts: list = [self.get_decoded_token_parts(picture_path) for picture_path in self.pictures_list]

        return DOT.join(token_parts)

    def token_getter(self) -> str:
        if not self.are_all_pictures_exists():
            return ""

        return self.token_decoder()
