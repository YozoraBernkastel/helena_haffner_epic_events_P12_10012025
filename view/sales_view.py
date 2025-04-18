from view.generic_view import View
from models.db_models import Customer, Contract


class SalesView(View):
    @classmethod
    def contracts_menu(cls) -> None:
        pass

    @classmethod
    def events_menu(cls) -> str:
        choices_list: list = ["Créer un événement", "Voir tous les événements",
                              "Voir les événements de mes contrats sans support", "Voir un événement"]

        return cls.choice_loop(cls.what_to_do(), choices_list)

    @classmethod
    def customer_menu(cls) -> str:
        choices_list: list = ["Créer un nouveau client", "Modifier un de mes client", "Voir la liste des clients",
                              "Consulter les informations d'un client", "Supprimer un Client"]
        return cls.choice_loop(cls.what_to_do(), choices_list)

    @classmethod
    def customer_choice(cls) -> str:
        choices_list: list = ["Voir tous les clients", "Voir mes clients"]

        return cls.choice_loop(cls.what_to_do(), choices_list)

    @classmethod
    def menu(cls) -> str:
        choices_list: list = ["Clients", "Contrats", "Événement", "Mon Compte"]
        return cls.choice_loop(cls.category_question(), choices_list)

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
    def asks_event_address(cls):
        cls.quit_print("À quelle adresse aura lieu l'événement ?")
        return input("")

    @classmethod
    def sales_collab_contract_menu(cls):
        choices = ["Voir mes contrats", "Voir mes contrats n'ayant pas encore d'événement", "Voir un contrat",
                   "Modifier un contrat", "Voir tous les contrats"]
        return cls.choice_loop(cls.what_to_do(), choices).strip()

    @staticmethod
    def no_event_contract(contract: Contract):
        print(f"\n   Nom du contrat : {contract.name}")
        print(f"   Mail du client : {contract.customer.mail}\n")
