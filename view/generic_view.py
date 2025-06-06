import getpass
from view.unwanted_view import UnwantedView
from view.display_obj_view import DisplayView
from settings.settings import MANAGEMENT, SUPPORT, SALES


class View(UnwantedView, DisplayView):
    """
    Generic view use as the user is unknown then as parent of role views classes.
    """

    @classmethod
    def create_first_user_warning(cls) -> None:
        print("Aucun utilisateur n'existe actuellement dans la base de données.")
        print("Le premier utilisateur doit nécessairement appartenir au département de management.")

    @staticmethod
    def connection() -> tuple[str, str]:
        print("Pour vous connecter, veuillez renseigner votre nom d'utilisateur:")
        username = input("")
        username = username.strip()
        password_message: str = "Nous avons également besoin de votre mot de passe:"
        password = getpass.getpass(prompt=password_message, stream=None)
        password = password

        return username, password

    @staticmethod
    def what_to_do() -> str:
        return "Que souhaitez-vous faire ?"

    @classmethod
    def yes_or_no_choice(cls) -> bool:
        cls.print_choices(["oui", "non"])
        choice = input("").strip()

        return choice == "1" or choice.lower() == "oui"

    @staticmethod
    def create_with_success(obj: str = "") -> None:
        print(f"Création {obj} terminée !\n")

    @staticmethod
    def remember_me() -> bool:
        print("Se souvenir de vous ?")
        return View.yes_or_no_choice()

    @staticmethod
    def is_that_you(username: str) -> bool:
        print(f"Êtes-vous bien {username} ?")
        return View.yes_or_no_choice()

    @staticmethod
    def hello_prompt(username: str) -> None:
        print(f"Bonjour {username} !\n")

    @classmethod
    def quit_option_print(cls) -> None:
        print("   Q) pour quitter")

    @staticmethod
    def brackets_quit_str() -> str:
        return "('Q' pour quitter)"

    @classmethod
    def quit_print(cls, message: str) -> None:
        print(f"{message} {cls.brackets_quit_str()}")

    @staticmethod
    def category_question() -> str:
        return "Quelle catégorie souhaitez-vous consulter ? "

    @staticmethod
    def valid_choices(max_range: int) -> list:
        quit_choices: list = ["q", "Q"]
        valid_choices_list = [str(i) for i in range(1, max_range + 1)]

        return valid_choices_list + quit_choices

    @staticmethod
    def print_choices(choices_list: list) -> None:
        [print(f"   {index + 1}) {choices_list[index]}") for index in range(0, len(choices_list))]

    @classmethod
    def is_choice_valid(cls, choice: str, max_range: int) -> bool:
        return any(choice == valid for valid in cls.valid_choices(max_range))

    @classmethod
    def choice_loop(cls, question: str, choices_list: list) -> str:
        """
        While loop displaying the question and the choices as long as the user doesn't do a valid choice.
        :param question: question to display
        :param choices_list: choices to display
        :return: choice of the user
        """
        check_answer: bool = False
        choice = ""

        while not check_answer:
            print(question)
            cls.print_choices(choices_list)
            cls.quit_option_print()

            choice: str = input("")
            choice = choice.strip()

            if cls.is_choice_valid(choice, len(choices_list)):
                check_answer = True
            else:
                cls.unknown_option()

        return choice

    @classmethod
    def asks_password_template(cls, prompt: str) -> str:
        password_message = f"{prompt} {cls.brackets_quit_str()} :\n"
        return getpass.getpass(prompt=password_message, stream=None)

    @classmethod
    def asks_actual_password(cls) -> str:
        return cls.asks_password_template("Veuillez indiquer votre mot de passe")

    @classmethod
    def asks_collab_password(cls) -> str:
        return cls.asks_password_template("Définissez son mot de passe:")

    @staticmethod
    def asks_username(complete: str = "") -> str:
        question = f'Nom du collaborateur {complete}:'
        return View.no_blank_answer(question)

    @classmethod
    def asks_contract_name(cls, complete: str = "") -> str:
        cls.quit_print(f"Quel est le nom du contrat {complete} ?")
        return input("").strip()

    @staticmethod
    def asks_contract_new_name(contract_name: str) -> str:
        print(f"Quel nouveau nom souhaitez-vous donner au contrat {contract_name}?")
        return input("").strip()

    @classmethod
    def check_price_validity(cls, price: str) -> float:
        try:
            split_price = price.split(",")
            price = '.'.join(split_price)
            float_price: float = float(price)
            assert float_price >= 0.00
            return float_price
        except Exception:
            print("Erreur dans le montant.")
            return cls.error_price()

    @classmethod
    def update_contract_remain(cls, remain: float) -> float:
        if remain <= 0.00:
            print("Le contrat a déjà été payé en totalité.")
            return 0.00

        while True:
            print(f"D'après le contrat, {remain}€ n'ont pas encore été payées.\nCombien reste-t-il désormais à payer ?")
            new_price: str = input("").strip()
            new_float_price: float = cls.check_price_validity(new_price)
            if remain >= new_float_price > cls.error_price():
                return new_float_price

    @classmethod
    def signed_contract_prompt(cls):
        print("Confirmez-vous que le contrat est signé ?")
        return cls.yes_or_no_choice()

    @classmethod
    def asks_customer_mail(cls) -> str:
        cls.quit_print("Veuillez renseigner l'adresse email du client")
        return input("").strip()

    @classmethod
    def wants_to_change_password(cls) -> bool:
        print("Voulez-vous changer votre mot de passe ?")
        return cls.yes_or_no_choice()

    @staticmethod
    def password_updated() -> None:
        print("Mot de passe mis à jour")

    @classmethod
    def reset_collab_password(cls, username: str) -> bool:
        print(f"Voulez-vous changer le mot de passe de {username} ?")
        return cls.yes_or_no_choice()

    @staticmethod
    def roles_enum(choice: str) -> str:
        match choice:
            case "1":
                return MANAGEMENT
            case "2":
                return SUPPORT
            case "3":
                return SALES
            case _:
                return "q"

    @classmethod
    def no_blank_answer(cls, question: str) -> str:
        response: str = ""
        while response.strip() == "":
            cls.quit_print(question)
            response = input("")

        return response

    @staticmethod
    def modification_done():
        print("Modification effectuée !\n")

    @classmethod
    def asks_event_name(cls) -> str:
        cls.quit_print("Comment se nomme l'événement ?")
        return input("")

    @classmethod
    def asks_number_of_participants(cls) -> int | str:
        choice: str = ""

        while not choice.isdigit():
            cls.quit_print("Combien de personnes participeront-elles à l'événement ?")
            choice = input("").strip()
            if choice.strip().lower() == "q":
                return choice

        return int(choice)

    @classmethod
    def contract_modification_prompt(cls, role: str, is_already_signed: bool):
        choices: list = ["Modifier le nom du contrat", "Mettre à jour le montant payé", ]

        if not is_already_signed:
            choices.append("Valider la signature du contrat")
        if role == MANAGEMENT:
            choices.append("Modifier le commercial")

        return cls.choice_loop(cls.what_to_do(), choices)

    @classmethod
    def asks_event_date(cls, is_starting=True) -> tuple[str, str]:
        context: str = "débutera" if is_starting else "terminera"

        cls.quit_print(f"Quel jour {context} l'évenément ? -- au format JJ/MM/YYYY")
        date_info: str = input("").strip()

        cls.quit_print("À quelle heure ? -- au format 18h30  ")
        hour_info: str = input("").strip()

        return date_info, hour_info

    @classmethod
    def info_menu(cls) -> str:
        choices_list = ["Ajouter des informations", "Modifier les informations", "Supprimer les informations"]

        return cls.choice_loop(cls.what_to_do(), choices_list)

    @staticmethod
    def add_info_prompt() -> str:
        print("Ecrivez les informations à ajouter :")
        return input("")

    @staticmethod
    def same_collaborator_prompt() -> None:
        print("Vous avez choisi de réattribuer le contrat au même collaborateur.")
