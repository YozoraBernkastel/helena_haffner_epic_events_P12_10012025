from view.generic_view import View


class SupportView(View):
    """
        View Specific to support role's user.
        """

    @classmethod
    def event_modification_menu(cls, event_name: str):
        question: str = f"Quelle information de l'événmement {event_name} souhaitez-vous modifier ?"
        choices_list: list = ["Nommage", "Début de l'événement", "Fin de l'événement",
                              "Adresse", "Nombre de participants", "Commentaire"]

        return cls.choice_loop(question, choices_list)

    @classmethod
    def rename_event(cls) -> str:
        cls.quit_print("Comment voulez-vous renommer l'événement ?")
        return input("")

    @classmethod
    def asks_event_address(cls):
        cls.quit_print("À quelle adresse aura finalement lieu l'événement ?")
        return input("")

    @classmethod
    def event_menu(cls) -> str:
        choices_list: list = ["Afficher mes événements", "Afficher un de mes événement",
                              "Modifier un de mes événement", "Voir tous les événements", "Mon compte"]

        return cls.choice_loop(cls.what_to_do(), choices_list)

    @classmethod
    def menu(cls) -> str:
        choices_list: list = ["Voir les Événements", "Voir tous les Clients", "Voir les contrats"]

        return cls.choice_loop(cls.what_to_do(), choices_list)
