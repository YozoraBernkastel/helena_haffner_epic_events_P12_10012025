from models.db_models import Collaborator, Customer, Contract, Event


class DisplayView:
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
        print(f"   Dernière mise à jour : {customer.last_update}")
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
