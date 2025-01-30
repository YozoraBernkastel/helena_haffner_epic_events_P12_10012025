class View:
    @staticmethod
    def connection() -> tuple[str, str]:
        print("Bonjour,")
        print("Pour vous connecter, veuillez renseigner votre nom d'utilisateur:")
        username = input("")
        username = username.strip()
        print("Nous avons également besoin de votre mot de passe:")
        password = input("")
        password = password

        return username, password

    @staticmethod
    def remember_me() -> bool:
        choice: bool | None = None
        while choice is None:
            print("Se souvenir de vous ?")
            print("tapez 1 pour oui")
            print("tapez 2 pour non")
            choice = input("")

            if choice == "1":
                return True
            if choice == "2":
                return False

            choice = None


