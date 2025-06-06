class UnwantedView:
    """
    Virtual View Class storing all the "error's message" corresponding to an input of the user.
    """

    @staticmethod
    def unknown_user_or_password() -> None:
        print("Utilisateur ou mot de passe inconnu.")

    @staticmethod
    def unknown_customer() -> None:
        print("Ce client n'existe pas.")

    @staticmethod
    def unknown_event() -> None:
        print("Cet événement n'existe pas.")

    @staticmethod
    def unknown_contract(contract_name: str) -> None:
        print(f"Aucun contrat {contract_name} trouvé.")

    @staticmethod
    def access_denied():
        print("Vous n'avez pas l'autorisation d'accéder à ceci.")

    @staticmethod
    def bad_password() -> None:
        print("Vous avez donné un mauvais mot de passe.")

    @staticmethod
    def already_used_prompt(category: str, data: str, is_feminine: bool = False) -> None:
        feminine: str = "e" if is_feminine else ""
        print(f'{category} {data} est déjà utlisé{feminine}, veuillez en choisir un{feminine} autre, svp.')

    @classmethod
    def username_already_used(cls, username: str) -> None:
        cls.already_used_prompt("Le nom d'utilisateur", username)

    @staticmethod
    def missing_collaborator(username: str) -> None:
        print(f"Le collaborateur {username} n'est pas présent dans la base de données")

    @classmethod
    def mail_already_used(cls, mail: str) -> None:
        cls.already_used_prompt("L'adresse mail", mail, True)

    @staticmethod
    def unknown_option() -> None:
        print(
            "\nCette option n'existe malheureusement pas,"
            " veuillez sélectionner une commande valide parmi la liste\n")

    @staticmethod
    def error_price() -> float:
        return -1.00

    @staticmethod
    def different_passwords_prompt() -> None:
        print("Vous avez donné deux mots de passe différents")

    @staticmethod
    def modification_canceled() -> None:
        print("Annulation de la demande de modification\n")

    @staticmethod
    def unknown_sales_collaborator(collab_name: str) -> None:
        print(f"Le collaborateur {collab_name} n'existe pas ou n'appartient pas au département commercial.")

    @staticmethod
    def unknown_support_collaborator(collab_name: str) -> None:
        print(f"Le collaborateur {collab_name} n'existe pas ou n'appartient pas au département support.")

    @staticmethod
    def cannot_delete_own_account():
        print("Vous ne pouvez pas supprimer votre propre compte.")
