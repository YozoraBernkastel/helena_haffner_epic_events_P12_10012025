from view.support_view import SupportView as View
from control.generic_controller import GenericController
from models.db_models import Collaborator, Event


class SupportController(GenericController):
    def __init__(self, user: Collaborator):
        self.user: Collaborator = user

    def all_my_events(self) -> None:
        my_events = Event.select().where(Event.support == self.user).execute()
        [View.event_display(event) for event in my_events]

    def event_modification(self, event: Event) -> None:
        choice = View.event_modification_menu(event.name)

        if choice == "1":
            new_name = View.rename_event()
            self.modify_obj(event, "name", new_name)
        elif choice == "2":
            time = self.create_specific_datetime(is_starting=True)
            self.modify_obj(event, "starting_time", time)
        elif choice == "3":
            time = self.create_specific_datetime()
            self.modify_obj(event, "ending_time", time)
        elif choice == "4":
            address = View.asks_event_address()
            self.modify_obj(event, "address", address)
        elif choice == "5":
            attendant_number = View.asks_number_of_participants()
            self.modify_obj(event, "attendant_number", attendant_number)
        elif choice == "6":
            self.information_modification(event)
        else:
            return

    def modify_event(self) -> None:
        event: Event | None = self.find_event()
        if not isinstance(event, Event):
            View.modification_canceled()
            return

        self.event_modification(event)

    def home_menu(self) -> None:
        while True:
            choice = View.menu()

            if choice == "1":
                self.all_my_events()
            elif choice == "2":
                self.event_display()
            elif choice == "3":
                self.modify_event()
            elif choice == "4":
                self.account_menu(self.user)
            else:
                return
