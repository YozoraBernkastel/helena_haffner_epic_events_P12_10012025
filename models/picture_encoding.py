from PIL import ImageFile, Image
from models.picture_manipulation import PictureManipulation
from settings.settings import MAX_ASCII_NUM, DATA_FORMAT, DATA_INFO_BINARY_FORMAT, DOT


class PictureEncoding(PictureManipulation):
    def __init__(self):
        super().__init__()
        self.pictures_list: list = [self.picture_1_path, self.picture_2_path, self.picture_3_path]
        self.ascii_length = len(str(MAX_ASCII_NUM << self.shift_num))

    @staticmethod
    def mod_pix(picture_data: list[list[tuple]], data: list[list[str]]):
        """
        :param picture_data: the data of a picture
        :param data: a list of lists containing three digits converted in strings
        :return: Yield modified pixels.
        """

        # three_num var correspond to a list of three digits and pixel var to the three value of a pixel.
        # The digits inside three_num var can only be 0 or 1 since its binary code.
        for three_num, pixel in zip(data, picture_data):
            # Since a pixel is a tuple, we need to get its values into a list as we want to modify them.
            pix: list = [p for p in pixel]

            # Compare each digit of three_num var with the pixel's values.
            for i in range(len(pix)):
                # if the digit is a 0 and the pixel's value is odd, subtract 1 to have an even number.
                if three_num[i] == "0" and pix[i] % 2 != 0:
                    pix[i] -= 1
                # else if the figit is a 1 and the pixel's value is even ...
                elif three_num[i] == "1" and pix[i] % 2 == 0:
                    # if the pixel's value is not a 0, subtract 1 to this value,
                    # else add 1 instead since we don't want to have a negative number.
                    if pix[i] != 0:
                        pix[i] -= 1
                    else:
                        pix[i] += 1

            yield tuple(pix)

    @staticmethod
    def compute_data_info(data: list) -> list:
        """
        Get the length og the data, then transform this number into a twelve size binary and, finally,
        split the binary number into a list of lists. Each sub list will contain three separate digit.
        :param data: a list containing the binary form of a part of the token
        :return: A list of lists containing each digit of the data length converted into binary code.
        """
        binary_len: str = DATA_INFO_BINARY_FORMAT.format(len(data))

        return [[binary_len[i], binary_len[i + 1], binary_len[i + 2]] for i in
                range(0, len(binary_len), 3)]

    def encoded_img(self, picture: ImageFile, data: list):
        """
        :param picture: The data of the picture
        :param data: a list of lists containing the token in binary
        :return: The picture containing the binary sequence
        """

        # convert the data length into a list containing the info into binary code, then fusion this list with the data
        # since we want the length info at the beginning.
        data_info: list = self.compute_data_info(data)
        data_info.extend(data)

        width = picture.size[0]
        # variables used to track where we are in the picture
        x, y = 0, 0

        # Browse the picture and replace its pixels with the modified values' pixels.
        for pix in self.mod_pix(picture.getdata(), data_info):
            # identify the pixel we want to modify then put the modified version in its place.
            picture.putpixel((x, y), pix)
            if x == width - 1:
                x = 0
                y += 1
            else:
                x += 1

        return picture

    def rework_picture(self, picture_path: str, data: list[list[str]]) -> None:
        """
        :param picture_path:
        :param data: token part in form of binary sequences split into lists
        :return: None
        """
        picture: Image = self.import_picture(picture_path)

        if picture is not None:
            # create a copy of the copied picture in the memory.
            encoded_picture = picture.copy()
            # encode the binary shaped token int the copy.
            encoded_picture = self.encoded_img(encoded_picture, data)

            # give a name to the copy of the picture using the name of the original picture with an underscore then save the copy
            file_name, ext = picture_path.split(DOT)
            new_image_name = f"{file_name}_.{ext}"
            encoded_picture.save(new_image_name, quality=100, subsampling=0, optimize=False)

    def picture_token_link(self, binary_token: list) -> None:
        [self.rework_picture(picture, token_part) for picture, token_part in zip(self.pictures_list, binary_token)]

    @staticmethod
    def list_of_binary(shifted_token: list[str]) -> list[list[str]]:
        """
        Convert a list of number into a list containing multiple lists of three digits in string format.
        The lists work two per two and their digits form a six size binary.
        :param shifted_token: A list of strings which contains numbers.
        :return: A list of multiple lists composed of digits.
        """
        binary_token: list = []

        for number in shifted_token:
            for digit in number:
                # each digit is convert into a six bit binary
                byte_str = DATA_FORMAT.format(ord(digit))

                # then split the six bit binary into two lists of three digit which be placed at the end of a list of list.
                for i in range(0, len(byte_str), 3):
                    binary_token.append([byte_str[i], byte_str[i + 1], byte_str[i + 2]])

        return binary_token

    def shift(self, digit: int) -> str:
        """
        :param digit: a number
        :return: shifted digit param as a string with a predetermined length
        """
        shifted = str(digit << self.shift_num)

        for add_zero in range(0, self.ascii_length - len(shifted)):
            shifted = f"0{shifted}"

        return shifted

    def convert_token_part(self, token_part: str) -> list[list[str]]:
        """
        Transform each character of the token in its ascii counterpart -- which will be a number -- then shift its bytes
        to get a new number which will be transformed in binary.
        :param token_part: a part of the JWT Token
        :return: The part of the JWT Token given as argument but transformed in binary code
        """
        ascii_token: list[int] = [ord(character) for character in token_part]
        shifted_token: list[str] = [self.shift(digit) for digit in ascii_token]

        return self.list_of_binary(shifted_token)

    def crypt_token(self, token: str) -> None:
        if not token:
            return

        split_token: list[str] = token.split(DOT)
        binary_token: list = [self.convert_token_part(token_part) for token_part in split_token]

        self.picture_token_link(binary_token)
