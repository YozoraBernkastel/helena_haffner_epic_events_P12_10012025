from view.generic_view import View
from settings.settings import ROLES_LIST


class ManagementView(View):
    @classmethod
    def collab_menu(cls) -> str:
        choices_list: list = ["Créer un collaborateur", "Modifier un collaborateur",
                              "Supprimer un collaborateur", "Voir la liste des collaborateurs"]

        return cls.choice_loop(cls.what_to_do(), choices_list)

    @classmethod
    def menu(cls) -> str:
        choices_list: list = ["Collaborateurs", "Contrats", "Événements", "Mon Compte"]

        return cls.choice_loop(cls.category_question(), choices_list)

    @classmethod
    def asks_collab_password(cls) -> str:
        return cls.asks_password_template("Définissez son mot de passe:")

    @classmethod
    def asks_role(cls, modification: bool = False) -> str:
        new = "nouveau " if modification else ""
        question: str = f"Définissez son {new}rôle:"
        choice: str = ManagementView.choice_loop(question, ROLES_LIST).strip()

        return cls.roles_enum(choice)

    @classmethod
    def which_info_change(cls):
        question: str = "Quelle information souhaitez-vous modifier ?"
        choices_list: list = ["Nom d'utilisateur", "Rôle", "Mot de passe"]
        return cls.choice_loop(question, choices_list)

    @classmethod
    def asks_collab_delete_confirmation(cls, username):
        print(f"Confirmer la suppression du compte de {username}")
        return cls.yes_or_no_choice()






