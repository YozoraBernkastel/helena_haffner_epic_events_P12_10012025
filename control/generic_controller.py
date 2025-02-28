

class GenericController:
    @staticmethod
    def is_quitting(choice: str) -> bool:
        return choice.lower() == "q"