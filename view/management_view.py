from tabnanny import check

from view.generic_view import View


class ManagementView(View):
    @classmethod
    def users_db_menu(cls) -> str:
        check_answer: bool = False
        choice = ""

        # todo créer et utiliser un décorateur contenant la while loop et permettant de donner un argument à valid_choices !!!
        while not check_answer:
            print("Que souhaitez-vous faire ? ")
            print("   1) Créer un utilisateur")
            print("   2) Modifier un utilisateur")
            print("   3) Supprimer un utilisateur")
            cls.quit_option()

            choice: str = input("")
            choice = choice.strip()

            if any(choice == valid for valid in cls.valid_choices(3)):
                check_answer = True
            else:
                cls.unknown_option()

        return choice


    @classmethod
    def contracts_menu(cls) -> None:
        print("Que souhaitez-vous faire ? ")
        print("   1) Créer un contrat")
        print("   2) Supprimer un utilisateur")
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
            print("   1) Utilisateurs")
            print("   2) Contrats")
            print("   3) Événements")
            cls.quit_option()

            choice: str = input("")
            choice = choice.strip()

            if any(choice == valid for valid in cls.valid_choices(3)):
                check_answer = True
            else:
                cls.unknown_option()

        return choice




