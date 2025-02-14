from PIL import Image, ImageFile
from os import path


class PictureDecoding:
    def __init__(self):
        self.picture_1_path: str = "pictures/wallpaper_1_.jpeg"
        self.picture_2_path: str = "pictures/wallpaper_2_.jpeg"
        self.picture_3_path: str = "pictures/wallpaper_3_.jpeg"
        self.pictures_list: list = [self.picture_1_path, self.picture_2_path, self.picture_3_path]

    def get_binary_code(self, picture_path: str) -> str:
        pass

    def token_decoder(self) -> str:
        binary_token_parts: list = [self.get_binary_code(picture_path) for picture_path in self.pictures_list]

        token_parts_list: list = []

        return ".".join(token_parts_list)

    def are_all_pictures_exists(self) -> bool:
        def exists(pathe):
            return path.exists(pathe)

        return exists(self.picture_1_path) and exists(self.picture_2_path) and exists(self.picture_3_path)
        # return all([path.exists(picture) for picture in self.pictures_list])

    def token_getter(self) -> str:
        if not self.are_all_pictures_exists():
            return ""

        return self.token_decoder()
