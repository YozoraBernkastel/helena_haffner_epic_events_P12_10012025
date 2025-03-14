from getpass import getpass


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
    def unknown_user_or_password() -> None:
        print("Utilisateur ou mot de passe inconnu.")

    @staticmethod
    def bad_password():
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
    def username_already_used(username: str) -> None:
        print(f"Le nom d'utilisateur {username} est déjà utilisé, veuillez en choisir un autre, svp.")

    @staticmethod
    def hello_prompt(username: str) -> None:
        print(f"Bonjour {username} !")

    @classmethod
    def quit_option_print(cls):
        print("   Q) pour quitter")

    @staticmethod
    def brackets_quit_str() -> str:
        return "('Q' pour quitter)"

    @classmethod
    def quit_print(cls, message: str):
        print(f"{message} {cls.brackets_quit_str()}")

    @staticmethod
    def valid_choices(max_range: int) -> list:
        quit_choices: list = ["q", "Q"]
        valid_choices_list = [str(i) for i in range(1, max_range + 1)]

        return valid_choices_list + quit_choices

    @staticmethod
    def unknown_option():
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
    def asks_actual_password(cls):
        return cls.asks_password_template("Entrez votre ancien mot de passe")

    @staticmethod
    def missing_collaborator(username: str) -> None:
        print(f"Le collaborateur {username} n'est pas présent dans la base de données")

    @staticmethod
    def different_passwords_prompt() -> None:
        print("Vous avez donné deux mots de passe différents")

    @staticmethod
    def modification_canceled():
        print("Annulation de la demande de modification\n")

    @classmethod
    def wants_to_change_password(cls) -> bool:
        print("Voulez-vous changer votre mot de passe ?")
        return cls.yes_or_no_choice()

    @staticmethod
    def actual_role(collaborator):
        print(f"{collaborator.username} est actuellement affecté au service de {collaborator.role}")

