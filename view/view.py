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