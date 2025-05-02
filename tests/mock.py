from datetime import datetime
from settings.settings import MANAGEMENT, SUPPORT, SALES


def mock_get_pass(*args, **kwargs):
    return MANAGEMENT_1["password"]

q: str = "q"
question: str = "Est-ce une question ?"

UNKNOWN_USERNAME: str = "unknown username"
UNKNOWN_MAIL: str = "unknown@mail"
UNKNOWN_CONTRACT_NAME: str = "unkown contract"
UNKNOWN_EVENT_NAME: str = "unkown event"

MANAGEMENT_1: dict = {"username": "management1", "password": "management1", "role": MANAGEMENT}
SUPPORT_1: dict = {"username": "support1", "password": "support1", "role": SUPPORT}
SALES_1 = {"username": "sales1", "password": "sales", "role": SALES}
TO_CREATE_COLLAB: dict = {"username": "new user", "password": "newuser", "role": MANAGEMENT}

TO_CHANGE_COLLAB: dict = {"username": "changelin", "password": "changelin", "role": SUPPORT}

CUSTOMER_1: dict = {"fullname": "Kust Homer", "mail": "kusthomer@mail.com", "phone": "0102030405",
                    "company_name": "Entre deux prises", "information": "Aime les pâtes et le jambon "}
CUSTOMER_1_NEW_NAME: str = "Kurt Amer"

CUSTOMER_2: dict = {"fullname": "Kurt Omer", "mail": "kurtomer@mail.com", "phone": "0102030405",
                    "company_name": "Entre deux prises", "information": "Aime le riz et le chocolat "}

NEW_PHONE: str = "1020304050"
NEW_COMPANY: str = "nouvelle entreprise"


TO_CREATE_CUSTOMER: dict = {"mail": "Csion@mail.com", "fullname": "Crea Sion", "company_name": "Entre trous prises",
                            "phone": "0102030405", "information": "est un nouveau client "}

CONTRACT_1: dict = {"name": "contrat1", "total": 41.25}

START_1: datetime = datetime(2025, 9, 21, 7, 42)
END_1: datetime = datetime(2025, 9, 22, 17, 41)
ATTENDANT_NUMBER: int = 117
EVENT_1: dict = {"name": "event1", "address": "27 rue du test ambulant 67452 TESTHEIM", "start": START_1, "end": END_1,
                 "attendant": ATTENDANT_NUMBER, "information": "informations pertinentes pour le test"}