from view.generic_view import View


class ManagementView(View):
    @classmethod
    def users_db_menu(cls) -> str:
        check_answer: bool = False
        choice = ""
        choices_list: list = ["Créer un utilisateur", "Modifier un utilisateur", "Supprimer un utilisateur"]

        # todo créer et utiliser un décorateur contenant la while loop et permettant de donner un argument à valid_choices !!!
        while not check_answer:
            print("Que souhaitez-vous faire ? ")
            cls.print_choices(choices_list)
            cls.quit_option()

            choice: str = input("")
            choice = choice.strip()

            if cls.is_choice_valid(choice, len(choices_list)):
                check_answer = True
            else:
                cls.unknown_option()

        return choice

    @classmethod
    def contracts_menu(cls) -> None:
        print("Que souhaitez-vous faire ? ")
        choices_list: list = ["Créer un contrat", "Supprimer un utilisateur"]
        cls.print_choices(choices_list)
        cls.quit_option()

    @classmethod
    def events_menu(cls) -> None:
        print("event menu")
        pass

    @classmethod
    def menu(cls) -> str:
        check_answer: bool = False
        choice = ""

        while not check_answer:
            print("Quelle catégorie souhaitez-vous consulter ? ")
            choices_list: list = ["Utilisateurs", "Contrats", "Événements"]
            cls.print_choices(choices_list)
            cls.quit_option()

            choice: str = input("")
            choice = choice.strip()

            if cls.is_choice_valid(choice, len(choices_list)):
                check_answer = True
            else:
                cls.unknown_option()

        return choice




