MAX_ASCII_NUM: int = 127
BINARY_LENGTH: int = 6
DATA_FORMAT: str = '{0:0' + str(BINARY_LENGTH) + 'b}'
DATA_INFO_BINARY_LENGTH: int = 12
DATA_INFO_BINARY_FORMAT: str = '{0:0' + str(DATA_INFO_BINARY_LENGTH) + 'b}'
DATA_INFO_LEN: int = int(DATA_INFO_BINARY_LENGTH / 3)
DOT: str = "."
SHIFTER = 7

MANAGEMENT: str = "gestion"
SUPPORT: str = "support"
SALES: str = "commercial"
ROLES_LIST: list[str] = [MANAGEMENT, SUPPORT, SALES]
