from PIL import Image
from models.picture_manipulation import PictureManipulation


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
        data_len: list = [data[pixel] for pixel in range(0, 4)]

        return self.convert_binary_to_int(data_len)

    def decoded_data(self, data_len: int, data) -> str:
        digit_list: list = []
        temp_list = []
        blabla = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        print(len(blabla))

        for i in range(4, data_len + 4, 2):
            digit: int = self.convert_binary_to_int([data[i], data[i + 1]])
            if len(temp_list) == 5:
                digit_list.append(temp_list)
                temp_list = []
            temp_list.append(digit)
            # digit_list.append(digit)

        print(len(digit_list))

        return ""


    def get_binary_code(self, picture_path: str) -> str:
        picture: Image = self.import_picture(picture_path)
        data_len: int = self.get_binary_string(picture.getdata())
        decoded_data: str = self.decoded_data(data_len, picture.getdata())

        return ""

    def token_decoder(self) -> str:
        binary_token_parts: list = [self.get_binary_code(picture_path) for picture_path in self.pictures_list]

        token_parts_list: list = []

        return ".".join(token_parts_list)

    def token_getter(self) -> str:
        if not self.are_all_pictures_exists():
            return ""

        return self.token_decoder()
