from models.picture_encoding import PictureEncoding
from models.picture_decoding import PictureDecoding
from Helper.jwt_helper import JwtHelper


def test_token_transformation():
    user_id = 1
    token = JwtHelper.generate_jwt(user_id=user_id)

    encoder = PictureEncoding()
    encoder.crypt_token(token)

    decoder: PictureDecoding = PictureDecoding()
    decoded_token = decoder.token_getter()

    assert token == decoded_token
