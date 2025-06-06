from PIL import Image
from models.picture_manipulation import PictureManipulation
from settings.settings import DATA_INFO_LEN, DOT, BINARY_LENGTH


class PictureDecoding(PictureManipulation):
    """
    Class used to decode the token stored inside the pictures.
    """

    def __init__(self):
        super().__init__()
        self.picture_1_path: str = "pictures/wallpaper_1_.png"
        self.picture_2_path: str = "pictures/wallpaper_2_.png"
        self.picture_3_path: str = "pictures/wallpaper_3_.png"
        self.pictures_list: list = [self.picture_1_path, self.picture_2_path, self.picture_3_path]
        # Division by three since a pixel is composed of three values
        self.one_character_length: int = int(self.ascii_length * BINARY_LENGTH / 3)

    @staticmethod
    def convert_binary_to_int(binary_list: list) -> int:
        temp_list: list = []

        for element in binary_list:
            for n in element:
                # we can just check if the value is even or odd to determinate if it's a 0 or a 1
                temp_list.append(str(n % 2))
        temp: str = "".join(temp_list)

        return int(temp, 2)

    def get_binary_string(self, data: list) -> int:
        """
        Get the data length insert at the beginning of the picture. The length of this binary info correspond to the
        size of the binary used when it was encoded.
        :param data: list containing all data of a picture.
        :return: Length of the binary sequence in int.
        """
        # Grab the pixels containing the data length info
        data_len: list = [data[pixel] for pixel in range(0, DATA_INFO_LEN)]

        # Convert the length from binary to int.
        return self.convert_binary_to_int(data_len)

    def decoded_data(self, data_len: int, data: list) -> str:
        """
        :param data_len: the length of the data needed to reconstitute the token part
        :param data: picture's data
        :return: The Jwt token's part decoded
        """
        token_part: str = ""

        # skip the first pixels corresponding to the data length,
        # then get a number of pixels corresponding to the binary code of one character.
        for i in range(DATA_INFO_LEN, data_len + DATA_INFO_LEN, self.one_character_length):
            temp_list = [data[j] for j in range(i, i + self.one_character_length)]

            temp_str: str = ""
            for y in range(0, len(temp_list), 2):
                # Since a character was convert into a 6 size binary code, we can take the two following pixels to
                # get the character back.
                ascii_number: int = self.convert_binary_to_int([temp_list[y], temp_list[y + 1]])
                temp_str = f"{temp_str}{chr(ascii_number)}"
            # add the character to ones we already have to reconstitute the token part
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
