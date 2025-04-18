from getpass import getpass
from settings.settings import MANAGEMENT, SUPPORT, SALES
from models.db_models import Event, Contract, Collaborator, Customer


class View:
    @staticmethod
    def connection() -> tuple[str, str]:
        print("Pour vous connecter, veuillez renseigner votre nom d'utilisateur:")
        username = input("")
        username = username.strip()
        password_message: str = "Nous avons également besoin de votre mot de passe:"
        password = getpass(prompt=password_message, stream=None)
        password = password

        return username, password

    @staticmethod
    def what_to_do() -> str:
        return "Que souhaitez-vous faire ?"

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

    @classmethod
    def yes_or_no_choice(cls) -> bool:
        cls.print_choices(["oui", "non"])
        choice = input("").strip()

        if choice == "1" or choice.lower() == "oui":
            return True

        return False

    @staticmethod
    def create_with_success(obj: str) -> None:
        print(f"Création {obj} terminée !\n")

    @staticmethod
    def remember_me() -> bool:
        print("Se souvenir de vous ?")
        return View.yes_or_no_choice()

    @staticmethod
    def is_that_you(username: str) -> bool:
        print(f"Êtes-vous bien {username} ?")
        return View.yes_or_no_choice()

    @staticmethod
    def already_used_prompt(category: str, data: str, is_feminine: bool = False) -> None:
        feminine: str = "e" if is_feminine else ""
        print(f'{category} {data} est déjà utlisé{feminine}, veuillez en choisir un{feminine} autre, svp.')

    @classmethod
    def username_already_used(cls, username: str) -> None:
        cls.already_used_prompt("Le nom d'utilisateur", username)

    @classmethod
    def mail_already_used(cls, mail: str) -> None:
        cls.already_used_prompt("L'adresse mail", mail, True)

    @staticmethod
    def hello_prompt(username: str) -> None:
        print(f"Bonjour {username} !\n")

    @classmethod
    def quit_option_print(cls) -> None:
        print("   Q) pour quitter")

    @staticmethod
    def brackets_quit_str() -> str:
        return "('Q' pour quitter)"

    @classmethod
    def quit_print(cls, message: str) -> None:
        print(f"{message} {cls.brackets_quit_str()}")

    @staticmethod
    def category_question() -> str:
        return "Quelle catégorie souhaitez-vous consulter ? "

    @staticmethod
    def valid_choices(max_range: int) -> list:
        quit_choices: list = ["q", "Q"]
        valid_choices_list = [str(i) for i in range(1, max_range + 1)]

        return valid_choices_list + quit_choices

    @staticmethod
    def unknown_option() -> None:
        print(
            "\nCette option n'existe malheureusement pas,"
            " veuillez sélectionner une commande valide parmi la liste\n")

    @staticmethod
    def print_choices(choices_list: list) -> None:
        [print(f"   {index + 1}) {choices_list[index]}") for index in range(0, len(choices_list))]

    @classmethod
    def is_choice_valid(cls, choice: str, max_range: int) -> bool:
        return any(choice == valid for valid in cls.valid_choices(max_range))

    @classmethod
    def choice_loop(cls, question: str, choices_list: list) -> str:
        check_answer: bool = False
        choice = ""

        while not check_answer:
            print(question)
            cls.print_choices(choices_list)
            cls.quit_option_print()

            choice: str = input("")
            choice = choice.strip()

            if cls.is_choice_valid(choice, len(choices_list)):
                check_answer = True
            else:
                cls.unknown_option()

        return choice

    @classmethod
    def asks_password_template(cls, prompt: str) -> str:
        password_message = f"{prompt} {cls.brackets_quit_str()} :\n"
        return getpass(prompt=password_message, stream=None)

    @classmethod
    def asks_actual_password(cls) -> str:
        return cls.asks_password_template("Veuillez indiquer votre mot de passe")

    @staticmethod
    def asks_username(complete: str = "") -> str:
        question = f'Nom du collaborateur {complete}:'
        return View.no_blank_answer(question)

    @classmethod
    def asks_contract_name(cls, complete: str = "") -> str:
        cls.quit_print(f"Quel est le nom du contrat {complete} ?")
        return input("").strip()

    @staticmethod
    def asks_contract_new_name(contract_name: str) -> str:
        print(f"Quel nouveau nom souhaitez-vous donner au contrat {contract_name}?")
        return input("").strip()

    @staticmethod
    def error_price() -> float:
        return -1.00

    @classmethod
    def check_price_validity(cls, price: str) -> float:
        try:
            split_price = price.split(",")
            price = '.'.join(split_price)
            float_price: float = float(price)
            assert float_price >= 0.00
            return float_price
        except:
            print("Erreur dans le montant.")
            return cls.error_price()

    @classmethod
    def update_contract_remain(cls, remain: float) -> float:
        if remain <= 0.00:
            print("Le contrat a déjà été payé en totalité.")
            return 0.00

        while True:
            print(f"D'après le contrat, {remain}€ n'ont pas encore été payées.\nCombien reste-t-il désormais à payer ?")
            new_price: str = input("").strip()
            new_float_price: float = cls.check_price_validity(new_price)
            if remain >= new_float_price > cls.error_price():
                return new_float_price

    @classmethod
    def signed_contract_prompt(cls):
        print("Confirmez-vous que le contrat est signé ?")
        return cls.yes_or_no_choice()

    @classmethod
    def asks_customer_mail(cls) -> str:
        cls.quit_print("Veuillez renseigner l'adresse email du client")
        return input("").strip()

    @staticmethod
    def missing_collaborator(username: str) -> None:
        print(f"Le collaborateur {username} n'est pas présent dans la base de données")

    @staticmethod
    def different_passwords_prompt() -> None:
        print("Vous avez donné deux mots de passe différents")

    @staticmethod
    def modification_canceled() -> None:
        print("Annulation de la demande de modification\n")

    @classmethod
    def wants_to_change_password(cls) -> bool:
        print("Voulez-vous changer votre mot de passe ?")
        return cls.yes_or_no_choice()

    @staticmethod
    def password_updated() -> None:
        print("Mot de passe mis à jour")

    @classmethod
    def reset_collab_password(cls, username: str) -> bool:
        print(f"Voulez-vous changer le mot de passe de {username} ?")
        return cls.yes_or_no_choice()

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
    def no_blank_answer(cls, question: str) -> str:
        response: str = ""
        while response.strip() == "":
            cls.quit_print(question)
            response = input("")

        return response

    @staticmethod
    def modification_done():
        print("Modification effectuée !\n")

    @staticmethod
    def unknown_sales_collaborator(collab_name: str) -> None:
        print(f"Le collaborateur {collab_name} n'existe pas ou n'appartient pas au département commercial.")

    @staticmethod
    def unknown_support_collaborator(collab_name: str) -> None:
        print(f"Le collaborateur {collab_name} n'existe pas ou n'appartient pas au département support.")

    @classmethod
    def asks_event_name(cls) -> str:
        cls.quit_print("Comment se nomme l'événement ?")
        return input("")

    @classmethod
    def asks_number_of_participants(cls) -> int | str:
        choice: str = ""

        while not choice.isdigit():
            cls.quit_print("Combien de personnes participeront-elles à l'événement ?")
            choice = input("").strip()
            if choice.strip().lower() == "q":
                return choice

        return int(choice)

    @classmethod
    def contract_modification_prompt(cls, role: str, is_already_signed: bool):
        choices: list = ["Modifier le nom du contrat", "Mettre à jour le montant payé", ]

        if not is_already_signed:
            choices.append("Valider la signature du contrat")
        if role == MANAGEMENT:
            choices.append("Modifier le commercial")

        return cls.choice_loop(cls.what_to_do(), choices)

    @staticmethod
    def collab_display(collaborator: Collaborator):
        print(f"\n   Nom d'utilisateur : {collaborator.username}")
        print(f"   rôle : {collaborator.role}\n")

    @staticmethod
    def contract_display(contract: Contract):
        print(f"\n   Nom :{contract.name}")
        print(f"   Nom du client : {contract.customer.full_name}")
        print(f"   Entreprise du client : {contract.customer.company_name}")
        print(f"   Nom du commercial : {contract.collaborator.username}")
        print(f"   Montant total : {contract.total_value}€")
        print(f"   Reste à payer : {contract.remains_to_be_paid}€")
        is_signed: str = "Oui" if contract.signed else "Non"
        print(f"   Signé : {is_signed}\n")

    @staticmethod
    def display_customer_detail(customer: Customer):
        print(f"\n   Nom : {customer.full_name}")
        print(f"   Mail : {customer.mail}")
        print(f"   Entreprise : {customer.company_name}")
        print(f"   Créé le : {customer.creation_date}")
        print(f"   Nom de son contact : {customer.collaborator.username}")
        print(f"   Informations complémentaires : {customer.information}\n")

    @classmethod
    def display_customers_detail(cls, my_customers_list: list) -> None:
        [print(f"- Client : {customer.full_name} - mail : {customer.mail} - entreprise : {customer.company_name}")
         for customer in my_customers_list]
        print()

    @staticmethod
    def event_display(event: Event) -> None:
        print(f"\n   Nom :{event.name}")
        print(f"   Nom du client : {event.contract.customer.full_name}")
        print(f"   Contrat : {event.contract.name}")
        print(f"   Début : {event.starting_time}")
        print(f"   Fin : {event.ending_time}")
        print(f"   Adresse : {event.address}")
        print(f"   Nombre de participants : {event.attendant_number}")
        support_name: str = "Aucun" if event.support is None else event.support.username
        print(f"   Technicien : {support_name}")
        print(f"   Commentaires : {event.information}\n")

    @classmethod
    def asks_event_date(cls, is_starting=True) -> tuple[str, str]:
        context: str = "débutera" if is_starting else "terminera"

        cls.quit_print(f"Quel jour {context} l'évenément ? -- au format JJ/MM/YYYY")
        date_info: str = input("").strip()

        cls.quit_print("À quelle heure ? -- au format 18h30  ")
        hour_info: str = input("").strip()

        return date_info, hour_info

    @classmethod
    def info_menu(cls) -> str:
        choices_list = ["Ajouter des informations", "Modifier les informations", "Supprimer les informations"]

        return cls.choice_loop(cls.what_to_do(), choices_list)

    @staticmethod
    def add_info_prompt() -> str:
        print("Ecrivez les informations à ajouter :")
        return input("")

    @staticmethod
    def same_collaborator_prompt():
        print("Vous avez choisit de réattribuer le contrat au même collaborateur.")
