from getpass import getpass
from settings.settings import MANAGEMENT, SUPPORT, SALES
from models.db_models import Event


class View:
    @staticmethod
    def connection() -> tuple[str, str]:
        print("Pour vous connecter, veuillez renseigner votre nom d'utilisateur:")
        username = input("")
        username = username.strip()
        password_message: str = "Nous avons également besoin de votre mot de passe:"
        password = getpass(prompt=password_message, stream=None)
        password = password

        return username, password

    @staticmethod
    def what_to_do() -> str:
        return "Que souhaitez-vous faire ?"

    @staticmethod
    def unknown_user_or_password() -> None:
        print("Utilisateur ou mot de passe inconnu.")

    @staticmethod
    def unknown_customer() -> None:
        print("Ce client est n'existe pas.")

    @staticmethod
    def bad_password() -> None:
        print("Vous avez donné un mauvais mot de passe.")

    @classmethod
    def yes_or_no_choice(cls) -> bool:
        cls.print_choices(["oui", "non"])
        choice = input("").strip()

        if choice == "1" or choice.lower() == "oui":
            return True

        return False

    @staticmethod
    def remember_me() -> bool:
        print("Se souvenir de vous ?")
        return View.yes_or_no_choice()

    @staticmethod
    def is_that_you(username: str) -> bool:
        print(f"Êtes-vous bien {username} ?")
        return View.yes_or_no_choice()

    @staticmethod
    def already_used_prompt(category: str, data: str, is_feminine: bool = False) -> None:
        feminine: str = "e" if is_feminine else ""
        print(f'{category} {data} est déjà utlisé{feminine}, veuillez en choisir un{feminine} autre, svp.')

    @classmethod
    def username_already_used(cls, username: str) -> None:
        cls.already_used_prompt("Le nom d'utilisateur", username)

    @classmethod
    def mail_already_used(cls, mail: str) -> None:
        cls.already_used_prompt("L'adresse mail", mail, True)

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
    def unknown_option() -> None:
        print(
            "\nCette option n'existe malheureusement pas,"
            " veuillez sélectionner une commande valide parmi la liste\n")

    @staticmethod
    def print_choices(choices_list: list) -> None:
        [print(f"   {index + 1}) {choices_list[index]}") for index in range(0, len(choices_list))]

    @classmethod
    def is_choice_valid(cls, choice: str, max_range: int) -> bool:
        return any(choice == valid for valid in cls.valid_choices(max_range))

    @classmethod
    def choice_loop(cls, question: str, choices_list: list) -> str:
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
        return getpass(prompt=password_message, stream=None)

    @classmethod
    def asks_actual_password(cls) -> str:
        return cls.asks_password_template("Veuillez indiquer votre mot de passe")

    @staticmethod
    def asks_username(complete: str = "") -> str:
        question = f'Nom du collaborateur {complete}:'
        return View.no_blank_answer(question)

    @staticmethod
    def asks_contract_name():
        print("Quel est le nom du contrat ?")
        return input("").strip()

    @staticmethod
    def missing_collaborator(username: str) -> None:
        print(f"Le collaborateur {username} n'est pas présent dans la base de données")

    @staticmethod
    def different_passwords_prompt() -> None:
        print("Vous avez donné deux mots de passe différents")

    @staticmethod
    def modification_canceled() -> None:
        print("Annulation de la demande de modification\n")

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

    @staticmethod
    def unknown_sales_collaborator(collab_name: str) -> None:
        print(f"Le collaborateur {collab_name} n'existe pas ou n'appartient pas au département commercial.")

    @classmethod
    def asks_event_name(cls) -> str:
        cls.quit_print("Comment se nomme l'événement ?")
        return input("")

    @staticmethod
    def event_display(event: Event) -> None:
        print(f"\n   Nom :{event.name}")
        print(f"   Nom du client : {event.customer.full_name}")
        print(f"   Contrat : {event.contract.name}")
        print(f"   Début : {event.starting_time}")
        print(f"   Fin : {event.ending_time}")
        print(f"   Adresse : {event.address}")
        print(f"   Nombre de participants : {event.attendant_number}")
        print(f"   Technicient : {event.support}")
        print(f"   Commentaires : {event.comment}\n")

    @classmethod
    def asks_event_date(cls, is_starting=True) -> tuple[str, str]:
        context: str = "débutera" if is_starting else "terminera"

        cls.quit_print(f"Quel jour {context} l'évenément ? -- au format JJ/MM/YYYY")
        date_info: str = input("").strip()

        cls.quit_print("À quelle heure ? -- au format 18h30  ")
        hour_info: str = input("").strip()

        return date_info, hour_info


