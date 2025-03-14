from view.generic_view import View
from settings.settings import WHAT_TO_DO, ROLES_LIST, MANAGEMENT, SUPPORT, SALES


class ManagementView(View):
    @classmethod
    def collab_menu(cls) -> str:
        choices_list: list = ["Créer un collaborateur", "Modifier un collaborateur",
                              "Supprimer un collaborateur", "Voir la liste des collaborateurs"]

        return cls.choice_loop(WHAT_TO_DO, choices_list)

    # @classmethod
    # def contracts_menu(cls) -> str:
    #     choices_list: list = ["Créer un contrat", "Supprimer un contrat"]
    #     return cls.choice_loop(WHAT_TO_DO, choices_list)
    #
    # @classmethod
    # def events_menu(cls) -> str:
    #     question = "Quel contrat souhaitez-vous modifier ?"
    #     # todo afficher la liste des contrats présents dans la db
    #     choices_list: list = ["contrat 1", "contrat 2"]
    #     return cls.choice_loop(question, choices_list)

    @classmethod
    def menu(cls) -> str:
        question: str = "Quelle catégorie souhaitez-vous consulter ? "
        choices_list: list = ["Collaborateurs", "Contrats", "Événements", "Mon Compte"]

        return cls.choice_loop(question, choices_list)

    @staticmethod
    def asks_username(complete: str = "") -> str:
        View.quit_print(f'Nom du collaborateur {complete}:')
        return input("").strip()

    @classmethod
    def asks_password(cls) -> str:
        return cls.asks_password_template("Définissez son mot de passe:")

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
    def asks_role(cls, modification: bool = False) -> str:
        new = "new " if modification else ""
        question: str = f"Définissez {new}son rôle:"
        choice: str = ManagementView.choice_loop(question, ROLES_LIST).strip()

        return cls.roles_enum(choice)

    @classmethod
    def which_info_change(cls):
        question: str = "Quelle information souhaitez-vous modifier ?"
        choices_list: list = ["Nom d'utilisateur", "Rôle", "Mot de passe"]
        return cls.choice_loop(question, choices_list)






