from view.generic_view import View


class SupportView(View):

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
    def menu(cls) -> str:
        choices_list: list = ["Afficher mes événements", "Afficher un de mes événement",
                              "Modifier un de mes événement", "Mon compte"]

        return cls.choice_loop(cls.what_to_do(), choices_list)







