from getpass import getpass


class View:
    @staticmethod
    def connection() -> tuple[str, str]:
        print("Bonjour,")
        print("Pour vous connecter, veuillez renseigner votre nom d'utilisateur:")
        username = input("")
        username = username.strip()
        password_message: str = "Nous avons également besoin de votre mot de passe:"
        password = getpass(prompt=password_message, stream=None)
        password = password

        return username, password

    @staticmethod
    def yes_or_no_prompt() -> str:
        print("  1) oui")
        print("  2) non")
        return input("")

    @staticmethod
    def check_yes_or_no_answer(choice) -> bool | None:
        if choice == "1" or choice.lower() == "oui":
            return True
        if choice == "2" or choice.lower() == "non":
            return False

        return None

    @staticmethod
    def invalid_answer_prompt():
        print("Veuillez saisir une réponse valide svp.")

    @staticmethod
    def remember_me() -> bool:
        choice: bool | None = None

        while choice is None:
            print("Se souvenir de vous ?")
            user_answer = View.yes_or_no_prompt()
            choice = View.check_yes_or_no_answer(user_answer)

            if choice is not None:
                return choice

            View.invalid_answer_prompt()
