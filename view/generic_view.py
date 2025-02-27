from getpass import getpass


class View:
    @staticmethod
    def quit_option():
        print("   Q) pour quitter")

    @staticmethod
    def is_quitting(choice: str) -> bool:
        return choice.lower() == "q"

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
    def connection() -> tuple[str, str]:
        print("Pour vous connecter, veuillez renseigner votre nom d'utilisateur:")
        username = input("")
        username = username.strip()
        password_message: str = "Nous avons également besoin de votre mot de passe:"
        password = getpass(prompt=password_message, stream=None)
        password = password

        return username, password

    @staticmethod
    def yes_or_no_choice() -> bool:
        print("  1) oui")
        print("  2) non")
        choice = input("")

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
