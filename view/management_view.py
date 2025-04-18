from view.generic_view import View
from settings.settings import ROLES_LIST


class ManagementView(View):
    @classmethod
    def collab_menu(cls) -> str:
        choices_list: list = ["Créer un collaborateur", "Modifier un collaborateur",
                              "Supprimer un collaborateur", "Liste des collaborateurs"]

        return cls.choice_loop(cls.what_to_do(), choices_list)

    @classmethod
    def menu(cls) -> str:
        choices_list: list = ["Collaborateurs", "Contrats", "Événements", "Clients", "Mon Compte"]

        return cls.choice_loop(cls.category_question(), choices_list)

    @classmethod
    def collab_list_menu(cls):
        choices_list: list = ["Consulter la liste de tous les collaborateurs", "Consulter la liste d'un département"]

        return cls.choice_loop(cls.what_to_do(), choices_list)

    @classmethod
    def asks_role(cls, modification: bool = False) -> str:
        new = "nouveau " if modification else ""
        question: str = f"Définissez son {new}rôle:"
        choice: str = cls.choice_loop(question, ROLES_LIST).strip()

        return cls.roles_enum(choice)

    @classmethod
    def which_role(cls) -> str:
        question: str = "De quel département souhaitez-vous consulter la liste des employés ?"
        choice: str = cls.choice_loop(question, ROLES_LIST).strip()

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

    @staticmethod
    def deletion_complete():
        print("Suppression terminée.\n")

    @staticmethod
    def canceled_deletion(category: str = ""):
        print(f"Suppression {category} annulée.\n")

    @classmethod
    def contract_menu(cls) -> str:
        choices = ["Créer un contrat", "Modifier un contrat",
                   "Voir la liste des contrats", "Voir les informations d'un contrat", "Supprimer un contrat"]
        return cls.choice_loop(cls.what_to_do(), choices)

    @classmethod
    def asks_contract_total_value(cls):
        # todo possible utiliser la lib mock pour utiliser le décorateur side_effect, permettant d'entrer des inputs
        while True:
            print("Quel est le montant total du contrat ?")
            new_price = input("").strip()
            new_float_price = cls.check_price_validity(new_price)
            if new_float_price > cls.error_price():
                return new_float_price

    @classmethod
    def event_menu_display(cls) -> str:
        choices_list: list = ["Afficher tous les événements", "Afficher un événement en particulier",
                              "Modifier le collaborateur travaillant sur un événement"]
        return cls.choice_loop(cls.what_to_do(), choices_list)

    @classmethod
    def events_will_loose_support(cls) -> bool:
        print("Tous les événements gérer par ce collaborateur vont se retrouver sans personne pour les gérer.")
        print("Confirmer la suppression ?")

        return cls.yes_or_no_choice()