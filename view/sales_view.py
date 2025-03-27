from view.generic_view import View
from models.db_models import Customer


class SalesView(View):
    @classmethod
    def contracts_menu(cls) -> None:
        pass

    @classmethod
    def events_menu(cls) -> None:
        pass

    @classmethod
    def customer_menu(cls):
        choices_list: list = ["Créer un nouveau client", "Modifier un de mes client",
                              "Voir ma liste de clients", "Consulter les informations d'un client"]
        return cls.choice_loop(cls.what_to_do(), choices_list)

    @classmethod
    def menu(cls) -> str:
        choices_list: list = ["Mes Clients", "Mes Contrats", "Mes Événements", "Mon Compte"]
        return cls.choice_loop(cls.category_question(), choices_list)

    @classmethod
    def asks_customer_mail(cls) -> str:
        cls.quit_print("Veuillez renseigner l'adresse email du client")
        return input("").strip()

    @classmethod
    def new_customer_name(cls) -> str:
        question = "Comment se nomme votre nouveau client ?"
        return cls.no_blank_answer(question)

    @classmethod
    def new_customer_company(cls) -> str:
        question = "À quelle entreprise appartient-il ?"
        return cls.no_blank_answer(question)

    @classmethod
    def asks_customer_phone_number(cls) -> str:
        question = "Quel est son numéro de téléphone ?"
        return cls.no_blank_answer(question)

    @staticmethod
    def asks_info():
        print("Informations complémentaires ? (facultatif)")
        return input("")

    @classmethod
    def customer_modification_menu(cls, customer_name) -> str:
        question = f"Quelle information du client {customer_name} souhaitez-vous modifier ?"
        choices_list = ["Modifier son nom", "Modifier son adresse mail", "Modifier son numéro de téléphone",
                        "Modifier le nom de son entreprise", "Modifier son commercial",
                        "Modifier les informations du le client"]

        return cls.choice_loop(question, choices_list)

    @classmethod
    def rename_customer_prompt(cls, customer_name) -> str:
        question = f"Renseignez le nouveau nom du client {customer_name} :"
        return cls.no_blank_answer(question)

    @classmethod
    def new_mail_customer_prompt(cls, customer_name: str) -> str:
        question = f"Quelle est la nouvelle adresse mail de {customer_name} ?"
        return cls.no_blank_answer(question).strip()

    @classmethod
    def new_phone_customer_prompt(cls, customer_name) -> str:
        question = f"Quel est le nouveau numéro de téléphone de {customer_name} ?"
        return cls.no_blank_answer(question).strip()

    @classmethod
    def new_company_prompt(cls, customer_name) -> str:
        question = f"Quel est le nouveau nom del 'entrerprise de {customer_name} ?"
        return cls.no_blank_answer(question)

    @classmethod
    def customer_info_menu(cls):
        choices_list = ["Ajouter des informations", "Modifier les informations", "Supprimer les informations"]

        return cls.choice_loop(cls.what_to_do(), choices_list)

    @staticmethod
    def add_customer_info_prompt(customer) -> str:
        print("Ecrivez les informations à ajouter :")
        return input("")

    @staticmethod
    def display_customer_detail(customer: Customer):
        print(f"\n   Nom : {customer.full_name}")
        print(f"   Mail : {customer.mail}")
        print(f"   Entreprise : {customer.company_name}")
        print(f"   Créé le : {customer.creation_date}")
        print(f"   Nom de son contact : {customer.collaborator.username}")
        print(f"   Informations complémentaires : {customer.information}\n")
